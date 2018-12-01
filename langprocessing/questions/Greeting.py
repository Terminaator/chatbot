from langprocessing.wordTags import WordTag as wt
from random import randint


class Greeting:
    def canAnswer(self, layer):
        return wt.greeting in layer[wt.keywords]

    def answer(self, layer):
        greetings = ['Tere!', 'Hello!', 'Ahoi!', 'Tervitus!', 'Näen, et mind on üles leitud. Teretulemast!',
                     'Tervist, härra President!', 'Tere, tere, vana kere!', 'Tere kaunitar!',
                     'Ära ehmata! Hommikust sullegi!',
                     '01010100 01100101 01110010 01100101 00001010', 'Tsau tsau!']
        return greetings[randint(0, len(greetings) - 1)]
