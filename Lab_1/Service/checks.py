import sys


def alphabet_check(arrays):
    array_of_alphabet = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']
    for array in arrays:
        for element in array:
            for sign in str(element):
                if sign not in array_of_alphabet:
                    print(f"Ошибка. Символ '{sign}' элемента '{element}' не принадлежит заданному алфавиту {array_of_alphabet}.")
                    sys.exit()


def length_check(length_A, length_B):
    if length_A == length_B:
        return length_A

    else:
        print("Ошибка. Количество переменных разное.")
        sys.exit()


def number_check(arrays):
    for array in arrays:
        for element in array:
            if float(element) < 0 or float(element) > 1:
                print(f"Ошибка. Элемент '{element}' не принадлежит отрезку [0,1].")
                sys.exit()

