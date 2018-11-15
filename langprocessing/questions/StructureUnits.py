from langprocessing.wordTags import WordTag as wt
import oisbotServer.views.ois.structuralUnits as oisStructuralUnits
from estnltk.vabamorf.morf import synthesize, analyze


class StructureUnitQuestions:
    def __init__(self):
        self.subject = "struktuuriüksuse"
        self.possibleTopics = ['kodulehte', 'telefoninumbrit', 'asukohta', 'emaili']
        self.questions = [
            Website(),
            Phone(),
            Email(),
            Address()
        ]

    def canAnswer(self, layer):
        return len(layer[wt.structureUnitCode]) != 0

    def answer(self, layer):
        for q in self.questions:
            if q.canAnswer(layer):
                return q.answer(layer)


class Website:
    def canAnswer(self, layer):
        return wt.website in layer[wt.keywords]

    def answer(self, layer):
        """
        finds and gives possible links as an answer to the asked question
        :param Layer: Current frame layer
        :return: Structure unit websites
        """
        possibleLinks = set()
        linkMap = {}
        StructUnits = layer[wt.structureUnitCode]
        for unit in StructUnits:
            json = oisStructuralUnits.getStructuralUnit(unit)
            if "webpage_url" in json:
                link = json["webpage_url"]
                if link not in possibleLinks:
                    possibleLinks.add(link)
                    linkMap[json["name"]["et"]] = link

        if len(possibleLinks) == 0:
            return "Sain küsimusest valesti aru või küsitud struktuuriüksusel ei ole veebilehte."
        elif len(possibleLinks) == 1:
            return "Selle struktuuriüksuse veebileht asub aadressil " + linkMap.popitem()[1]
        return "Leidsin mitu erinevat veebilehte. Need on: " + ', '.join(possibleLinks)


class Phone:
    def canAnswer(self, layer):
        return wt.phone in layer[wt.keywords]

    def answer(self, layer):
        """
        Creates answer for phone question
        :param structUnits: asked structuralunits
        :return: structuralunits phonenumber
        """
        structUnits = layer[wt.structureUnitCode]
        results = []
        for id in structUnits:
            json = oisStructuralUnits.getStructuralUnit(id)
            name = json['name']['et'].split(" ")
            name[-1] = synthesize(name[-1], 'sg g')[0]
            results.append(" ".join(name).capitalize() + "("+json['code']+")" + " telefoni number on " + json['phone'])
        return "\n".join(results) + "."


class Email:
    def canAnswer(self, layer):
        return wt.email in layer[wt.keywords]

    def answer(self, layer):
        """
        Creates answer for email question
        :param structUnits: asked structuralunits
        :return: structuralunits email
        """
        results = []
        structUnits = layer[wt.structureUnitCode]
        for id in structUnits:
            json = oisStructuralUnits.getStructuralUnit(id)
            name = json['name']['et'].split(" ")
            name[-1] = synthesize(name[-1], 'sg g')[0]
            results.append(" ".join(name).capitalize() + "("+json['code']+")" + " email on " + json['email'])
        return "\n".join(results) + "."


class Address:
    def canAnswer(self, layer):
        return wt.address in layer[wt.keywords] or layer[wt.questionWord] in ['kus'] and ('olema' in layer[wt.verb] or 'asuma' in layer[wt.verb])

    def answer(self, layer):
        """
        Creates answer for address question
        :param structUnits: asked structuralunits
        :return: structuralunits address
        """
        results = []
        structUnits = layer[wt.structureUnitCode]
        for id in structUnits:
            json = oisStructuralUnits.getStructuralUnit(id)
            name = json['name']['et'].split(" ")
            name[-1] = synthesize(name[-1], 'sg g')[0]
            results.append(" ".join(name).capitalize() + "("+json['code']+")" + " aadress on " + json['street'] + ", " + json['city'])
        return "\n".join(results) + "."


def synthesizeWord(word, f):
    """
    Changes the word's form without changing it form plural to singular or vice versa
    :param word: word to be formed
    :param f: desired form
    :return: word in desired form
    """
    # need to check if the title is plural or not.
    form = analyze(word)[0]["analysis"][0]["form"]
    return synthesize(word, form[:2] + " " + f, "S")[0]
