# # -*- coding: utf-8 -*-


import peewee

db = peewee.SqliteDatabase('weather.db')


class BaseTable(peewee.Model):
    class Meta:
        database = db


class Weather(BaseTable):
    temperature = peewee.CharField(2)
    weather_type = peewee.CharField(10)
    weather_date = peewee.CharField(10)
    image_path = peewee.CharField()


db.create_tables([Weather])
