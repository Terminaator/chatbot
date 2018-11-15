from langprocessing.wordTags import WordTag as wt


class AuthReqQuestions:
    def __init__(self):
        self.questions = [
            NextCourse()
        ]

    def canAnswer(self, layer):
        return len(layer[wt.courseID]) != 0

    def answer(self, layer):
        for q in self.questions:
            if q.canAnswer(layer):
                return q.answer(layer)

class NextCourse:
    def canAnswer(self, layer):
        return layer[wt.pronoun] == "mina" and layer[wt.timeWord] == "järgmine" and wt.course in layer[wt.keywords] and layer[wt.questionWord]

    def answer(self, layer):
        """
        questions a question about users next course
        :param layer: curreny layer
        :return: question to the question
        """
        return "Kahjuks ma ei saa teile vastata kuna te pole sisse logitud."
