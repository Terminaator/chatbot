from langprocessing.Chatbot import chatbot
from unittest import TestCase
from unittest.mock import Mock
from oisbotServer.views.ois import misc
import oisbotServer.views.weather.weather as weather


class TestUsingMock(TestCase):
    # This class test questions with a bit random results or just if method call needs to be checked

    def testWeather(self):
        cb = chatbot()
        w = weather
        w.getTodaysWeather = Mock()
        w.getTodaysWeather.return_value = "ehh ilma kutsuti"
        res = cb.getResponse("ilm")
        self.assertEqual({"answer": "ehh ilma kutsuti"}, res)
        w.getTodaysWeather.assert_called_once()

    def testRandomPosts(self):
        cb = chatbot()
        m = misc
        m.getRandomPost = Mock()
        m.getRandomXkcd = Mock()
        data = [{"data": {"title": "t", "selftext": "s"}} for _ in range(25)]
        m.getRandomPost.return_value = {"data": {"children": data}}
        m.getRandomXkcd.return_value = {"safe_title": "safe", "img": "img"}
        res1 = cb.getResponse("xkcd")
        res2 = cb.getResponse("nali")
        self.assertEqual({'answer': 'safe', 'img': 'img'}, res1)
        self.assertEqual({"answer": "t\ns"}, res2)
