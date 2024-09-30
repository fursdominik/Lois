"""
Лабораторная работа №4 по дисциплине "Логические основы интеллектуальных систем"
Выполнили студенты группы 121701: Лемантович Д.К., Фурс Д.С,, Мулярчик Д.С.
Файл содержит пример реализации алгоритма импликации Лукасевича
Дата: 25.09.2023
17.12.2023 - добавлен функционал, отвечающий за вывод только новых множеств
"""
from main_functions import *

def main ():
    premise_to_rule_list = []
    external_counter = 0
    input_information_dict, input_values_dict = input_transformation()
    #print(input_information_dict)
    #print(input_values_dict)
    premise_information_dict, premise_values_dict, premises = premise_transformation(external_counter)
    array_of_operations = operation_reader()
    #print(array_of_operations)
    matrix_dict = lukasiewicz_matrix_formation(input_information_dict, array_of_operations)
    #print(matrix_dict)

    new_matrix_dict, premise_to_rule_list = t_norm(input_information_dict, input_values_dict, matrix_dict, premise_information_dict, premise_values_dict, premise_to_rule_list)

    result = strait_output(new_matrix_dict, input_information_dict, input_values_dict, premise_information_dict, external_counter, premise_to_rule_list, premises)

    while result>0:
        external_counter+=1
        premise_information_dict, premise_values_dict, premises = premise_transformation(external_counter)
        new_matrix_dict, premise_to_rule_list = t_norm(input_information_dict, input_values_dict, matrix_dict,
                                                      premise_information_dict, premise_values_dict,
                                                      premise_to_rule_list)
        result = strait_output(new_matrix_dict, input_information_dict, input_values_dict, premise_information_dict, external_counter, premise_to_rule_list, premises)

if __name__ == "__main__":
    main()
