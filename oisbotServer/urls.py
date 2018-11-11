from django.conf.urls import url
from django.views.generic import TemplateView
import oisbotServer.views.client.clientQuestionView

urlpatterns = [
    url(r'^api/question', oisbotServer.views.client.clientQuestionView.ClientQuestionView.as_view()),
    url(r'^', TemplateView.as_view(template_name="main.html")),
]
