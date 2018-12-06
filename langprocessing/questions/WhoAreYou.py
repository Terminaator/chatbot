from langprocessing.WordTags import WordTag as wt

class WhoAreYou:
    def canAnswer(self, layer):
        return layer[wt.questionWord] in ['mis', 'kes'] and layer[wt.pronoun] == 'sina' and 'olema' in layer[wt.verb]

    def answer(self, layer):
        """
        Creates an answer for question who you are
        :return: Describtion of bot
        """
        return "Mina olen sõbralik Õis2 bot. Mina aitan sul saada vastust küsimustele, mis sind vaevavad."