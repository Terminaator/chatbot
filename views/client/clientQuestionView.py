from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse

from langprocessing.chatbot import chatbot
from views.json.requestJson import RequestJson

@method_decorator(csrf_exempt, name='dispatch') #Võimalik, et me eemaldame selle ära
class ClientQuestionView(View):
    def __init__(self):
        self.__chatbot = chatbot()

    @method_decorator(RequestJson)
    def post(self, request):
        json_data = request.json
        #return JsonResponse({"answer": self.__chatbot.getResponse(json_data["question"])})
        return 2
