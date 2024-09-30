# Лабораторная работа 2 по предмету "Логические основы интеллектуальных систем"
# Вариант 8: Запрограммировать обратный нечеткий логический вывод на основе операции нечеткой композиции (max({max({0}U{xi+yi-1})|i})).
# Выполнили студенты группы 121701: Лемантович Д.К., Фурс Д.С,, Мулярчик Д.С.
# Дата выполнения: 27.12.2023
# Используемые источники: Теория в системе.


from itertools import product


def find_intersection(interval1, interval2):
    if not interval1 or not interval2:
        return None
    start1, end1 = interval1
    start2, end2 = interval2
    intersection_start = max(start1, start2)
    intersection_end = min(end1, end2)
    if intersection_start <= intersection_end:
        return intersection_start, intersection_end
    else:
        return None


def test(y, p):
    result = []
    for key, element in y.items():
        # список иксов, которые относятся к данному игрику
        related_values = []
        for key_b, element_b in p.items():
            # если игрек есть в тупле отношения с икс, то добавляем в список
            if key in key_b:
                related_values.append({key_b[0]: element_b})
        result.append(fix_interval(max_reverse(element, related_values)))
    return define_intersection(result)


def define_intersection(values):
    result = []
    for intersection in pairwise_combinations(values):
        if len(intersection) == 1:
            result.append(intersection)
            continue
        result_of_intersection = {}
        for index in range(1, len(intersection)):
            if index == 1:
                for key in intersection[index]:
                    result_of_intersection.update({key: find_intersection(intersection[index - 1][key],
                                                                          intersection[index][key])})
            else:
                for key in result_of_intersection:
                    intersection_value = find_intersection(result_of_intersection[key],
                                                           intersection[index][key])
                    if intersection_value:
                        result_of_intersection.update({key: intersection_value})
        # print("Промежутки: ", intersection)
        # print("Результат пересечения: ", result_of_intersection)
        result.append(result_of_intersection)
    return result


def pairwise_combinations(list_of_lists):
    # Получаем попарные комбинации элементов
    combinations = list(product(*list_of_lists))
    return combinations


def max_reverse_equal(vp, vy):
    if vy == 0:
        return 0, round(1-vp)
    else:
        return round(1 + vy - vp, 2), round(1 + vy - vp, 2)


def max_reverse_less(vp, vy):
    if vy == 0:
        return 0, round(1-vp)
    else:
        return 0, round(1 + vy - vp, 2)


def fix_interval(interval_list: list):
    result = []
    for interval_value in interval_list:
        interval_dict = {}
        for key, value in interval_value.items():
            interval_dict.update({key: find_intersection(value, (0, 1))})
        result.append(interval_dict)
    return result


def check_interval(interval):
    if interval[0] < 0:
        interval[0] = 0
    if interval[1] > 1:
        interval[1] = 1.0
    return interval


def max_reverse(result: float, related_list: list):
    interval_list = []
    for equal_item in related_list:
        one_case_dict = {}
        for item in related_list:
            if item == equal_item:
                one_case_dict.update({list(item.items())[0][0]: max_reverse_equal(list(item.items())[0][1], result)})
                continue
            one_case_dict.update({list(item.items())[0][0]: max_reverse_less(list(item.items())[0][1], result)})
        interval_list.append(one_case_dict)
    return interval_list