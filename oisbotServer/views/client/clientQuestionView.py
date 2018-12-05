from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
import langprocessing.chatbot as cbot
from oisbotServer.views.json.requestJson import RequestJson
from django.core.cache import cache
from langprocessing.data import Data
from secrets import token_urlsafe

@method_decorator(csrf_exempt, name='dispatch')
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
            cache.set(cookie,self.bot.getData())
            return response
        else:
            key = token_urlsafe(16)
            response = JsonResponse(self.bot.getResponse(inputSentence))
            cache.set(key,self.bot.getData())
            response.set_cookie("TakeMeHome",key)
            return response


    def getCookie(self,cookie):
        if cookie is None:
            return False
        else:
            data = cache.get_or_set(cookie, Data(self.bot.askedQuestion,self.bot.frames,self.bot.currentFrame))
            self.bot.setData(data)
            return True