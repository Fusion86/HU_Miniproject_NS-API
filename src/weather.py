import config
import requests


def get_temperature(plaats):
    # GET request to openweathermap.org
    data = {"q": plaats, "appid": config.OPENWEATHERMAPP_APPID, "units": "metric"}
    res = requests.get("http://api.openweathermap.org/data/2.5/weather", params=data)
    data = res.json()

    # Round to 1 decimal
    return round(data["main"]["temp"], 1)
