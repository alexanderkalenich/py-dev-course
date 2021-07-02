# -*- coding: utf-8 -*-
import datetime
import calendar
from collections import defaultdict
import re
import json

from generate_ticket import generate_ticket

re_name = re.compile(r'^[\w\-\s]{3,40}$')
re_email = re.compile(r"\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\b")
re_dep_city = re.compile(r"\b[Мм]оскв|[Лл]ондон|[Пп]ариж|[Ее]катеринбург|[Тт]оронто\b")
re_destination_city = re.compile(r"\b[Мм]оскв|[Лл]ондон|[Пп]ариж|[Ее]катеринбург|[Тт]оронто\b")
re_date = re.compile(r"([0-2]\d|3[0-1])(-)([0]\d|1[0-2])(-)([0-2]{4})")
re_confirm_list = re.compile(r"[Oo][Kk]|[Оо][Кк]")
re_flight_number = re.compile(r"[1-5]")
re_number_of_seats = re.compile(r"[1-5]")
re_confirmation = re.compile(r"([Дд][Аа])")
re_phone = re.compile(r"^\+?[78][-\(]?\d{3}\)?-?\d{3}-?\d{2}-?\d{2}$")

flight_direction = None
available_directions = None
incoming_date = None
schedule_weekday = {}
schedule_date = {}
day = None
month = None
year = None
user_choose = defaultdict()
dic_of_5 = {}


def directions():
    global available_directions
    with open('schedule.json', 'r', encoding='utf-8') as read_file:
        json_schedule = json.load(read_file)

        all_directions = {**json_schedule}
        all_directions_list = []
        for flight, date in all_directions.items():

            for direction, time in date.items():
                if flight == 'schedule_weekday':
                    schedule_weekday[direction] = time
                elif flight == 'schedule_date':
                    schedule_date[direction] = time
                all_directions_list.append(direction)

        all_directions_list = list(set(all_directions_list))
        available_directions = "; ".join(all_directions_list)


def handle_dep_city(text, context):
    match = re.match(re_dep_city, text)
    if match:
        context['dep_city'] = text.title()
        return True
    else:
        return False


def handle_destination_city(text, context):
    global flight_direction
    match = re.match(re_destination_city, text)
    if match:
        context['destination_city'] = text.title()
        flight_direction = f"{context['dep_city']} – {context['destination_city']}"
        if flight_direction in available_directions:
            return True
        else:
            return False
    else:
        return False


def handle_date(text, context):
    global day, month, year
    match = re.match(re_date, text)
    if match:
        context['date'] = text
        incoming_date_datetime = datetime.datetime.strptime(context['date'], '%d-%m-%Y')
        client_date = incoming_date_datetime.strftime('%Y-%m-%d')
        date_actual_date = str(datetime.date.today())
        if client_date >= date_actual_date:
            day = int(match[1])
            month = int(match[3])
            year = int(match[5])
            return True
        else:
            return False
    else:
        return False


def handle_list_of_flights(text, context):
    new_list = []
    match = re.match(re_confirm_list, text)
    if match:
        list_of_5 = start_search()
        for key, item in list_of_5.items():
            new_list.append("{}: {}".format(key, item))
        result = "; ".join(new_list)
        context['list_of_flights'] = result
    return True


def handle_flight_number(text, context):
    match = re.match(re_flight_number, text)
    if match:
        for number, flight in dic_of_5.items():
            if int(text) == int(number):
                context['flight_number'] = flight
                return True
    else:
        return False


def handle_number_of_seats(text, context):
    match = re.match(re_flight_number, text)
    if match:
        context['number_of_seats'] = text
        return True
    else:
        return False


def handle_comment(text, context):
    match = text
    if match:
        context['comment'] = text
        return True
    else:
        return True


def handle_confirmation(text, context):
    match = re.match(re_confirmation, text)
    if match:
        context['confirmation'] = text
        return True
    else:
        return False


def handle_phone(text, context):
    match = re.match(re_phone, text)
    if match:
        context['phone'] = text
        return True
    else:
        return False


def handle_name(text, context):
    match = re.match(re_name, text)
    if match:
        context['name'] = text
        return True
    else:
        return False


def handle_email(text, context):
    match = re.match(re_email, text)
    if match:
        context['email'] = text
        return True
    else:
        return False


def generate_ticket_handler(text, context):
    return generate_ticket(name=context['name'], email=context['email'], flight_number=context['flight_number'],
                           number_of_seats=context['number_of_seats'])


def f_day_iterator(year, month):
    calendar_text = calendar.TextCalendar()
    day_iterator = calendar_text.itermonthdays2(year, month)
    return day_iterator


def f_day_iterator2(year, month):
    calendar_text = calendar.TextCalendar()
    day_iterator = calendar_text.itermonthdays(year, month)
    return day_iterator


number_of_flights = 0
count = 1
list_of_user_flights = defaultdict()


def exceptions_check(number_of_flights, flight_direction):
    global day, month, year
    if number_of_flights < 5:
        if month < 12:
            month += 1
            search_flights(day, month, year, flight_direction)


def search_flights(day, month, year, flight_direction):
    global number_of_flights, count
    date_actual_datetime = datetime.datetime.now()
    if flight_direction in schedule_weekday:
        for direction, weekday in schedule_weekday.items():
            if flight_direction == direction:
                weekday, time = weekday[0], weekday[1]
                day_iterator = f_day_iterator(year, month)
                for flight in range(5):
                    users_weekday = weekday
                    for data, weekday in day_iterator:
                        if data >= day and weekday == users_weekday:
                            temp_datetime = datetime.datetime(year=year, month=month, day=data, hour=int(time[0:2]),
                                                              minute=int(time[3:5]))
                            if temp_datetime >= date_actual_datetime:
                                list_of_user_flights[count] = f' {direction}: {data}-{month}-{year} вылет {time}'
                                count += 1
                                number_of_flights += 1
        if number_of_flights < 5:
            exceptions_check(number_of_flights, flight_direction)

    elif flight_direction in schedule_date:
        for direction, day in schedule_date.items():
            if flight_direction == direction:
                day1, day2, time = day[0], day[1], day[-1]
                day_iterator = f_day_iterator2(year, month)
                for flight in range(5):
                    for data in day_iterator:
                        if day1 == data or day2 == data:
                            temp_datetime = datetime.datetime(year=year, month=month, day=data, hour=int(time[0:2]),
                                                              minute=int(time[3:5]))
                            if temp_datetime >= date_actual_datetime:
                                list_of_user_flights[count] = f' {direction}: {data}-{month}-{year} вылет {time}'
                                count += 1
                                number_of_flights += 1
        if number_of_flights < 5:
            exceptions_check(number_of_flights, flight_direction)
    else:
        print('В заданом направлении рейсов не найдено')


def start_search():
    search_flights(day, month, year, flight_direction)
    for number, flight in list_of_user_flights.items():
        if number > 5:
            break
        dic_of_5[number] = flight
    return dic_of_5
