from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from views.json.requestJson import  RequestJson
import views.ois.test as s

@method_decorator(csrf_exempt, name='dispatch') #Võimalik, et me eemaldame selle ära
class ClientQuestionView(View):

    @method_decorator(RequestJson)
    def post(self, request):
        json_data = request.json
        s.req()
        return JsonResponse({"key": "value"})
