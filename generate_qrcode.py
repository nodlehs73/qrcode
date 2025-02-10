from generate_forbidden_matrices import generate_forbidden_matrix
from qr_code_table import qr_code_table
from reedsolo import RSCodec, ReedSolomonError
from remainder_bits_by_version_table import qr_remainder_bits
from generate_forbidden_matrices import all_positions, generate_forbidden_matrix_without_alignment
from best_mask import *
from qr_to_matrix import matrix_to_qrcode
from qr_code_data_encoding import transformare
from qr_version_mask import qr_version_mask
import sys

correction_level_to_binary = {
    "L" : "01",
    "M": "00",
    "Q" : "11",
    "H": "10",
}

def generate_format_string (initial_mask, limit, initial_padding, generator_polynom, qr_code_specification_mask):

    mask = initial_mask + "0" * initial_padding


    while (len (mask) > 0 and mask[0] == "0"):
        mask = mask[1:]


    while (len (mask) > limit):
        new_polynom = generator_polynom
        while (len (new_polynom) != len (mask)):
            new_polynom += "0"

        new_mask = bin (int (mask, 2) ^ int (new_polynom, 2))[2:]
        while (new_mask[0] == "0"):
            new_mask = new_mask[1:]

        mask = new_mask


    while (len (mask) < limit):
        mask = "0" + mask

    final_mask = bin (int (initial_mask + mask, 2) ^ int (qr_code_specification_mask, 2))[2:]

    while (len (final_mask) < limit + len (initial_mask)):
        final_mask = "0" + final_mask
    return final_mask


def fill_mask_and_level_information (matrix, mask):
    n = len (matrix)

    # Filling horizontal
    for j in range (8):
        if (j == 6):
            continue
        matrix[8][j] = int(mask[j])

    idx = 7
    for j in range (n - 8, n):
        matrix[8][j] = int (mask[idx])
        idx += 1

    # Filling vertical

    idx = 0
    for i in range (n - 1, n - 8, -1):
        matrix[i][8] = int (mask[idx])
        idx += 1

    idx = 7
    for i in range (8, -1, -1):
        if i == 6:
            continue
        matrix[i][8] = int (mask[idx])
        idx += 1


def fill_version_information (matrix, mask):
    n = len (matrix)

    for j in range (6):
        for i in range (3):
            row = n - 11 + i
            column = j
            matrix[row][column] = int (mask[j * 3 + i])

    for i in range (6):
        for j in range (3):
            row = i
            column = n - 11 + j
            matrix[row][column] = int (mask[i * 3 + j])


def fill_finder_pattern (matrix, row, column):
    n = len (matrix)
    finder_pattern = [
        "1111111",
        "1000001",
        "1011101",
        "1011101",
        "1011101",
        "1000001",
        "1111111"
    ]
    for i in range (7):
        for j in range (7):
            new_row = row + i
            new_column = column + j
            matrix[new_row][new_column] = int (finder_pattern[i][j])

    # FILL SMALL BLACK SQUARE
    matrix[len (matrix) - 8][8] = 1

def fill_timing_patterns (matrix):
    n = len (matrix)

    #horizontal
    for j in range (8, n - 8, 2):
        matrix[6][j] = 1

    # vertical
    for i in range (8, n - 8, 2):
        matrix[i][6] = 1

def fill_all_alignment_patterns (matrix, forbidden_matrix_without_alignment):
    n = len (matrix)
    version = (n - 17) // 4

    positions = all_positions[version - 1]

    def intersection_with_matrix (forbidden_matrix_without_alignment, row, column):

        for r in range (row - 2, row + 3):
            for c in range (column - 2, column + 3):
                if forbidden_matrix_without_alignment[r][c] == 1:
                    return True
        return False

    def fill_alignment_pattern (matrix, row, col):
        alignment_pattern = [
            "11111",
            "10001",
            "10101",
            "10001",
            "11111"
        ]

        for i in range (5):
            for j in range (5):
                new_row = row + i
                new_column = col + j

                matrix[new_row][new_column] = int (alignment_pattern[i][j])

    for i in range (len (positions)):
        for j in range (len (positions)):
            x, y = positions[i], positions[j]
            if not intersection_with_matrix (forbidden_matrix_without_alignment, x, y):

                fill_alignment_pattern (matrix, x - 2, y - 2)


def fill_qrcode (blocks, correction_level, version, structured_append, image_path):
    matrix_size = 17 + version * 4
    matrix = [[0 for i in range(matrix_size)] for j in range(matrix_size)]
    forbidden_matrix = generate_forbidden_matrix (version)

    n = len (blocks)
    error_correction_codewords_per_block = qr_code_table[version][correction_level]['ec_codewords_per_block']
    rsc = RSCodec(error_correction_codewords_per_block)

    error_correction_blocks = []
    for block in blocks:
        error_correction_codewords = list (rsc.encode (block)[-error_correction_codewords_per_block:])
        error_correction_blocks.append (error_correction_codewords)

    data = []
    for j in range (len (blocks[-1])):
        for i in range (len (blocks)):
            if j < len (blocks[i]):
                data.append(blocks[i][j])

    for j in range (error_correction_codewords_per_block):
        for i in range (len (error_correction_blocks)):
            data.append (error_correction_blocks[i][j])

    intercaleted_string = ""
    for x in data:
        x = bin (x)[2:]
        while (len (x) < 8):
            x = "0" + x
        intercaleted_string += x

    remainder_bits = qr_remainder_bits [version]

    for i in range (remainder_bits):
        intercaleted_string += "0"

    up_or_down = 0
    intercaleted_string_location = 0


    for column in range (matrix_size - 1, -1, -2):
        rows = range (0, matrix_size) if up_or_down == 1 else range (matrix_size - 1, -1, -1)
        for row in rows:
            for offset in range (0, 2 if column != 0 else 1):
                new_column = column - offset
                if forbidden_matrix[row][new_column] == 0:
                    matrix[row][new_column] = int (intercaleted_string[intercaleted_string_location])
                    intercaleted_string_location += 1

        up_or_down ^= 1

    assert (intercaleted_string_location == len (intercaleted_string))

    fill_finder_pattern (matrix, 0, 0)
    fill_finder_pattern (matrix, len (matrix) - 7,0)
    fill_finder_pattern (matrix, 0, len (matrix) - 7)
    fill_timing_patterns(matrix)

    fill_all_alignment_patterns (matrix, generate_forbidden_matrix_without_alignment(version))

    version_bin = bin (version)[2:]
    while (len (version_bin) < 6):
        version_bin = "0" + version_bin

    if version >= 7:
        fill_version_information(matrix, list (reversed (qr_version_mask[version])))
    penalty = float ("inf")

    matrix_after_best_mask = None

    selected_mask = 0
    for i, get_matrix_after_mask in enumerate (mask_functions):
        binary_mask = bin (i)[2:]
        while (len (binary_mask) < 3):
            binary_mask = "0" + binary_mask

        mask = correction_level_to_binary[correction_level] + binary_mask

        fill_mask_and_level_information(matrix, generate_format_string (mask, 10, 10, "10100110111", "101010000010010"))

        masked_matrix = get_matrix_after_mask(matrix, forbidden_matrix)
        if (total_penalty(masked_matrix) < penalty):
            selected_mask = i
            penalty = total_penalty(masked_matrix)
            matrix_after_best_mask = masked_matrix

    matrix_to_qrcode(deepcopy(matrix_after_best_mask), 10, image_path, structured_append)

def get_parity (message):
    parity = 0
    for char in message:
        parity ^= ord(char)

    return parity

def get_single_qr_code (message, error_correction, image_path):
    blocks, version = transformare(message, error_correction, False, -1, -1, -1)
    fill_qrcode (blocks, error_correction, version, False, image_path)

def get_multiple_qr_codes (message, error_correction, number_of_splits):
    n = len (message)
    parity = get_parity (message)

    if number_of_splits > 16:
        raise Exception ("Number of splits must be less than or equal to 16")

    split_message = [[] for _ in range (number_of_splits)]
    split_length = n // number_of_splits

    for i in range (n):
        split_message[min (number_of_splits - 1, i // split_length)].append (message[i])

    for i, partial_message in enumerate(split_message):
        partial_message = "".join (partial_message)
        blocks, version = transformare (partial_message, error_correction, True, i, len (split_message) - 1, parity)
        fill_qrcode (blocks, error_correction, version, True, "")
