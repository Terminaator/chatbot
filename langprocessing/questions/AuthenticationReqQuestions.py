from langprocessing.WordTags import WordTag as wt
#from oisbotServer.views.auth import authentication as auth #This class doesnt work properly



class AuthReqQuestions:
    def __init__(self):
        self.questions = [
            StudyBookN(),
        ]

    def canAnswer(self, layer):
        return True

    def answer(self, layer, token):
        for q in self.questions:
            if q.canAnswer(layer):
                return q.answer(layer, token)


class StudyBookN:
    def canAnswer(self, layer):
        return layer[wt.pronoun] == "mina" and wt.studybookNr in layer[wt.keywords]

    def answer(self, layer, token):
        """
        questions a question about users next course
        :param layer: current layer
        :return: question to the question
        """
        return "Kahjuks ma ei saa teile vastata kuna te pole sisse logitud."

