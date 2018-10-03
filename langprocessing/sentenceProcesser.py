import estnltk as enl
from estnltk import Text
from estnltk.taggers import VabamorfTagger, PhraseTagger, read_vocabulary, SpanTagger


def getWords(sentence):
    """

    :param sentence:
    """
    v = read_vocabulary(vocabulary_file='vocabulary.csv', key='_token_',  string_attributes=['value', '_token_'])
    inputText = Text(sentence)
    tagger = SpanTagger(output_layer='tagged_tokens',
                        input_layer='morph_analysis',
                        input_attribute='lemma',
                        vocabulary=v,
                        output_attributes=['value'],  # default: None
                        ambiguous=False  # default: False
                        )
    inputText.tag_layer(['morph_analysis'])
    tagger.tag(inputText)
    print(inputText.morph_analysis)
    return [(i, j) for i, j in zip(inputText.tagged_tokens.text, inputText.tagged_tokens.value)]


print(getWords("Mitu eap'd on kursus tarkvaraprojekt?"))
