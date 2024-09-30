

# def lukasiewicz_implication(A, B):
#     result = {}
#
#     keys_of_A = list(A.keys())
#     keys_of_B = list(B.keys())
#
#     for key in range(len(A)):
#         A_value = A[keys_of_A[key]]
#         B_value = B[keys_of_B[key]]
#         result[key] = min(1, 1 - A_value + B_value)
#     return result
#
#
# def fuzzy_conjunction(parcel_lines, array_of_X_lines):
#
#     array_of_fuzzy_conjunction_X_lines = []
#
#     for index, parcel_line in enumerate(parcel_lines):
#         array_of_fuzzy_conjunction_X_line = []
#
#         for line in array_of_X_lines[index]:
#             result = min(float(parcel_line), float(line))
#             array_of_fuzzy_conjunction_X_line.append(round(result, 1))
#
#         array_of_fuzzy_conjunction_X_lines.append(array_of_fuzzy_conjunction_X_line)
#
#     return array_of_fuzzy_conjunction_X_lines


def input_memory(line, dict_of_input, array_of_input_memory):

    letter = line.split('=')[0]
    array_of_input_memory.append(letter)
    value = line.split('=')[1]
    variable = value.split(',')[0][2]

    dict_of_input[letter] = variable

    return dict_of_input,  array_of_input_memory


def parcel_memory(line, dict_of_parcels_variables, array_of_parcel_memory):
    letter = line.split('=')[0]
    array_of_parcel_memory.append(letter)
    value = line.split('=')[1]
    variable = value.split(',')[0][2]

    dict_of_parcels_variables[letter] = variable

    return dict_of_parcels_variables, array_of_parcel_memory

def dict_formation():

    dict_of_predicates = {}

    dict_of_input = {}
    array_of_input_memory = []

    with open("../Inputs/input.txt", 'r') as file:

        array_of_lines = file.readlines()

    for line in array_of_lines:
        array_of_values = []
        dict_of_input, array_of_input_memory = input_memory(line, dict_of_input, array_of_input_memory)
        line = line.strip()
        key = line.strip('=')[0]
        value = line.split('=')[1]
        value = value.split(',')
        for string in value:
            if '>' in string:
                string = string[:-1]
                if '>' in string:
                    string = string[:-1]
                array_of_values.append(string)

        dict_of_predicates[key] = array_of_values

    return dict_of_predicates, dict_of_input, array_of_input_memory


def operation_reader():

    with open("../Inputs/operation.txt", 'r') as file:

        array_of_operations = file.readlines()
        for index, value in enumerate(array_of_operations):
            if '\n' in value:
                array_of_operations[index] = value.strip()


    return array_of_operations


def lukasiewicz_implication_new(array_of_operations, dict_of_predicates):

    print(dict_of_predicates)
    array_of_keys = list(dict_of_predicates.keys())
    print(array_of_keys)

    for operation in array_of_operations:
        lukasiewicz_result = []
        param_1 = operation.split('>')[0]
        param_2 = operation.split('>')[1]

        for key in range(len(dict_of_predicates[array_of_keys[0]])):
            value_1 = float(dict_of_predicates[param_1][key])
            value_2 = float(dict_of_predicates[param_2][key])

            result = min(1, 1 - value_1 + value_2)

            lukasiewicz_result.append(result)

    return lukasiewicz_result


def lukasiewicz_matrix_formation(array_of_operations, dict_of_predicates):
    array_of_keys = list(dict_of_predicates.keys())

    length = len(dict_of_predicates[array_of_keys[0]])
    dict_of_matrix = {}

    for operation in array_of_operations:
        matrix_rows = []
        param_1 = operation.split('>')[0]
        param_2 = operation.split('>')[1]

        for external in range(length):
            matrix_row_values_array = []
            value_1 = float(dict_of_predicates[param_1][external])

            for internal in range(length):
                value_2 = float(dict_of_predicates[param_2][internal])

                # result = min(1, 1 - value_1 + value_2)
                result = max(0, value_1 + value_2 - 1)
                result = float(result)
                matrix_row_values_array.append(round(result, 1))

            matrix_rows.append(matrix_row_values_array)
        for row in matrix_rows:
            print(row)

        dict_of_matrix[f"{param_1}~>{param_2}"] = matrix_rows

    return dict_of_matrix


def parcel_reader():
    dict_of_parcels = {}
    dict_of_parcels_variables = {}
    array_of_parcel_memory = []
    with open('../Inputs/parcel.txt', 'r') as file:
        parcels = file.readlines()

    for line in parcels:
        array_of_parcels = []

        line = line.strip()
        dict_of_parcels_variables, array_of_parcel_memory = parcel_memory(line, dict_of_parcels_variables, array_of_parcel_memory)
        key = line.strip('=')[0]
        value = line.split('=')[1]
        value = value.split(',')
        for string in value:
            if '>' in string:
                string = string[:-1]
                if '>' in string:
                    string = string[:-1]
                array_of_parcels.append(float(string))

        dict_of_parcels[key] = array_of_parcels

    return dict_of_parcels, dict_of_parcels_variables, array_of_parcel_memory


def lukasiewicz_parcel(dict_of_matrix, dict_of_parcels):

    print('='*20)

    dict_of_parcel_matrix = {}

    keys = list(dict_of_matrix.keys())
    parcel_keys = list(dict_of_parcels.keys())


    for key in keys:
        array_of_rows = []
        current_array = dict_of_matrix[key]
        for row_index, row in enumerate(current_array):

            array_of_row_values = []

            for row_number in row:
                current_parcel = float(dict_of_parcels[parcel_keys[0]][row_index])
                result = min(current_parcel, row_number)
                result = float(result)
                array_of_row_values.append(round(result, 1))

            array_of_rows.append(array_of_row_values)
            print(f"{array_of_row_values}")

        dict_of_parcel_matrix[key] = array_of_rows

        # Получение столбцов матрицы
        columns = [[row[i] for row in array_of_rows] for i in range(len(array_of_rows[0]))]

        direct_conclusive = []
        for column in columns:
            direct_conclusive.append(max(column))

        # # Вывод результатов
        # for column in columns:
        #     print(f"Колонки: {column}")

        print(f"Прямой вывод: {direct_conclusive}")

    return dict_of_parcel_matrix












dict_of_predicates, dict_of_input, array_of_input_memory = dict_formation()
array_of_operations = operation_reader()
parcel, dict_of_parcels_variables, array_of_parcel_memory = parcel_reader()


# lukasiewicz_implication_new(array_of_operations, dict_of_predicates)
dict_of_matrix = lukasiewicz_matrix_formation(array_of_operations, dict_of_predicates)
lukasiewicz_parcel(dict_of_matrix, parcel)