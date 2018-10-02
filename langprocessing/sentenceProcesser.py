import estnltk as enl
from estnltk import Text
#from estnltk.taggers import VabamorfDisambiguator, VabamorfTagger, UserDictTagger

"""

:param sentence: 
"""



def getWords(sentence):
    inputText = Text(sentence)
    # morphTagger = VabamorfTagger()
    # morphDisambiguator = VabamorfDisambiguator()
    # userTagger = UserDictTagger()
    inputText.tag_layer(['words', 'sentences'])
    # morphTagger.tag(inputText)
    # print(inputText.morph_analysis.partofspeech)
    # userTagger.add_word("eap", {"root": "eap", "type": "ects", })
    # userTagger.tag(inputText)
    # morphDisambiguator.tag(inputText)
    return [x.lemma for x in inputText.morph_analysis]


def tagWords(words):
    wordDict = dict()
    for word in words:
        for lemma in words:
            pass

# print(getWords("Mitu eap on kursus tarkvaraprojekt?"))
