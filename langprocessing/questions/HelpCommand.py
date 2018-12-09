from langprocessing.WordTags import WordTag as wt
from collections import defaultdict


class HelpCommand:
    def canAnswer(self, layer):
        return wt.help in layer[wt.keywords]

    def answer(self, layer):
        """
        Creates answer for help command
        :return: help
        """
        topics = defaultdict(list)
        topics["Kursused:"] = ['Eap\'de arv', 'Kursuse kood', 'Eeldusained', 'Õpetamiskeel', 'Kirjeldus', 'Eesmärk',
                               'Koduleht', 'Eksami vastused', 'Õppejõud', 'Hindamine']
        topics["Struktuuriüksused:"] = ['Koodi tähendus', 'Koduleht', 'Telefoninumber', 'Email', 'Aadress']
        topics["Sisse logitud kasutaja:"] = ['Järgmine aine', 'matrkli number']
        topics["Muu:"] = ['Moodle link', 'Courses link', 'Õisi link', 'Estri link', 'Pealehe link', 'Tartu ilma(Täna, homme, ülehomme)', "Mis/kes on ___", 'Nali', 'Pilt', 'Xkcd', 'Hangman']

        result = "Mina olen sõbralik õis2 chatbot. Mult saab küsida järgmiste teemade kohta."
        for topic in topics:
            result += "\n" + topic
            for t in topics[topic]:
                result += "\n\t" + t
        result += "\nKüsimiseks kirjuta aine/struktuuri üksuse nimi ja sõna mida tahad teada. Näiteks, et küsida aine tarkvaraprojekti EAP'de arvu, kirjuta 'tarkvaraprojekt eap' ning saad teada, et tarkvaraprojekt on 6 EAP'd."
        result += "\nSisse logimine on omal vastusel ning logimiseks kirjuta sisene."
        result += "\nTeiste küsimuste(kategooria muu) jaoks piisab kui kirjutad üleval antud võtmesõna. Näiteks 'Tartu ilm homme'."

        return result
