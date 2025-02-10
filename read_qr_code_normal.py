from qr_to_matrix import png_to_binary_matrix
from math import floor
from qr_code_table import qr_code_table
from reedsolo import RSCodec

# Cod importat pentru generarea matricei cu zonele interzise

################################################################


forbidden_matrices = []
all_positions = [[], [6, 18], [6, 22], [6, 26], [6, 30], [6, 34], [6, 22, 38], [6, 24, 42], [6, 26, 46], [6, 28, 50],
                 [6, 30, 54], [6, 32, 58], [6, 34, 62], [6, 26, 46, 66], [6, 26, 48, 70], [6, 26, 50, 74],
                 [6, 30, 54, 78], [6, 30, 56, 82], [6, 30, 58, 86], [6, 34, 62, 90], [6, 28, 50, 72, 94],
                 [6, 26, 50, 74, 98], [6, 30, 54, 78, 102], [6, 28, 54, 80, 106], [6, 32, 58, 84, 110],
                 [6, 30, 58, 86, 114], [6, 34, 62, 90, 118], [6, 26, 50, 74, 98, 122], [6, 30, 54, 78, 102, 126],
                 [6, 26, 52, 78, 104, 130], [6, 30, 56, 82, 108, 134], [6, 34, 60, 86, 112, 138],
                 [6, 30, 58, 86, 114, 142], [6, 34, 62, 90, 118, 146], [6, 30, 54, 78, 102, 126, 150],
                 [6, 24, 50, 76, 102, 128, 154], [6, 28, 54, 80, 106, 132, 158], [6, 32, 58, 84, 110, 136, 162],
                 [6, 26, 54, 82, 110, 138, 166], [6, 30, 58, 86, 114, 142, 170]]



def generate_forbidden_matrices():
    global forbidden_matrices
    for version in range(1, 41):
        forbidden_matrices.append(generate_forbidden_matrix(version))


def generate_forbidden_matrix(version):
    n = 17 + version * 4

    forbidden_matrix = [[0 for j in range(n)] for i in range(n)]

    fill_finder_patterns(forbidden_matrix)
    fill_allignment_patterns(forbidden_matrix)
    fill_timing_patterns(forbidden_matrix)

    if version >= 7:
        fill_version_information(forbidden_matrix)

    return forbidden_matrix


def generate_forbidden_matrix_without_alignment(version):
    n = 17 + version * 4

    forbidden_matrix = [[0 for j in range(n)] for i in range(n)]

    fill_finder_patterns(forbidden_matrix)
    #  fill_timing_patterns(forbidden_matrix)

    if version >= 7:
        fill_version_information(forbidden_matrix)

    return forbidden_matrix


def fill_allignment_patterns(forbidden_matrix):
    global all_positions

    qr_code_version = (len(forbidden_matrix) - 21) // 4

    def intersection_with_matrix(matrix, line, column):
        for r in range(line - 2, line + 3):
            for c in range(column - 2, column + 3):
                if matrix[r][c] != 0:
                    return True
        return False

    def fill_finder_pattern(matrix, line, column):
        for r in range(line - 2, line + 3):
            for c in range(column - 2, column + 3):
                matrix[r][c] = 1

    allignment_pattern_positions = all_positions[qr_code_version]

    for i in range(len(allignment_pattern_positions)):
        for j in range(len(allignment_pattern_positions)):
            line = allignment_pattern_positions[i]
            column = allignment_pattern_positions[j]

            if intersection_with_matrix(forbidden_matrix, line, column) == False:
                fill_finder_pattern(forbidden_matrix, line, column)


def fill_finder_patterns(forbidden_matrix):
    n = len(forbidden_matrix)

    # Fill top left
    for i in range(9):  # Pana la 9 ca sa includ si format string ul
        for j in range(9):
            forbidden_matrix[i][j] = 1

    # Fill top right
    for i in range(9):
        for j in range(n - 8, n):
            forbidden_matrix[i][j] = 1

    # Fill bottom left
    for i in range(n - 8, n):
        for j in range(9):
            forbidden_matrix[i][j] = 1


def fill_timing_patterns(forbidden_matrix):
    n = len(forbidden_matrix)

    # Fill row
    for j in range(8, n - 7):
        forbidden_matrix[6][j] = 1

    # Fill columns
    for i in range(8, n - 7):
        forbidden_matrix[i][6] = 1

    # Patratel unic negru
    forbidden_matrix[n - 8][8] = 1


def fill_version_information(forbidden_matrix):
    n = len(forbidden_matrix)
    for i in range(n - 11, n - 8):
        for j in range(6):
            forbidden_matrix[i][j] = 1
    for i in range(6):
        for j in range(n - 11, n - 8):
            forbidden_matrix[i][j] = 1


generate_forbidden_matrices()


#######################################################


def convert_byte_to_character(byte_encoded_data, interleaved_message):

    power = 2 ** 7
    code_of_character = 0
    for i in range(8):
        code_of_character += byte_encoded_data[i] * power
        power //= 2

    interleaved_message.append(code_of_character)


def convert_byte_to_character_for_error(byte_encoded_data, interleaved_error_codewords):

    power = 2 ** 7
    code_of_character = 0
    for i in range(8):
        code_of_character += byte_encoded_data[i] * power
        power //= 2

    interleaved_error_codewords.append(code_of_character)

def read_qr_code_normal (file_path):

    # Citeste matricea de pe poza
    binary_matrix, version = png_to_binary_matrix(file_path)

    n = len (binary_matrix)

    # Matricea de pozitii interzise
    forbidden_matrix = generate_forbidden_matrix(version)

    # Aflam EC level si mask pattern din primii 5 biti din format string, XOR-ati cu 10101 (din masca spaciala de la format string)

    EC_level_and_mask = "".join(map(str, binary_matrix[8][0:5]))

    first_bits_from_xor_mask = "10101"

    EC_level_and_mask_list = list(EC_level_and_mask)

    for i in range(5):
        EC_level_and_mask_list[i] = str(int(EC_level_and_mask[i]) ^ int(first_bits_from_xor_mask[i]))


    # Din EC_level_and_mask_list scoatem EC level si mask pattern

    error_correction_level = int(EC_level_and_mask_list[1]) + int(EC_level_and_mask_list[0]) * 2
    mask_pattern = int(EC_level_and_mask_list[4]) + int(EC_level_and_mask_list[3]) * 2 + int(EC_level_and_mask_list[2]) * 4


    # Am aflat mask pattern, deci acum aducem matricea la forma initiala, inainte de aplicarea mastii
    # Modific bianry_matrix

    for i in range(n):
        for j in range(n):
            if forbidden_matrix[i][j] == 0:
                if mask_pattern == 0:
                    if (i + j) % 2 == 0:
                        binary_matrix[i][j] = 1 - binary_matrix[i][j]

                if mask_pattern == 1:
                    if i % 2 == 0:
                        binary_matrix[i][j] = 1 - binary_matrix[i][j]

                if mask_pattern == 2:
                    if j % 3 == 0:
                        binary_matrix[i][j] = 1 - binary_matrix[i][j]

                if mask_pattern == 3:
                    if (i + j) % 3 == 0:
                        binary_matrix[i][j] = 1 - binary_matrix[i][j]

                if mask_pattern == 4:
                    if (floor(i // 2) + floor(j // 3)) % 2 == 0:
                        binary_matrix[i][j] = 1 - binary_matrix[i][j]

                if mask_pattern == 5:
                    if ((i * j) % 2) + ((i * j) % 3) == 0:
                        binary_matrix[i][j] = 1 - binary_matrix[i][j]

                if mask_pattern == 6:
                    if (((i * j) % 2) + ((i * j) % 3)) % 2 == 0:
                        binary_matrix[i][j] = 1 - binary_matrix[i][j]

                if mask_pattern == 7:
                    if (((i + j) % 2) + ((i * j) % 3)) % 2 == 0:
                        binary_matrix[i][j] = 1 - binary_matrix[i][j]


    # Mode indicator-ul este 0100 - lucarm in Byte Mode
    mode_indicator = "0100"

    # Pe cati biti se afla dimensiunea mesajului care trebuie citit
    if version <= 9:
        character_count_size = 8
    else:
        character_count_size = 16

    if error_correction_level == 0:
        error_correction_letter = 'M'

    elif error_correction_level == 1:
        error_correction_letter = 'L'

    elif error_correction_level == 2:
        error_correction_letter = 'H'

    else:
        error_correction_letter = 'Q'

    # Luam din tabel nuamrul de data codeword-uri si cate codeword-uri sunt in fiecare bloc

    total_number_of_codewords = qr_code_table[version][error_correction_letter]['total_data_codewords']

    blocks_in_group_1 = qr_code_table[version][error_correction_letter]['blocks_in_group1']

    data_codewords_block_group_1 = qr_code_table[version][error_correction_letter]['data_codewords_group1']

    blocks_in_group_2 = qr_code_table[version][error_correction_letter]['blocks_in_group2']

    data_codewords_block_group_2 = qr_code_table[version][error_correction_letter]['data_codewords_group2']

    # Aflam numarul de caractere al mesajului encodat din bitii din Character Count Indicator

    matrix_line_index = n - 1
    matrix_column_index = n - 1
    bits_placement_direction = 0
    movement_counter = 0  # Ca sa vad daca acum trebuie sa merge la stanga sau in dr-sus,  respectiv la stanga sau dr-jos

    bits_counter = 0

    # Incepem sa parcurgem cate 8 biti pt fiecare caracter din mesaj si punem intr-o lista reprezentarea in decimal a fiecarui byte parcurs

    interleaved_message = []

    # Retin intr-o lista tot cate 8 biti cititi, pe care ii transform in caracter si adaug la lista interleaved_message
    total_number_of_bits_data_codewords = total_number_of_codewords * 8

    bits_in_byte_counter = 0
    byte_encoded_data = [0 for i in range(8)]

    while bits_counter < total_number_of_bits_data_codewords:
        if forbidden_matrix[matrix_line_index][matrix_column_index] == 0:
            bits_counter += 1

            byte_encoded_data[bits_in_byte_counter] = binary_matrix[matrix_line_index][matrix_column_index]
            bits_in_byte_counter += 1

            if bits_in_byte_counter == 8:
                convert_byte_to_character(byte_encoded_data, interleaved_message)
                bits_in_byte_counter = 0

        if bits_placement_direction % 2 == 0:  # Daca se merge in sus
            if movement_counter % 2 == 0:  # Se merge la stanga
                matrix_column_index -= 1
            else:  # Se merge in dreapta-sus
                matrix_column_index += 1
                matrix_line_index -= 1

        else:  # Se merge in jos
            if movement_counter % 2 == 0:  # Se merge la stanga
                matrix_column_index -= 1
            else:  # Se merge in dreapta-jos
                matrix_column_index += 1
                matrix_line_index += 1

        movement_counter += 1

        # Verific daca trebuie schimbata directia de mers pe cele 2 coloane
        if matrix_line_index == -1:
            bits_placement_direction += 1
            movement_counter = 0

            matrix_line_index = 0
            matrix_column_index -= 2

        elif matrix_line_index == n:
            bits_placement_direction += 1
            movement_counter = 0

            matrix_line_index = n - 1
            matrix_column_index -= 2

    ################################################
    # Dupa ce am sirul de codewords intercalat, il pun intr-o matrice pe coloane
    # Apoi sirul corect, adica secvential, va fi cel obtinut la citirea pe linie in matrice

    line_dimension = blocks_in_group_1 + blocks_in_group_2
    column_dimension = data_codewords_block_group_1 + 1


    message_matrix = [[0 for j in range(column_dimension)] for i in range(line_dimension)]

    interleaved_message_index = 0

    for j in range(column_dimension - 1):
        for i in range(line_dimension):
            message_matrix[i][j] = interleaved_message[interleaved_message_index]
            interleaved_message_index += 1

    # Daca mai sunt caractere in mesaj (daca exista blocuri in grupul 2 )
    if interleaved_message_index < total_number_of_codewords - 1:
        for i in range(blocks_in_group_1, line_dimension):
            message_matrix[i][column_dimension - 1] = interleaved_message[interleaved_message_index]
            interleaved_message_index += 1


    sequential_bit_string_of_codewords = ""

    for i in range(line_dimension):
        if i < blocks_in_group_1:
            for j in range(column_dimension - 1):
                binary_representation = format(message_matrix[i][j], '08b')
                sequential_bit_string_of_codewords += binary_representation

        else:
            for j in range(column_dimension):
                binary_representation = format(message_matrix[i][j], '08b')
                sequential_bit_string_of_codewords += binary_representation


    # Stim sirul secvential in binar, pornim de dupa chracater count si sarim din 8 in 8, pana aflam toate caracterele din mesaj

    mode_indicator_and_character_count = 4 + character_count_size

    number_of_characters_in_message = int(sequential_bit_string_of_codewords[4: (mode_indicator_and_character_count)], 2)

    index_for_character = mode_indicator_and_character_count

    final_message = []

    for i in range(number_of_characters_in_message):
        character = chr(int(sequential_bit_string_of_codewords[index_for_character: (index_for_character + 8)], 2))
        final_message.append(character)
        index_for_character += 8


    ##############################################################################################

    # CORECTAREA ERORILOR

    error_correction_codewords = qr_code_table[version][error_correction_letter]['ec_codewords_per_block'] * (
                blocks_in_group_1 + blocks_in_group_2)


    # Incepem sa parcurgem cate 8 biti pt fiecare error codeword si punem intr-o lista reprezentarea in decimal a fiecarui byte parcurs
    # Incepem parcurgerea de unde ne-am oprit la data codewords

    interleaved_error_codewords = []

    # Retin intr-o lista tot cate 8 biti cititi, pe care ii transform in decimal si adaug la lista interleaved_error_codewords
    bits_data_and_error_codewords = total_number_of_bits_data_codewords + 8 * error_correction_codewords


    bits_in_byte_counter = 0
    # byte_encoded_data = [0 for i in range(8)]


    while bits_counter < bits_data_and_error_codewords:
        if forbidden_matrix[matrix_line_index][matrix_column_index] == 0:
            bits_counter += 1

            byte_encoded_data[bits_in_byte_counter] = binary_matrix[matrix_line_index][matrix_column_index]
            bits_in_byte_counter += 1

            if bits_in_byte_counter == 8:
                convert_byte_to_character_for_error(byte_encoded_data, interleaved_error_codewords)
                bits_in_byte_counter = 0

        if bits_placement_direction % 2 == 0:  # Daca se merge in sus
            if movement_counter % 2 == 0:  # Se merge la stanga
                matrix_column_index -= 1
            else:  # Se merge in dreapta-sus
                matrix_column_index += 1
                matrix_line_index -= 1

        else:  # Se merge in jos
            if movement_counter % 2 == 0:  # Se merge la stanga
                matrix_column_index -= 1
            else:  # Se merge in dreapta-jos
                matrix_column_index += 1
                matrix_line_index += 1

        movement_counter += 1

        # Verific daca trebuie schimbata directia de mers pe cele 2 coloane
        if matrix_line_index == -1:
            bits_placement_direction += 1
            movement_counter = 0

            matrix_line_index = 0
            matrix_column_index -= 2

        elif matrix_line_index == n:
            bits_placement_direction += 1
            movement_counter = 0

            matrix_line_index = n - 1
            matrix_column_index -= 2


    ################################################
    # Dupa ce am sirul de error codewords intercalat, il pun intr-o matrice pe coloane
    # Apoi sirul corect, adica secvential, va fi cel obtinut la citirea pe linie in matrice

    error_line_dimension = blocks_in_group_1 + blocks_in_group_2
    error_column_dimension = error_correction_codewords // error_line_dimension


    error_matrix = [[0 for j in range(error_column_dimension)] for i in range(error_line_dimension)]

    interleaved_error_index = 0

    for j in range(error_column_dimension):
        for i in range(error_line_dimension):
            error_matrix[i][j] = interleaved_error_codewords[interleaved_error_index]
            interleaved_error_index += 1


    sequential_bit_string_of_error_codewords = ""

    for i in range(error_line_dimension):
        for j in range(error_column_dimension):
            binary_representation = format(error_matrix[i][j], '08b')
            sequential_bit_string_of_error_codewords += binary_representation


    # Stim sirul secvential in binar, sarim din 8 in 8, pana aflam toate caracterele din mesaj

    index_for_character = 0

    final_errors = []

    for i in range(error_correction_codewords):
        error_number = int(sequential_bit_string_of_error_codewords[index_for_character: (index_for_character + 8)], 2)
        final_errors.append(error_number)
        index_for_character += 8


    # Transform mesajul intr-un bytearray

    total_sequential_bit_string_of_rsc_codewords = ""

    for i in range(line_dimension):
        message_matrix[i][0] += 1
        if i < blocks_in_group_1:
            message_bytes = bytearray(message_matrix[i][:-1])
        else:
            message_bytes = bytearray(message_matrix[i])

        error_codewords_bytes = bytearray(error_matrix[i])

        full_data = message_bytes + error_codewords_bytes

        rsc = RSCodec(qr_code_table[version][error_correction_letter]['ec_codewords_per_block'])

        # decoded_data, error = rsc.decode( full_data )


        L = list(rsc.decode(full_data)[0])

        sequential_bit_string_of_rsc_codewords = ""

        for i in range(len(L)):
            binary_representation = format(L[i], '08b')
            sequential_bit_string_of_rsc_codewords += binary_representation

        total_sequential_bit_string_of_rsc_codewords += sequential_bit_string_of_rsc_codewords


    if character_count_size == 8:
        number_of_characters_in_total_sequential_bit_string_of_rsc_codewords = int(
            total_sequential_bit_string_of_rsc_codewords[4:12], 2)
    else:
        number_of_characters_in_total_sequential_bit_string_of_rsc_codewords = int(
            total_sequential_bit_string_of_rsc_codewords[4:20], 2)

    encoded_message = ""
    for i in range(number_of_characters_in_total_sequential_bit_string_of_rsc_codewords):
        if character_count_size == 8:
            character_at_position_i_in_total_sequential_bit_string_of_rsc_codewords = chr(
                int(total_sequential_bit_string_of_rsc_codewords[12 + i * 8: 12 + (i + 1) * 8], 2))
            encoded_message += character_at_position_i_in_total_sequential_bit_string_of_rsc_codewords
        else:
            character_at_position_i_in_total_sequential_bit_string_of_rsc_codewords = chr(
                int(total_sequential_bit_string_of_rsc_codewords[20 + i * 8: 20 + (i + 1) * 8], 2))
            encoded_message += character_at_position_i_in_total_sequential_bit_string_of_rsc_codewords
    print ("Mesajul encodat este")
    print(encoded_message)
