
from Service.checks import alphabet_check, length_check, number_check

def input_reader():
    array_of_lines = []
    with open('Inputs/input.txt', 'r') as file:
        for line in file:
            array_of_lines.append(str(line.strip('\n')))

    return array_of_lines


def input_divider(array_of_input):
    A = {}
    B = {}
    x_y_array = ['x', 'y']

    array_of_conversed_inputs = string_conversion(array_of_input)

    A_array = array_of_conversed_inputs[0]
    B_array = array_of_conversed_inputs[1]

    array_of_A_B_numbers = [A_array, B_array]

    arrays = [A_array, B_array]
    for array in arrays:
        for index, element in enumerate(array):
            array[index] = str(element).strip(' ')

    alphabet_check(arrays)
    number_check(arrays)

    length = length_check(len(A_array), len(B_array))
    for letter in x_y_array:
        for index in range(0, length):
            if letter == x_y_array[0]:
                A[str(letter) + str(index)] = float(A_array[index])
            else:
                B[str(letter) + str(index)] = float(B_array[index])
    return A, B, array_of_A_B_numbers


def string_conversion(array_of_input):
    array_of_conversed_inputs = []
    for string in array_of_input:
        array = string.split(',')
        new_string = ''
        for element in array:
            if '>' in element:
                new_string += element
        new_array = new_string.split('>')[:-1]
        array_of_conversed_inputs.append(new_array)
    return array_of_conversed_inputs


def parcel_reader():
    array_of_lines = []
    with open('Inputs/parcel.txt', 'r') as file:
        for line in file:
            array_of_lines.append(str(line.strip('\n')))

    return array_of_lines


def lukasiewicz_matrix_formation(array_A, array_B):
    array_of_X_lines = []

    for element_A in array_A:
        X_line_array = []

        for element_B in array_B:
            result = min(1, 1 - float(element_A) + float(element_B))
            X_line_array.append(round(float(result), 1))

        array_of_X_lines.append(X_line_array)

    return array_of_X_lines


def matrix_formation(array_of_X_lines, tag):
    array_of_matrix_lines = []
    for line in array_of_X_lines:
        string = '|| ' + ' | '.join(str(number) for number in line) + ' ||'
        array_of_matrix_lines.append(string)

    print('\n')
    print(tag)
    print('=' * 27)
    for index, line in enumerate(array_of_matrix_lines):
        print(line)
        # if index != len(array_of_matrix_lines) - 1:
        # print('-' * 27)
    print('=' * 27)


def parcel_matrix_formation(parcel_line):
    print('\n')
    print('Матрица посылки С:')
    print('=' * 9)
    for element in parcel_line:
        print(f"|| {float(element)} ||")
    print('=' * 9)


def show_result(result):
    print("Импликация Лукасевича для A → B:")
    for x in result:
        print(f"{x}: {round(float(result[x]), 1)}")