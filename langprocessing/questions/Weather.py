from langprocessing.wordTags import WordTag as wt
import oisbotServer.views.weather.weather as weather


class Weather:

    def canAnswer(self, layer):
        return layer[wt.weather] != ""

    def answer(self, layer):
        if layer[wt.when] != "":
            return weather.getWeather(layer[wt.when])
        return weather.getTodaysWeather()
