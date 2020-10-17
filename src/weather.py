from pyowm.owm import OWM
from pyowm.utils import timestamps, formatting

#api_key is available on your openweathermap's account
api_key = "01c55848d9929f0aa1271d79bc148a78"

owm = OWM(api_key)

mgr = owm.weather_manager()
three_h_forecaster = mgr.forecast_at_place('Dijon,FR', '3h')
for i in range(0, 24, 3):
    tomorrow_at_five = timestamps.tomorrow(i, 0)
    weather = three_h_forecaster.get_weather_at(tomorrow_at_five)
    print(weather)


