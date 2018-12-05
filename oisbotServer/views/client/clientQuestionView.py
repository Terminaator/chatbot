from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
import langprocessing.chatbot as cbot
from oisbotServer.views.json.requestJson import RequestJson

bot = cbot.chatbot()
@method_decorator(csrf_exempt, name='dispatch') #Võimalik, et me eemaldame selle ära
class ClientQuestionView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    @method_decorator(RequestJson)
    def post(self, request):
        self.request = request
        inputSentence = request.json.get('question')
        return JsonResponse(bot.getResponse(inputSentence))


