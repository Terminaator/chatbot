# coding: utf-8
from bs4 import BeautifulSoup
from django.http import HttpResponse, JsonResponse
from requests import Session
from rest_framework.decorators import api_view
import requests


def login(username,password):
    response = HttpResponse()
    try:
        session = Session()
        page = session.get("https://ois2dev.ut.ee/api/user/sso")
        parts = page.url.split("AuthState")
        login = session.post(parts[0] + "username=" + username + "&password="+ password+ "&AuthState" + parts[1])
        soup = BeautifulSoup(login.content.decode("utf8"), features="lxml")
        payload = {
            'SAMLResponse': soup.find("input", {"name": "SAMLResponse"})["value"],
            'RelayState': soup.find("input", {"name": "RelayState"})["value"]
        }
        session.post("https://ois2dev.ut.ee/Shibboleth.sso/SAML2/POST", data=payload)
        response["X-Access-Token"] = session.cookies["X-Access-Token"]
        response.status_code = 200
    except Exception:
        response.status_code = 401
    finally:
        return response

@api_view(['POST'])
def authenticate(request):
    username = request.GET.get("username")
    password = request.GET.get("password")
    login(username,password)
    return login(username,password)

@api_view(['GET'])
def isLogged(request):
    xAccessToken = request.META.get("HTTP_X_ACCESS_TOKEN")
    if(xAccessToken == None):
        return JsonResponse(data={"login": "Logige palun sisse!"},status=401)
    else:
        check = requests.get("https://ois2dev.ut.ee/api/user",headers={'X-Access-Token': xAccessToken})
        if(check.status_code == 401):
            return JsonResponse(data={"login": "Logige palun sisse!"})
        elif(check.status_code == 200):
            response = JsonResponse(data={"login": "Olete sisse logitud!"})
            response["X-Access-Token"] = xAccessToken
            return response


def isAuthenticated(request):
    x_access_token = request.META.get("HTTP_X_ACCESS_TOKEN")
    if(x_access_token == None):
        return False
    else:
        check = requests.get("https://ois2dev.ut.ee/api/user",headers={'X-Access-Token': x_access_token})
        if(check.status_code == 401):
            return False
        elif(check.status_code == 200):
            return True