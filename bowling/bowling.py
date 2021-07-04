from collections import defaultdict


def get_score(game_result, rules=None):
    try:
        check_initial(game_result)
    except ValueError as exc:
        raise exc

    global frames
    frames = 0
    total_score = 0
    dict_analized_res = defaultdict(int)
    for i, k in enumerate(zip(game_result.replace('X', 'X-')[0::2], game_result.replace('X', 'X-')[1::2]), start=1):
        dict_analized_res[i] = k

    for key, value in dict_analized_res.items():
        exceptions_check(value)
        if rules == 1:
            if 'X' in value:
                if frames >= 1:
                    if 'X' in dict_analized_res[key - 1]:
                        total_score += 20
                        if frames >= 2:
                            if 'X' in dict_analized_res[key - 2]:
                                total_score += 10
                    elif '/' in dict_analized_res[key - 1]:
                        total_score += 20
                    else:
                        total_score += 10
                else:
                    total_score += 10

            elif '/' in value:
                if frames >= 1:
                    if 'X' in dict_analized_res[key - 1]:
                        total_score += 20
                        if frames >= 2:
                            if 'X' in dict_analized_res[key - 2]:
                                total_score += int(value[0])
                    elif '/' in dict_analized_res[key - 1]:
                        total_score += 10 + int(value[0])
                        if frames >= 2:
                            if 'X' in dict_analized_res[key - 2]:
                                total_score += int(value[0])

                    else:
                        total_score += 10
                else:
                    total_score += 10

            elif value[0] == '-' and value[1] == '-' in value:
                total_score += 0
            elif value[0].isdigit() and value[1] == '-' in value:
                if frames >= 1:
                    if 'X' in dict_analized_res[key - 1]:
                        total_score += (int(value[0])) * 2
                        if frames >= 2:
                            if 'X' in dict_analized_res[key - 2]:
                                total_score += (int(value[0])) * 2
                                if 'X' in dict_analized_res[key - 1]:
                                    total_score += (int(value[0])) * 2
                                elif '/' in dict_analized_res[key - 1]:
                                    total_score += (int(value[0])) * 2
                            elif '/' in dict_analized_res[key - 1]:
                                total_score += (int(value[0])) * 2
                            else:
                                total_score += int(value[0])

                    elif '/' in dict_analized_res[key - 1]:
                        total_score += (int(value[0])) * 2
                        if frames >= 2:
                            if 'X' in dict_analized_res[key - 2]:
                                total_score += (int(value[0]))
                    else:
                        total_score += int(value[0])

                else:
                    total_score += int(value[0])



            elif value[1].isdigit() and value[0] == '-' in value:
                if frames >= 1:
                    if 'X' in dict_analized_res[key - 1]:
                        total_score += (int(value[1])) * 2

                    else:
                        total_score += int(value[1])

                else:
                    total_score += int(value[1])


            else:
                sum_int = int(value[0]) + int(value[1])
                if frames >= 1:
                    if 'X' in dict_analized_res[key - 1]:
                        total_score += sum_int * 2
                        if frames >= 2:
                            if 'X' in dict_analized_res[key - 2]:
                                total_score += int(value[0])

                    elif '/' in dict_analized_res[key - 1]:
                        total_score += sum_int + int(value[0])
                    else:
                        total_score += sum_int
                else:
                    total_score += sum_int
            frames += 1

        else:
            if 'X' in value:
                total_score += 20
            elif '/' in value:
                total_score += 15
            elif value[0] == '-' and value[1] == '-' in value:
                total_score += 0
            elif value[0].isdigit() and value[1] == '-' in value:
                total_score += int(value[0])
            elif value[1].isdigit() and value[0] == '-' in value:
                total_score += int(value[1])
            else:
                sum_int = int(value[0]) + int(value[1])
                total_score += sum_int
            frames += 1

    if frames != 10:
        raise ValueError('Количество фреймов не равно 10')

    # print(total_score)
    return total_score


def check_initial(game_result):
    global total_frames
    count_frames = 0
    count_pins = 0
    thrown_balls = 0
    pins_left = 100
    total_frames = []
    for frame in game_result:
        if frame == "X":
            count_frames += 1
            count_pins += 10
            total_frames += frame
            pins_left -= 10
        elif frame == "-":
            thrown_balls += 1
            count_pins += 0
            total_frames += frame
            pins_left -= 0
        elif frame == "/":
            total_frames += frame
            thrown_balls += 1
            count_pins += 10
            pins_left -= 10
        elif frame.isdigit():
            if int(frame) == 0:
                raise ValueError('Неверное значение "0"')
            elif int(frame) <= 9:
                total_frames += frame
                thrown_balls += 1
                pins_left -= int(frame)
            else:
                raise ValueError('Ошибка! Значение не может быть больше "9"')
    for value in total_frames:
        if value.isdigit():
            count_pins += int(value)
    total_frames_count = count_frames + (thrown_balls / 2)
    if total_frames_count == 10:
        if pins_left != 100 - count_pins:
            raise ValueError('Ошибка: вводные данные не корректны. Количество кеглей не совпадает')

    else:
        raise ValueError('Ошибка: вводные данные не корректны. Количество фреймов не равно 10')


def exceptions_check(value):
    if value == 'X':
        raise ValueError('Ошибка! Страйк не может быть на втором броске!')
    elif value[0].isdigit() and value[1].isdigit() and int(value[0]) + int(value[1]) >= 10:
        raise ValueError('Ошибка! Значение не может быть больше "9"')
    elif '0' in value:
        raise ValueError('Неверное значение "0"')
    elif '/' in value[0]:
        raise ValueError('Спэа на первом броске')

# if __name__ == '__main__':
#     # input = "1/2/3/4/5/6/7/8/9/X" # 154
#     # input = "XXXXXXXXXX" # 270
#     # input = "XXXXXXXX2/62" # 234
#     input = "-263X815/5/27-----6"  # 81
#     # input = "XXX5/34XXXXX" # 215
#     # input = "5/43X211744XX-/--"
#     # input = "43X-/211744XX32--"
#     get_score(input, rules=0)
