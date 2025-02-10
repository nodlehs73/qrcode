# #same color modules in row or column >= 5 add it to penalty
from copy import deepcopy


# same color 2x2 -> add 3

# 10111010000 or 00001011101-> add 40

# Calculate percentage of dark modules
# Get the previous multiple of five and the next one
# subtract both by 50 (taking absolute value)
# divide each by 5
# take smallest multiply by 10 and add it to penalty


def first_type_penalty (matrix): #same color modules in row or column >= 5 add it to penalty
    penalty = 0
    n = len(matrix)
    for i in range (n): # Count rows
        streak = 1
        for j in range (1, n):
            if matrix[i][j] == matrix[i][j - 1]:
                streak += 1
                if streak >= 5:
                    penalty += streak
                    streak = 1
            else:
                streak = 1


    for j in range (n): # Count columns
        streak = 1
        for i in range (1, n):
            if matrix[i][j] == matrix[i - 1][j]:
                streak += 1
            elif streak >= 5:
                penalty += streak
                streak = 1

    return penalty

def second_type_penalty (matrix):
    n = len (matrix)
    penalty = 0
    for i in range (n - 1):
        for j in range (n - 1):
            if matrix[i][j] == matrix[i][j + 1] and matrix[i + 1][j] == matrix[i][j] and matrix[i + 1][j + 1] == matrix[i][j]:
                penalty += 2
    return penalty

def third_type_penalty (matrix):
    n = len (matrix)

    def search_substring (matrix, n, subarray):
        penalty = 0
        for i in range (n):
            for j in range (n - len (subarray) + 1):
                matching = 1
                for k in range (len (subarray)):
                    if matrix[i][j + k] != subarray[k]:
                        matching = 0
                penalty += matching * 40
        return penalty

    # 10111010000 or 00001011101-> add 40
    searching = [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0]
    return search_substring(matrix, n, searching) + search_substring(matrix, n, list (reversed (searching)))

def fourth_type_penalty (matrix):
    n = len (matrix)
    black_modules = 0
    for i in range (n):
        black_modules += matrix[i].count (1)

    black_module_percentage = int(black_modules / (n * n) * 100)
    previous_percentage = black_module_percentage - black_module_percentage % 5
    next_percentage = black_module_percentage + 5 - black_module_percentage % 5 if black_module_percentage % 5 != 0 else black_module_percentage

    subtracted_percentage1 = abs (previous_percentage - 50)
    subtracted_percentage2 = abs (next_percentage - 50)
    subtracted_percentage1 //= 5
    subtracted_percentage2 //= 5

    return min (subtracted_percentage1, subtracted_percentage2) * 10


def total_penalty (matrix):
    return first_type_penalty(matrix) + second_type_penalty(matrix) + third_type_penalty(matrix) + fourth_type_penalty(matrix)

def get_matrix_after_first_mask (matrix, forbidden_matrix):
    matrix_after_first_mask = deepcopy(matrix)
    for i in range (len (matrix)):
        for j in range (len (matrix)):
            if (i + j) % 2 == 0 and not forbidden_matrix[i][j]:
                matrix_after_first_mask[i][j] = matrix[i][j] ^ 1
    return matrix_after_first_mask

def get_matrix_after_second_mask (matrix, forbidden_matrix):
    matrix_after_second_mask = deepcopy(matrix)
    for i in range (len (matrix)):
        for j in range (len (matrix)):
            if i % 2 == 0 and not forbidden_matrix[i][j]:
                matrix_after_second_mask[i][j] = matrix[i][j] ^ 1
    return matrix_after_second_mask

def get_matrix_after_third_mask (matrix, forbidden_matrix):
    matrix_after_third_mask = deepcopy(matrix)
    for i in range (len (matrix)):
        for j in range (len (matrix)):
            if j % 3 == 0 and not forbidden_matrix[i][j]:
                matrix_after_third_mask[i][j] = matrix[i][j] ^ 1
    return matrix_after_third_mask

def get_matrix_after_fourth_mask (matrix, forbidden_matrix):
    matrix_after_fourth_mask = deepcopy(matrix)
    for i in range (len (matrix)):
        for j in range (len (matrix)):
            if (i + j) % 3 == 0 and not forbidden_matrix[i][j]:
                matrix_after_fourth_mask[i][j] = matrix[i][j] ^ 1
    return matrix_after_fourth_mask

def get_matrix_after_fifth_mask (matrix, forbidden_matrix):
    matrix_after_fifth_mask = deepcopy(matrix)
    for i in range (len (matrix)):
        for j in range (len (matrix)):
            if (i // 2 + j // 3) % 2 == 0 and not forbidden_matrix[i][j]:
                matrix_after_fifth_mask[i][j] = matrix[i][j] ^ 1
    return matrix_after_fifth_mask

def get_matrix_after_sixth_mask (matrix, forbidden_matrix):
    matrix_after_sixth_mask = deepcopy(matrix)
    for i in range (len (matrix)):
        for j in range (len (matrix)):
            if ((i * j) % 2 + (i * j) % 3 ) == 0 and not forbidden_matrix[i][j]:
                matrix_after_sixth_mask[i][j] = matrix[i][j] ^ 1
    return matrix_after_sixth_mask

def get_matrix_after_seventh_mask (matrix, forbidden_matrix):
    matrix_after_seventh_mask = deepcopy(matrix)
    for i in range (len (matrix)):
        for j in range (len (matrix)):
            if ((i * j) % 2  + (i * j) % 3) % 2 == 0 and not forbidden_matrix[i][j]:
                matrix_after_seventh_mask[i][j] = matrix[i][j] ^ 1
    return matrix_after_seventh_mask

def get_matrix_after_eighth_mask (matrix, forbidden_matrix):
    matrix_after_eighth_mask = deepcopy(matrix)
    for i in range (len (matrix)):
        for j in range (len (matrix)):
            if ((i + j) % 2 + (i * j) % 3) % 2 == 0 and not forbidden_matrix[i][j]:
                matrix_after_eighth_mask[i][j] = matrix[i][j] ^ 1
    return matrix_after_eighth_mask


mask_functions = [get_matrix_after_first_mask, get_matrix_after_second_mask, get_matrix_after_third_mask, get_matrix_after_fourth_mask, get_matrix_after_fifth_mask, get_matrix_after_sixth_mask, get_matrix_after_seventh_mask, get_matrix_after_eighth_mask]

def get_best_mask (matrix):
    best_penalty = float ('inf')
    best_mask = None

    for i, apply_mask in enumerate(mask_functions):
        mask = bin (i)[2:]
        if total_penalty(apply_mask (matrix)) < best_penalty:
            best_penalty = total_penalty (apply_mask (matrix))
            best_mask = mask

    return best_mask, best_penalty

