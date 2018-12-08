from langprocessing.WordTags import WordTag as wt
import langprocessing.questions.answers.WhoAnswers as wha


class WhoIs:
    def canAnswer(self, layer):
        """
        checks if user asked WHO IS question
        :param currenLayer: currently used layer
        :return:return if client asked who question
        """
        sentence = layer[wt.sentence]
        if len(sentence) < 2:
            return False
        if sentence[1] != wt.verb or sentence[0] != wt.questionWord:
            return False
        return (layer[wt.questionWord] in ["kes", "keda"] and
                len(set(layer[wt.verb]).intersection({"olema", "valima", "on"}))) != 0 and sentence[2] == wt.about

    def answer(self, layer):
        """
        Answers general who questions about UT
        :param word: Noun that the user asks the meaning of
        :return: If chatbot knows the answer then it returns the answer, otherwise it will return that it does not know
        """
        answer = wha.Answers
        word = layer[wt.about]
        try:
            a = answer.__getattribute__(answer, word)
        except AttributeError:
            a = "Ma ei tea kes " + word + " on."
        return a
