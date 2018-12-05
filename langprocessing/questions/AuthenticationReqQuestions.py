from langprocessing.wordTags import WordTag as wt
#from oisbotServer.views.auth import authentication as auth #This class doesnt work properly



class AuthReqQuestions:
    def __init__(self):
        self.questions = [
            NextCourse(),
            NewNotifications()
        ]

    def canAnswer(self, layer):
        return True

    def answer(self, layer, request):
        for q in self.questions:
            if q.canAnswer(layer):
                return q.answer(layer, request)


class NextCourse:
    def canAnswer(self, layer):
        return False # layer[wt.pronoun] == "mina" and layer[wt.timeWord] == "järgmine" and wt.course in layer[wt.keywords] and layer[wt.questionWord]

    def answer(self, layer, request):
        """
        questions a question about users next course
        :param layer: current layer
        :return: question to the question
        """
        return "Kahjuks ma ei saa teile vastata kuna te pole sisse logitud."


class NewNotifications:

    def canAnswer(self, layer):
        return False ## wt.wordNew in layer[wt.keywords] and wt.notifications in layer[wt.keywords]

    def answer(self, layer, request):
        """
        questions a question about users notifications
        :param layer: current layer
        :return: question to the question
        """
        """
        if (auth.isAuthenticated(request)):
            return "siin peaks vastus olema"
            """
        return "Kahjuks ma ei saa teile vastata kuna te pole sisse logitud."