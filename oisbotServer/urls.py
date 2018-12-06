from django.conf.urls import url
from django.views.generic import TemplateView
import oisbotServer.views.client.ClientQuestionView
import oisbotServer.views.auth.authentication


urlpatterns = [
    url(r'^api/authenticated', oisbotServer.views.auth.authentication.isLogged),
    url(r'^api/login/', oisbotServer.views.auth.authentication.authenticate),
    url(r'^api/question', oisbotServer.views.client.ClientQuestionView.ClientQuestionView.as_view()),
    url(r'^', TemplateView.as_view(template_name="main.html")),
]
