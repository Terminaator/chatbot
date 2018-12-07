from langprocessing.WordTags import WordTag as wt
from oisbotServer.views.auth import authentication as auth # ei tööta ilusti
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
        return wt.auth in layer[wt.keywords]

    def answer(self, layer):
        """
        answers based on authentication status
        :param layer: current layer
        :param request: user querry
        :return: answer based on authentication status
        """
        if auth.isTokkenValid(self.xToken).status_code == 200:
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

        response = auth.login(self.username, inputString)
        if response.status_code == 200:
            self.xToken = response["X-Access-Token"]
            json = user.getUserBasicDetails(self.xToken)
            return "Tere " + json["first_name"] + "!"
        return "Midagi läks valesti"

    def getData(self):
        return [self.authStepInProgress, self.xToken, self.username]

    def setData(self, data):
        self.authStepInProgress = data[0]
        self.xToken = data[1]
        self.username = data[2]






