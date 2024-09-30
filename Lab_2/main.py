# Лабораторная работа 2 по предмету "Логические основы интеллектуальных систем"
# Вариант 8: Запрограммировать обратный нечеткий логический вывод на основе операции нечеткой композиции (max({max({0}U{xi+yi-1})|i})).
# Выполнили студенты группы 121701: Лемантович Д.К., Фурс Д.С,, Мулярчик Д.С.
# Дата выполнения: 27.12.2023
# Используемые источники: Теория в системе.

from functions import *
from re import fullmatch
from itertools import product
import json



# b1: 0.5, b2: 0.6, b3: 0.2
# [[0.5,0.5],[0.6,0.7],[0.3,0.2]]

# b1: 0.6, b2: 0.7
# [[1,1,0.8],[1,1,0.9]]

# b1: 0.4, b2: 0.5, b3: 0.1
# [[0.6,0.7,0.5],[0.7,0.7,0.7],[0.5,0.7,0.2]]

# b1: 0.4, b2: 0.5, b3: 0.1
# [[0.6,0.6,0.5],[0.7,0.7,0.7],[0.3,0.3,0.2]]

# b1: 0.5, b2: 0.5, b3: 0.5, b4: 0.5
# [[0.5,0.5],[0.5,0.5],[0.5,0.5],[0.5, 0.5]]

if __name__ == '__main__':
    cycle = True
    while cycle:
        try:
            choice = int(input("Выберите номер следствия и отношения для нахождения обратного нечёткого логического вывода\n-1 для выхода \n--->"))
            start_consequence, start_relation = read_file(choice)
        except Exception as e:
            print(e)
            if str(e) == 'Выход из программы':
                cycle = False
        else:
            consequence = start_consequence.replace(" ", "").rstrip()
            if fullmatch(r'\w{1}\d{1}:(0.\d+|0|1)(,\w{1}\d{1}:(0.\d+|0|1))*', consequence):
                pass
            else:
                print(f"Неправильный формат ввода следствия в строке {(choice-1)*3+1}. Вывод невозможен.")
                continue
            relation = start_relation.replace(" ", "").rstrip()
            try:
                relation = json.loads(relation)
            except:
                print(f"Неправильный формат ввода отношения в строке {(choice-1)*3+2}. Вывод невозможен.")
                continue

            consequence = consequence_to_variables(consequence)
            if len(consequence) != len(relation):
                print("Невозможно построить матрицу. Вывод невозможен.")
                continue

            answer = reverse_fuzzy_conclusion([i[1] for i in consequence], relation)
            if answer:
                result = get_merged_answer(answer)
                if not result:
                    result = "Вывод невозможен."
            else:
                result = "Вывод невозможен."
            print(f"Ответ: {result}")
            write_file(start_consequence.rstrip(), start_relation.rstrip(), result)
