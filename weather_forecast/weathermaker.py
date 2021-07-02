# -*- coding: utf-8 -*-
import cv2
import lxml.html
import requests
import datetime
import re
import databaseupdater
import imagemaker

re_date = re.compile(r"([0-2]{4})(-)([0]\d|1[0-2])(-)([0-2]\d|3[0-1])")

date = datetime.date.today()

"""
Модуль-движок с классом WeatherMaker и GetForecast, необходимыми для получения и формирования предсказаний погоды.
"""


class WeatherMaker:
    """
    Парсинг прогноза с сайта погоды и запись в БД.
    """

    @classmethod
    def last_week(cls, date, n):
        for _ in range(n):
            weather_dict = {}
            current_date = requests.get(f'https://darksky.net/details/55.7616,37.6095/{date}/si12/en')
            html_tree = lxml.html.document_fromstring(current_date.text.encode("utf-8"))
            list_of_temp = html_tree.xpath('//*[@class="num"]')
            list_of_weather = html_tree.xpath('//*[@id="summary"]')
            weather = list_of_weather[0].text
            if 'cloudy' in weather:
                weather = 'облачно'
            elif 'rain' or 'Rain' in weather:
                weather = 'дождь'
            elif 'sun' in weather:
                weather = 'солнечно'
            elif 'snow' in weather:
                weather = 'снег'
            elif 'Clear' in weather:
                weather = 'ясно'

            weather_dict[date] = f'Температура: {list_of_temp[0].text}, погода: {weather}'

            image = imagemaker.ImageMaker(date)
            image_path = image.picture(weather_dict[date], logo=weather)

            temperature = list_of_temp[0].text

            weather_type = weather
            weather_date = date
            databaseupdater.DatabaseUpdater.write(temperature=temperature, weather_type=weather_type,
                                                  weather_date=weather_date, image_path=image_path)
            date_previous = date - datetime.timedelta(days=1)
            date = date_previous


class GetForecast:
    """
    Формирование погоды по дням из БД.
    """

    @classmethod
    def handle_date(cls, text):
        re_date = re.compile(r"([0-2]{4})(-)([0]\d|1[0-2])(-)([0-2]\d|3[0-1])")
        match = re.match(re_date, text)
        if match:
            year = int(match[1])
            month = int(match[3])
            day = int(match[5])
            selected_date = datetime.date(year=year, month=month, day=day)

            return selected_date
        else:
            print('Дата введена неверно. Попробуйте еще раз')
            return False

    @classmethod
    def viewImage(cls, image, name_of_window):
        image = cv2.imread(f'{image}')
        cv2.imshow(str(name_of_window), image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def selected_period_output(self, input_from, input_to):
        term = input_to
        while True:
            check_date = databaseupdater.DatabaseUpdater.check_date(term)
            if check_date:
                check_date = databaseupdater.DatabaseUpdater.read(term)
                image_cv2 = cv2.imread(f'{check_date.image_path}')
                print(f'{check_date.weather_date} Температура: {check_date.temperature}, '
                      f'погода: {check_date.weather_type}')
                self.viewImage(image_cv2, term)
            else:
                weathermaker = WeatherMaker()
                weathermaker.last_week(term, n=1)
            term = term - datetime.timedelta(days=1)
            if term < input_from:
                break

    def selected_period(self, selected_date_from, selected_date_to):
        input_from = datetime.date.strftime(selected_date_from, '%Y-%m-%d')
        input_to = datetime.date.strftime(selected_date_to, '%Y-%m-%d')
        print(f'Выбранный период: с {input_from} по {input_to}')
        self.selected_period_output(selected_date_from, selected_date_to)

    def input_to_date(self, selected_date_from):
        input_to = input(f'Введите вторую дату диапаза в следующем формате: "2021-06-20" ')
        selected_date_to = self.handle_date(input_to)
        if selected_date_to:
            self.selected_period(selected_date_from, selected_date_to)
        else:
            self.input_to_date(selected_date_from)

    def input_from_date(self):
        input_from = input(
            f'Введите первое значение диапаза дат в следующем формате: "2021-06-27", enter, "2021-06-28" ')
        selected_date_from = self.handle_date(input_from)
        if selected_date_from:
            self.input_to_date(selected_date_from)
        else:
            self.input_from_date()


if __name__ == '__main__':
    weathermaker = WeatherMaker()
    weathermaker.last_week(date, n=2)
    getforecast = GetForecast()
    getforecast.input_from_date()
