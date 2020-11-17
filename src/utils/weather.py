import os
from datetime import datetime

import discord
import requests
from dotenv import load_dotenv
from geopy.geocoders import Nominatim


class WeatherOneDay:
    def __init__(self, date, temp_min, temp_max, description, icon_code):
        self.date = datetime.utcfromtimestamp(int(date)).strftime('%d-%m')
        full_date = datetime.utcfromtimestamp(int(date)).strftime('%d-%m-%Y')
        days = ["Lundi", "Mardi", "Mercredi", "Jeudi",
                "Vendredi", "Samedi", "Dimanche"]
        self.day = days[datetime.strptime(full_date, '%d-%m-%Y').weekday()]
        self.temp_min = round(temp_min, 1)
        self.temp_max = round(temp_max, 1)
        self.description = description.capitalize()
        self.icon_code = icon_code


class Weather:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('API_KEY_OPENWEATHERMAP')

    def getCoordinatesCity(self, city_name):
        geolocator = Nominatim(user_agent="any_value")
        location = geolocator.geocode(city_name)
        return location.latitude, location.longitude

    def getWeatherDataJSON(self, city_name):
        (lati, long) = self.getCoordinatesCity(city_name)
        url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=minutely,hourly,alerts' \
              '&appid={}&units=metric&lang=fr'.format(lati, long, self.api_key)
        res = requests.get(url)
        data = res.json()
        return data

    def getWeatherData(self, city_name):
        data = self.getWeatherDataJSON(city_name)
        weather_data = []
        for data_day in data['daily']:
            date = data_day['dt']
            temp_min = data_day['temp']['min']
            temp_max = data_day['temp']['max']
            description = data_day['weather'][0]['description']
            icon_code = data_day['weather'][0]['icon']
            weather_data.append(WeatherOneDay(date, temp_min, temp_max, description, icon_code))
        return weather_data

    def weatherEmbed(self, city_name):
        weather_data = self.getWeatherData(city_name)
        embed = discord.Embed()
        embed.title = " ".join(city_name.split('+')).title()
        # getting icon corresponding to the current weather
        data = self.getWeatherDataJSON(city_name)
        icon_code = data['current']['weather'][0]['icon']
        embed.set_thumbnail(url=f'http://openweathermap.org/img/wn/{icon_code}.png')
        embed.color = 2246304
        embed.add_field(name='Date', value=f"Aujourd'hui:\n{weather_data[0].day} {weather_data[0].date}", inline=True)
        embed.add_field(name='Description', value=weather_data[0].description, inline=True)
        embed.add_field(name='Température', value=f'{weather_data[0].temp_min}°C -'
                                                  f' {weather_data[0].temp_max}°C', inline=True)
        for weather_data_unit in weather_data[1:]:
            embed.add_field(name='᲼᲼᲼᲼᲼᲼', value=f'{weather_data_unit.day} {weather_data_unit.date}', inline=True)
            embed.add_field(name='᲼᲼᲼᲼᲼᲼', value=weather_data_unit.description, inline=True)
            embed.add_field(name='᲼᲼᲼᲼᲼᲼', value=f'{weather_data_unit.temp_min}°C -'
                                                 f' {weather_data_unit.temp_max}°C', inline=True)
        return embed
