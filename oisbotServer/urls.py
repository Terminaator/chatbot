from django.conf.urls import url
from django.urls import re_path
from django.views.generic import TemplateView
import oisbotServer.views.client.clientQuestionView
import oisbotServer.views.auth.authentication


urlpatterns = [
    url(r'^api/authenticated', oisbotServer.views.auth.authentication.isLogged),
    url(r'^api/login/', oisbotServer.views.auth.authentication.authenticate),
    url(r'^api/question', oisbotServer.views.client.clientQuestionView.ClientQuestionView.as_view()),
    url(r'^', TemplateView.as_view(template_name="main.html")),
]
