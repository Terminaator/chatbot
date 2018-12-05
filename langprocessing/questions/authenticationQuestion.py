from langprocessing.wordTags import WordTag as wt
# from oisbotServer.views.auth import authentication as auth # ei tööta ilusti
from oisbotServer.views.auth import user

class Authenticate:

    def __init__(self):
        self.authStepInProgress = 0
        self.xToken = None
        self.username = ""

    def canAnswer(self, layer):
        """
        checks if the question can be answered
        :param layer: current layer
        :return: True, if can answer
        """
        return False #wt.auth in layer[wt.keywords]

    def answer(self, layer, request):
        """
        answers based on authentication status
        :param layer: current layer
        :param request: user querry
        :return: answer based on authentication status
        """
        if (self.xToken != None):
            return "Te olete juba sisse logitud"
        else:
            self.authStepInProgress = 1
            return "Palun sisestage kasutajanimi"

    def continueAuth(self, inputString):
        """
        Deals with asking the right questions
        :param inputString: user input
        :return: next question
        """
        if (self.authStepInProgress == 1):
            return self.askPW(inputString)
        elif (self.authStepInProgress == 2):
            return self.auth(inputString)
        else:
            return "Midagi läks autentimisega valesti"

    def askPW(self, inputString):
        """
        saves the username and asks for pw
        :param inputString: username
        :return: question asking the pw
        """
        self.authStepInProgress = 2
        self.username = inputString
        return "Palun sisestage parool"

    def auth(self, inputString):
        """
        Authenticates the user
        :param inputString: pw
        :return: greets the user by name
        """
        self.authStepInProgress = 0
        # uncomment this once Authentication api works
        """
        response = auth.login(self.username, inputString)
        if response.status_code == 200:
            self.xToken = response["X-Access-Token"]
            json = user.getUserBasicDetails(self.xToken)
            return "Tere " + json["first_name"] + "!"
        """
        return "Midagi läks valesti"






