from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
import langprocessing.Chatbot as cbot
from oisbotServer.views.json.requestJson import RequestJson
from django.core.cache import cache
from langprocessing.Data import Data
from secrets import token_urlsafe

time = 60 * 10


@method_decorator(csrf_exempt, name='dispatch')  # Võimalik, et me eemaldame selle ära
class ClientQuestionView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bot = cbot.chatbot()

    @method_decorator(RequestJson)
    def post(self, request):
        inputSentence = request.json.get('question')
        cookie = request.COOKIES.get("TakeMeHome")
        if self.getCookie(cookie):
            response = JsonResponse(self.bot.getResponse(inputSentence))
            cache.set(cookie, self.bot.getData(), time)
            return response
        else:
            key = token_urlsafe(16)
            response = JsonResponse(self.bot.getResponse(inputSentence))
            cache.set(key, self.bot.getData(), time)
            response.set_cookie("TakeMeHome", key, max_age=time)
            return response

    def getCookie(self, cookie):
        if cookie is None:
            return False
        else:
            data = cache.get_or_set(cookie, Data(self.bot.askedQuestion, self.bot.frames, self.bot.currentFrame), time)
            self.bot.setData(data)
            return True
