# -*- coding: utf-8 -*-

"""
Условия игры Dungeon:
Подземелье было выкопано ящеро-подобными монстрами рядом с аномальной рекой, постоянно выходящей из берегов.
Из-за этого подземелье регулярно затапливается, монстры выживают, но не герои, рискнувшие спуститься к ним в поисках
приключений.
Почуяв безнаказанность, ящеры начали совершать набеги на ближайшие деревни. На защиту всех деревень не хватило
солдат и вас, как известного в этих краях героя, наняли для их спасения.

Карта подземелья представляет собой json-файл под названием rpg.json. Каждая локация в лабиринте описывается объектом,
в котором находится единственный ключ с названием, соответствующем формату "Location_<N>_tm<T>",
где N - это номер локации (целое число), а T (вещественное число) - это время,
которое необходимо для перехода в эту локацию. Например, если игрок заходит в локацию "Location_8_tm30000",
то он тратит на это 30000 секунд.
По данному ключу находится список, который содержит в себе строки с описанием монстров а также другие локации.
Описание монстра представляет собой строку в формате "Mob_exp<K>_tm<M>", где K (целое число) - это количество опыта,
которое получает игрок, уничтожив данного монстра, а M (вещественное число) - это время,
которое потратит игрок для уничтожения данного монстра.
Например, уничтожив монстра "Boss_exp10_tm20", игрок потратит 20 секунд и получит 10 единиц опыта.
Гарантируется, что в начале пути будет две локации и один монстр
(то есть в коренном json-объекте содержится список, содержащий два json-объекта, одного монстра и ничего больше).

На прохождение игры игроку дается 123456.0987654321 секунд.
Цель игры: за отведенное время найти выход ("Hatch")

По мере прохождения вглубь подземелья, оно начинает затапливаться, поэтому
в каждую локацию можно попасть только один раз,
и выйти из нее нельзя (то есть двигаться можно только вперед).

Чтобы открыть люк ("Hatch") и выбраться через него на поверхность, нужно иметь не менее 280 очков опыта.
Если до открытия люка время заканчивается - герой задыхается и умирает, воскрешаясь перед входом в подземелье,
готовый к следующей попытке (игра начинается заново). Выход только один.
"""

import csv
import json
import re
from decimal import Decimal
import datetime
import logging


class Dungeon:

    def __init__(self):
        self.locations_list = []
        self.mob_list = []

        self.location_choose = []

        self.loc_list_new = []

        self.re_hatch = r'Hatch'
        self.re_exp_time = r'\s*(exp)(\d+)(_tm)(\d+\.\d+|\d+)|(_tm)(\d+\.\d+|\d+)\s*'

        self.current_experience = 0
        self.remaining_time = rem_time

        self.rem_time = remaining_time_dec
        self.current_location = None

    logging.basicConfig(level=logging.INFO, filename='game.log')

    def reg_check(self, location_choose):

        matched = re.search(self.re_exp_time, str(location_choose))

        tm = Decimal(matched[6])

        self.rem_time = self.rem_time - tm

        return rem_time

    def attack_mob(self, current_mob):

        count = 1
        print(f'Вы выбрали сражаться с монстром')
        mob_list_temp = []

        if current_mob:
            for mob in current_mob:
                print(f'{count}. {mob}')
                count += 1
        else:
            print('############################')
            print('Отсюда нет выхода! Прощайте!')
            print('############################')
            self.start_new_game()
        mob_choose = input(f'- Выберите монстра для сражения: ')

        if mob_choose.isalpha() or mob_choose == '' or int(mob_choose) not in range(1, count + 1):
            self.attack_mob(current_mob)
        else:
            mob_choose = int(mob_choose) - 1
            mob_fight = current_mob[mob_choose]
            mob_list_temp.append(mob_fight)
            matched = re.search(self.re_exp_time, str(mob_fight))
            tm = int(matched[4])
            self.current_experience += int(matched[2])

            self.rem_time = self.rem_time - tm
            time_passed = self.time()
            logging.info(f'{self.current_location}, {self.current_experience}, {time_passed}')

        if rem_time <= 0.0:
            print('У Вас закончилось время')
            self.start_new_game()
        else:

            print(f'Вы успешно победили монстра. {mob_list_temp[0]}')
            print('* * * * *')
            if len(current_mob) > 1:
                print(f'У вас {self.current_experience} опыта')
                print('В этой локации есть еще монстры')
                current_mob.remove(mob_list_temp[0])
                other_mob = current_mob

                count = 1
                for mob in other_mob:
                    print(f'{count}. {mob}')
                    count += 1
                next_step = input('Чтобы сразиться с монстром, введите "1". Для перехода в локацию - "2": ')

                if next_step == "1":
                    self.attack_mob(other_mob)
                else:
                    self.choose_action(current_mob, rem_time)

            else:
                current_mob.clear()
                self.choose_action(current_mob, rem_time)

    def game_over(self):

        print('****************************')
        print('******* Прощайте! **********')
        print('****************************')

        self.write_scv()
        return

    def start_new_game(self):

        print('****************************')
        print('И снова здравствуйте!')
        print('****************************')

        self.write_scv()
        self.current_experience = 0
        self.rem_time = remaining_time_dec
        self.proccess(loaded_json_file, remaining_time_dec)

    def write_scv(self):
        game_log_list = []
        field_names = ['current_location', 'current_experience', 'current_date']

        with open('game.log', 'r', newline='') as infile, open('game_log.csv', 'a', newline='') as outfile:
            csv_data = csv.reader(infile)
            for row in csv_data:
                game_log_list.append(row)
            writer = csv.writer(outfile)
            writer.writerow(field_names)
            for line in game_log_list:
                writer.writerow(line)

    def choose_location_f(self, count):
        number = input(f'Для выбора локации введите ее номер от 1 до {count}:  ')

        if number.isalpha() or number == '' or int(number) not in range(1, count + 1):
            self.choose_location_f(count)
        else:
            current_loc = int(number) - 1

            self.rem_time = self.reg_check(location_choose=self.location_choose[current_loc])

            self.location_choose.clear()
            self.mob_list.clear()
            self.loc_list = self.loc_list_new[current_loc]
            self.proccess(loc_list=self.loc_list, rem_time=rem_time)

    def proccess(self, loc_list, rem_time):
        self.location_choose.clear()
        self.mob_list.clear()
        self.loc_list_new.clear()

        for location_key, value_in_loclist in loc_list.items():

            if isinstance(value_in_loclist, list):
                for value_loc_or_mob in value_in_loclist:

                    if isinstance(value_loc_or_mob, dict):
                        self.loc_list_new.append(value_loc_or_mob)
                        for loc_to_append in value_loc_or_mob:
                            self.location_choose.append(loc_to_append)
                    else:
                        self.mob_list.append(value_loc_or_mob)
            current_location = location_key
            print('------------------------------------------------')
            print(f'Вы находитесь в {current_location}')

            time_passed = self.time()
            logging.info(f'{current_location}, {self.current_experience}, {time_passed}')
        current_mob = self.mob_list
        self.choose_action(current_mob, rem_time)

    def choose_action(self, current_mob, rem_time):
        count = 0
        time_passed = self.time()

        print(f'У вас {self.current_experience} опыта и осталось {rem_time} секунд до наводнения')
        print(f"Прошло времени: {time_passed}")
        print(f'Внутри вы видите:')
        for mob in current_mob:
            print(f'- Монстра: {mob}')
        matched = re.search(self.re_hatch, str(self.location_choose))
        for i in self.location_choose:
            if matched:
                print(f'— Открыть люк и выбраться через него на поверхность: {i}')
                count += 1
            elif i:
                print(f'— Вход в локацию: {i}')
                count += 1

        print(f'Выберите действие:')
        if current_mob:
            print(f'1.Атаковать монстра')
        print(f'2.Сдаться и выйти из игры')

        if count > 0:
            print(f'3.Перейти в другую локацию')

        elif matched:
            print(f'— 3.Открыть люк и выбраться через него на поверхность: {self.re_hatch}')
        else:
            print('############################')
            print('Отсюда нет выхода! Прощайте!')
            print('############################')

            self.start_new_game()

        user_choose = input(f'Введите цифру, соответствующую Вашему выбору: ')

        if user_choose == '1':
            if current_mob:
                self.attack_mob(current_mob)
            else:
                self.choose_action(current_mob, rem_time)

        elif user_choose == '2':
            self.game_over()

        elif user_choose == '3':
            if matched:
                if self.current_experience >= 280:
                    self.rem_time = self.reg_check(location_choose=self.location_choose)
                    if rem_time > 0:
                        print('###################')
                        print('«Ура! Вы выиграли!»')
                        print('###################')
                        game_continue = input('Если хотите сыграть еще раз, нажмите 1. Если нет 2: ')
                        if game_continue == '1':
                            self.write_scv()
                            self.start_new_game()
                        else:
                            self.write_scv()
                            self.game_over()
                    else:
                        self.game_over()
                else:
                    print(f'У Вас недостаточно опыта {self.current_experience}. Требуется опыт 280 очков')
                    self.attack_mob(current_mob)
            else:
                self.choose_location_f(count)

        else:
            self.choose_action(current_mob, rem_time)

    def time(self):
        time_now = datetime.datetime.today().strftime("%M:%S")
        format = "%M:%S"
        time_passed = datetime.datetime.strptime(time_now, format) - datetime.datetime.strptime(time_start, format)
        return time_passed


if __name__ == '__main__':
    remaining_time = '123456.0987654321'
    remaining_time_dec = Decimal(remaining_time)
    rem_time = remaining_time_dec

    with open('rpg.json', 'r') as read_file:
        loaded_json_file = json.load(read_file)
        loc_list = loaded_json_file
        time_start = datetime.datetime.today().strftime("%M:%S")

        dungeon = Dungeon()
        proccess = dungeon.proccess(loc_list, rem_time)
