# # -*- coding: utf-8 -*-

import models

Weather = models.Weather


class DatabaseUpdater:

    def __init__(self, temperature, weather_type, weather_date, image_path):
        self.Weather = models.Weather
        self.temperature = temperature
        self.weather_type = weather_type
        self.weather_date = weather_date
        self.image_path = image_path
        self.Weather.create_table()

    @classmethod
    def check_date(cls, weather_date):
        """
        Проверка наличиязаписи в базе данных.
        """
        query = Weather.select().where(Weather.weather_date == weather_date)
        return query.exists()

    @classmethod
    def write(cls, temperature, weather_type, weather_date, image_path):
        """
        Сохранение прогноза в базу данных.
        """
        weather, created = Weather.get_or_create(weather_date=weather_date,
                                                 defaults={'temperature': temperature, 'weather_type': weather_type,
                                                           'image_path': image_path})
        if not created:
            query = Weather.update(temperature=temperature, weather_type=weather_type,
                                   image_path=image_path).where(Weather.id == weather.id)
            query.execute()

    @classmethod
    def read(cls, term):
        """
        Получение данных из базы данных.
        """
        check = DatabaseUpdater.check_date(term)
        if check:
            check_date = Weather.get(Weather.weather_date == term)
            return check_date
        else:
            return False
