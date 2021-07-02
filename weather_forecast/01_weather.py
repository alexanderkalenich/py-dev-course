# -*- coding: utf-8 -*-

import argparse
import datetime

from weathermaker import WeatherMaker, GetForecast
from databaseupdater import DatabaseUpdater

date = datetime.date.today()
next_week = date + datetime.timedelta(days=7)
for _ in range(7):
    WeatherMaker.last_week(next_week, n=1)
    check_date = DatabaseUpdater.read(next_week)
    print(f'{check_date.weather_date} Температура: {check_date.temperature}, '
          f'погода: {check_date.weather_type}')
    next_week = next_week - datetime.timedelta(days=1)


parser = argparse.ArgumentParser(description='Прогноз погоды за период')
parser.add_argument('f', type=str, metavar='', help='1. Enter the date of the range START FROM in the following format '
                                                    '"2021-07-01", then press SPACE. '
                                                    'The complete request is as follows: "2021-07-01 2021-07-02",'
                                                    'then press ENTER. You can also use optional args described below. '
                                                    'E.g.: To create a card with weather forecast for each day from '
                                                    'the indicated range, please write a request as follows:'
                                                    '"2021-07-01 2021-07-02 -c".')

parser.add_argument('t', type=str, metavar='', help='2. Enter the date of the range END TO in the following format '
                                                    '"2021-07-02", then press ENTER.')

group = parser.add_mutually_exclusive_group()
group.add_argument('-a', '--add', action='store_true', help='add forecast to DB')
group.add_argument('-g', '--get', action='store_true', help='get forecast from DB and print to console')
group.add_argument('-c', '--create', action='store_true', help='create cards from received dates range')

"""
Примеры запуска консольного скрипта:  python 01_weather.py 2021-07-01 2021-07-02 -a
                                      python 01_weather.py 2021-07-02 2021-07-03 -g
                                      python 01_weather.py 2021-07-02 2021-07-03 -a
                                      python 01_weather.py 2021-07-02 2021-07-03 -g
                                      python 01_weather.py 2021-07-02 2021-07-03 -c
"""


args = parser.parse_args()


def dates_range(date_from, date_to):
    text = date_to
    text = GetForecast.handle_date(text)
    date_from = GetForecast.handle_date(date_from)
    range = []

    while True:

        range.append(text)
        text = text - datetime.timedelta(days=1)
        if text < date_from:
            break
    return range


def add_to_db(range):
    weathermaker = WeatherMaker()
    for date in range:
        weathermaker.last_week(date, n=1)
        print(f'Запись {date} добавлена в БД')


def get_from_db(range):
    for date in range:
        check_date = DatabaseUpdater.read(date)
        if check_date:
            print(f'{check_date.weather_date} Температура: {check_date.temperature}, '
                  f'погода: {check_date.weather_type}')
        else:
            print(f'Запись за {date} отсутствует в БД')


def create_card(range):
    for date in range:
        check_date = DatabaseUpdater.read(date)
        if check_date:
            GetForecast.viewImage(check_date.image_path, date)
        else:
            print(f'Запись за {date} отсутствует в БД')


def show_in_console(range):
    get_from_db(range)


if __name__ == "__main__":
    range = dates_range(args.f, args.t)
    if args.add:
        add_to_db(range)
        print(f'Все записи за период с {range[-1]} по {range[0]} успешно добавлены.')
    elif args.get:
        get_from_db(range)

    elif args.create:
        create_card(range)

    else:
        show_in_console(range)