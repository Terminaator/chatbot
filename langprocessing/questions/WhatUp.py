from langprocessing.WordTags import WordTag as wt


class WhatUp:
    def canAnswer(self, layer):
        return 'mis' in layer[wt.questionWord] and 'tegema' in layer[wt.verb]

    def answer(self, layer):
        return "Hetkel vastan küsimustele, aga hiljem lähen ATV-ga sõitma."