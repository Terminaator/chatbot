import requests

from oisbotServer.views.weather import weatherConditions as wc
import datetime


def parseJson(when, json):
    """
    Parses the provided json
    :param when: specifies the date
    :param json: provided json
    :return: returns bots answer
    """
    tempAvg = float(json.get('main').get('temp')) - 273.15
    desc = str(json.get('weather')[0].get('description')).replace(" ", "")
    wind = str(json.get('wind').get('speed')) + "m/s"
    tolge = wc.weatherConditions
    descEE = tolge.__getattribute__(tolge, desc)

    return when.capitalize() + " lubab: " + descEE + ". Temperatuur keskmiselt: " + str(
        tempAvg) + "." + " Tuule kiirus: " + wind


def getTodaysWeather():
    """
    Makes API call to OpenWeatherMap to get todays weather information.
    :return:  Returns answer for todays weather
    """
    request = requests.post(
        "http://api.openweathermap.org/data/2.5/weather?q=Tartu,ee&APPID=35e2b07a41ebe595eb82843ac306167e")
    status_code = request.status_code
    if status_code == 200:
        json = request.json()
        return parseJson("täna", json)
    else:
        raise Exception(status_code)


def getWeather(when):
    """
    Makes API call to OpenWeatherMap to get weather information
    :param when: the specification of the date
    :return: returns bots answer
    """
    if when == "täna":
        return getTodaysWeather()
    else:
        request = requests.post(
            "http://api.openweathermap.org/data/2.5/forecast?id=7522434&APPID=35e2b07a41ebe595eb82843ac306167e")
        status_code = request.status_code
        if status_code == 200:
            json = request.json()
            listof = json.get('list')
            if when == "homme" or when == "homne":
                tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
            elif when == "ülehomme" or when == "ülehomne":
                tomorrow = datetime.datetime.now() + datetime.timedelta(days=2)
            else:
                return "Ma ei tea, mis meid " + when + " ootab"
            print(tomorrow.day)
            for i in listof:
                datetimetom = datetime.datetime.strptime(i.get("dt_txt"), '%Y-%m-%d %H:%M:%S')
                if datetimetom.day == tomorrow.day and datetimetom.hour == 12:
                    return parseJson(when, i)
        else:
            raise Exception(status_code)
