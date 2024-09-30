# Лабораторная работа 2 по предмету "Логические основы интеллектуальных систем"
# Вариант 8: Запрограммировать обратный нечеткий логический вывод на основе операции нечеткой композиции (max({max({0}U{xi+yi-1})|i})).
# Выполнили студенты группы 121701: Лемантович Д.К., Фурс Д.С,, Мулярчик Д.С.
# Дата выполнения: 27.12.2023
# Используемые источники: Теория в системе.

from file import read_file, check_len, correct_output
from functions import test
import os

NOT_CORRECT_INPUT = "Неверный ввод!"


def menu():
    while True:
        names = os.listdir('examples')
        print("Выберите файл, содержащий консеквент и правило:")
        [print(f"{num}) {name}") for num, name in enumerate(names, 1)]
        print("Введите 0 для выхода")
        case = input('')
        if case == "0":
            break
        elif "-" in case:
            print(NOT_CORRECT_INPUT)
        else:
            try:
                rule, consequent = read_file("examples\\" + str(names[int(case)-1]))
                check_len(consequent, rule)
                print("-" * 200)
                # print(test(consequent, rule))
                print("Результат: ", correct_output(test(consequent, rule)))
                print("-" * 200)
            except (Exception, ):
                print(NOT_CORRECT_INPUT)


if __name__ == "__main__":
    menu()
