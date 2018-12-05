from langprocessing.wordTags import WordTag as wt
from oisbotServer.views.auth import authentication as auth
from oisbotServer.views.auth import user

class Authenticate:

    def __init__(self):
        self.authStepInProgress = 0
        self.xToken = None
        self.username = ""

    def canAnswer(self, layer):
        return wt.auth in layer[wt.keywords]

    def answer(self, layer, request):

        if (self.xToken != None):
            return "Te olete juba sisse logitud"
        else:
            self.authStepInProgress = 1
            return "Palun sisestage kasutajanimi"

    def continueAuth(self, inputString):
        if (self.authStepInProgress == 1):
            return self.askPW(inputString)
        elif (self.authStepInProgress == 2):
            return self.auth(inputString)
        else:
            return "Midagi läks autentimisega valesti"

    def askPW(self, inputString):
        self.authStepInProgress = 2
        self.username = inputString
        return "Palun sisestage parool"

    def auth(self, inputString):
        self.authStepInProgress = 0
        response = auth.login(self.username, inputString)
        if response.status_code == 200:
            self.xToken = response["X-Access-Token"]
            json = user.getUserBasicDetails(self.xToken)
            return "Tere " + json["first_name"] + "!"
        else:
            return "Midagi läks valesti"






