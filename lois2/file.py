# Лабораторная работа 2 по предмету "Логические основы интеллектуальных систем"
# Вариант 8: Запрограммировать обратный нечеткий логический вывод на основе операции нечеткой композиции (max({max({0}U{xi+yi-1})|i})).
# Выполнили студенты группы 121701: Лемантович Д.К., Фурс Д.С,, Мулярчик Д.С.
# Дата выполнения: 27.12.2023
# Используемые источники: Теория в системе.

import re

NOT_CORRECT_RULE_INPUT = "Неверный ввод правила!"
NOT_CORRECT_CONSEQUENT_INPUT = "Неверный ввод консеквента!"
NOT_CORRECT_FILE = "Некорректный файл!"
NOT_NUMERIC = "Введите численное значение!"
NOT_LIMITED = "Переменные множества должны лежать в промежутке [0, 1]!"


def read_file(filename):
    with open(filename, "r") as file:
        text = file.read()

        text = re.findall(r'= *{[^{}]*}\n', text)

        if len(text) > 2:
            return NOT_CORRECT_FILE

        line = text[0]
        for i in ["=", "\n", "{", "}", " "]:
            line = line.replace(i, "")
        consequent = process_consequent(line)

        line = text[1]
        for i in ["=", "\n", "{", "}", " "]:
            line = line.replace(i, "")
        rule = process_rule(line)

        return rule, consequent


def process_consequent(text):
    consequent = dict()
    line = re.findall(r'<[^<>]*>', text)
    value = re.sub(r'<[^<>]*>', "value", text).replace(",", "")
    if re.fullmatch(r'(value)*', value):
        line = [item.replace("<", "").replace(">", "").replace("value", "") for item in line]
        for l in line:
            item_1, item_2 = l.split(",")
            if "-" in item_2:
                return NOT_CORRECT_CONSEQUENT_INPUT
            if item_1 in consequent:
                return NOT_CORRECT_CONSEQUENT_INPUT
            try:
                item_2 = float(item_2)
            except (Exception, ):
                return NOT_NUMERIC
            if not 0 <= item_2 <= 1:
                return NOT_LIMITED
            consequent[item_1] = item_2
        return consequent
    else:
        return NOT_CORRECT_CONSEQUENT_INPUT


def process_rule(text):
    rule = dict()
    # убираем внутренние кавычки
    line_1 = re.findall(r'<[^<>]*>', text)
    value_1 = re.sub(r'<[^<>]*>', "value", text)
    # убираем внешние кавычки
    line_2 = re.findall(r'<[^<>]*>', value_1)
    value_2 = re.sub(r'<[^<>]*>', "value", value_1).replace(",", "")

    if re.fullmatch(r'(value)*', value_2):
        line_2 = [item.replace("<", "").replace(">", "").replace("value", "").replace(",", "") for item in line_2]
        for i in range(len(line_1)):
            value_1, value_2 = line_1[i].replace("<", "").replace(">", "").split(",")
            if "-" in line_2[i]:
                return NOT_CORRECT_RULE_INPUT
            if (value_1, value_2) in rule:
                return NOT_CORRECT_CONSEQUENT_INPUT
            try:
                line_2[i] = float(line_2[i])
            except (Exception, ):
                return NOT_NUMERIC
            if not 0 <= line_2[i] <= 1:
                return NOT_LIMITED
            rule[(value_1, value_2)] = line_2[i]
        return rule
    else:
        return NOT_CORRECT_RULE_INPUT


def check_len(consequent, rule):
    result = {key: list() for key in consequent.keys()}
    for consequent_key in consequent.keys():
        for value_1, value_2 in rule.keys():
            if value_2 == consequent_key:
                result[consequent_key].append(value_1)
    previous = -1
    result = list(result.values())
    for i in range(len(result)):
        if result[previous] != result[i]:
            raise Exception


def correct_output(rules):
    result = list()
    for rule in rules:
        if None not in rule.values():
            for key, value in rule.items():
                if value[0] == value[1]:
                    rule.update({key: value[0]})
            if rule not in result:
                result.append(rule)
    if len(result) == 0:
        return "Нет решений"

    return result