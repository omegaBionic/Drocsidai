import requests

#api_key is available on your openweathermap's account
api_key = "01c55848d9929f0aa1271d79bc148a78"

#get all the data about the weather
def getWeatherall(city):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'.format(city,api_key)
    res = requests.get(url)
    data = res.json()
    return data

#get specific data : overall weather and temperature
def getWeather(city):
    data = getWeatherall(city)
    temp = data['main']['temp']
    main_weather = data['weather'][0]['main']
    weather = "City: {}\n\t\t{}\n\t\tTemperature : {}°C\n".format(city,main_weather,temp)
    return weather

if __name__ == '__main__':
    data = getWeather('Dijon')
    print(data)


