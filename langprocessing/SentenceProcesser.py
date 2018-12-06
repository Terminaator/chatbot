# coding: utf-8
import oisbotServer.views.ois.courses as oisCourses
import oisbotServer.views.ois.structuralUnits as oisStrucUnits
from collections import defaultdict
from estnltk import Text
import itertools
import logging
import csv
import os
from langprocessing.WordTags import WordTag as wt


class SentenceProcessor:
    def __init__(self):
        self.courses = self._getCourses()
        self.structuralUnits = self._getStructuralUnits()
        self.structuralUnitCodes = self._getStructuralUnitCodes()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel('DEBUG')

    def getWords(self, sentence):
        """
        :param sentence: User input
        :return: tagged words in dictionary
        """
        text = Text(sentence)
        result = self._tagWords(text)
        self.logger.debug('Founded words: ' + str(result))
        result[wt.numbers] = self._getNumbersFromText(sentence)
        return result

    def _tagWords(self, inputText: Text):
        """
        Tags words and forms result dictionary
        :param inputText: Text object with morph_analysis layer
        :return: tagged words in dictionary
        """

        # keywords
        keywords = defaultdict(set)
        keywords[wt.help] = {'aitama', 'help', 'abi'}
        keywords[wt.courseCodeMentioned] = {'ainekood', 'kood'}
        keywords[wt.preReqs] = {'eeldusaine', 'eeldus'}
        keywords[wt.greeting] = {'tere', 'hei', 'hommikust', 'hommik', 'õhtust', 'tsau', 'ahoi'}
        keywords[wt.language] = {'keel'}
        keywords[wt.description] = {'kirjeldus'}
        keywords[wt.objective] = {'eesmärk'}
        keywords[wt.website] = {'koduleht', 'leht', 'veeb', 'veebileht', 'link'}
        keywords[wt.lecturers] = {'õppejõud'}
        keywords[wt.ects] = {'eap', 'eapd'}
        keywords[wt.phone] = {'telefon', 'mobiil', 'number', 'telefoninumber'}
        keywords[wt.email] = {'email', 'mail', 'meil'}
        keywords[wt.address] = {'aadress', 'asukoht'}
        keywords[wt.grade] = {'hindamine', 'hinne'}
        keywords[wt.course] = {'aine', 'kursus'}
        keywords[wt.wordNew] = {'uus'}
        keywords[wt.notifications] = {'teade'}
        keywords[wt.randomJoke] = {'nali'}
        keywords[wt.randomFunny] = {'pilt'}
        keywords[wt.randomXkcd] = {'xkcd'}
        keywords[wt.video] = {'vastus'}
        keywords[wt.auth] = {'sisene', 'login'}
        keywords[wt.hangman] = {'hangman'}


        # Keywords what needs string in frame
        keywordsString = defaultdict(set)
        keywordsString[wt.questionWord] = {'kes', 'mis', 'kus', 'mitu', 'kuna'}
        keywordsString[wt.pronoun] = {'mina', 'sina', 'tema', 'teie', 'meie', 'nemad'}
        keywordsString[wt.timeWord] = {'järgmine'}
        keywordsString[wt.websiteName] = {'courses', 'moodle', 'õis', 'õppeinfosüsteem', 'raamatukogu', 'ester',
                                          'esileht'}
        keywordsString[wt.about] = {'õppekava', 'õppeaine', 'valikaine', 'vabaaine', 'ainepunkt', 'EAP', 'moodul',
                                    'alusmoodul', 'suunamoodul', 'erialamoodul', 'valikmoodul', 'vabaaine',
                                    'bakalaureusetöö', 'bakalaureus', 'peaeriala', 'kõrvaleriala',
                                    'rakenduskõrgharidus', 'akrediteerimine', 'diplom', 'eksmatrikuleerimine',
                                    'ekstern', 'hindamine', 'immatrikuleerimine', 'kratt', 'urkund', 'külalisõppejõud',
                                    'õpiväljund', 'õppekavagrupp', 'õppekoht', 'õppekoormus', 'õppekorralduseeskiri',
                                    'õppeplaan', 'õppesuund', 'õppevaldkond', 'õppevorm', 'päevaõpe', 'sessioonõpe',
                                    'petturlus', 'praktika', 'võta', 'valdkond', 'reimmatrikuleerimine', 'täiskoormus',
                                    'osakoormus', 'akadeemilinekalender', 'eksam', 'korduseksam',
                                    'akadeemilinepuhkus', 'plagiaat', 'õppeprorektor', 'teadusprorektor',
                                    'arendusprorektor', 'kantsler', 'looja', 'rektor', 'tuutor'
                                    }
        keywordsString[wt.weather] = {"ilm", "ilmastik", "ilmake", "ilmuke", "ilmataat"}
        keywordsString[wt.when] = {"täna", "homme", "ülehomme", "homne", "ülehomne"}


        result = defaultdict(list)
        inputText.tag_layer(['morph_analysis'])

        # looks for courses from lemmatized courses dictionary
        words = inputText.morph_analysis
        i = len(words)
        coursesWords = []
        sUnitWords = []
        otherWords = []
        counter = 0
        wordCounter = 0

        for word in words:
            lemma = word.lemma[0].lower()
            # courses
            for key in keywords:
                if lemma in keywords[key]:
                    result[wt.keywords].append(key)
                    break
            # Misc
            for key in keywordsString:
                if lemma in keywordsString[key]:
                    result[key] = lemma
                    break
            # Structural units
            if lemma in self.structuralUnitCodes:
                result[wt.structureUnitCode] = [lemma]
            else:
                if 'V' in word.partofspeech:
                    result[wt.verb] += [lemma]
                else:
                    otherWords.append(lemma)
            counter += 1

        # Multi word keywords
        lemmas = [x.lemma[0].lower() for x in words]
        while i > 0:
            for lemma in itertools.combinations(lemmas, i):
                lemm = " ".join(lemma)
                if lemm in self.courses:
                    result[wt.courseID] += (self.courses[lemm])
                    coursesWords += lemma
                if lemm in self.structuralUnits:
                    result[wt.structureUnitCode] += (self.structuralUnits[lemm])
                    sUnitWords += lemma
                elif i == 1 and lemm not in coursesWords and lemm not in sUnitWords and lemm in otherWords:
                    result[wordCounter] = lemm
                    wordCounter += 1
            i -= 1

        result[wt.what] = result[1]
        return result

    def _getNumbersFromText(self, text):
        return [int(s) for s in text.split() if s.isdigit()]

    def _getCourses(self):
        """
        Reads courses from csv file
        :return: courses in dictionary
        """
        courses = defaultdict(list)
        with open(os.path.join(os.path.dirname(__file__), 'courses.csv'), encoding="UTF-8") as file:
            reader = csv.reader(file)
            for line in reader:
                courses[line[0].strip()].append(line[1].strip())
            return courses

    def _getStructuralUnits(self):
        """
        Reads structural Units from csv file
        :return: structural Units' codes and names in estonian in a dictionary
        """
        sUnits = defaultdict(list)
        with open(os.path.join(os.path.dirname(__file__), 'structuralUnits.csv'), encoding="UTF-8") as file:
            reader = csv.reader(file)
            for line in reader:
                sUnits[line[0].strip()].append(line[1].strip())
            return sUnits

    def _getStructuralUnitCodes(self):
        sUnits = []
        with open(os.path.join(os.path.dirname(__file__), 'structuralUnits.csv'), encoding="UTF-8") as file:
            reader = csv.reader(file)
            for line in reader:
                sUnits.append(line[1].strip())
            return set(sUnits)

    def updateCourses(self):
        self.updateCourses()
        self.logger.info('Updated courses dictionary')


def updateCoursesCSV():
    """
    Updates csv file where is all courses
    """
    with open(os.path.join(os.path.dirname(__file__), 'courses.csv'), 'w', newline='', encoding="UTF-8") as file:
        n = 300
        writer = csv.writer(file, delimiter=',')
        i = 1
        courses = oisCourses.getNCourses(n, i)
        while len(courses) != 0:
            for c in courses:
                if 'title' in c:
                    if 'et' in c['title']:
                        t = Text(c['title']['et'].lower())
                        t.tag_layer(['morph_analysis'])
                        writer.writerow([" ".join([x[0] for x in t.morph_analysis.lemma]), c['code']])
                    elif 'en' in c['title']:
                        t = Text(c['title']['en'].lower())
                        t.tag_layer(['morph_analysis'])
                        writer.writerow([" ".join([x[0] for x in t.morph_analysis.lemma]), c['code']])
            i += n
            courses = oisCourses.getNCourses(n, i)


def updateStructuralUnitsCSV():
    """
    Updates csv file where are all the university structure units
    """
    with open(os.path.join(os.path.dirname(__file__), 'structuralUnits.csv'), 'w', newline='',
              encoding="UTF-8") as file:
        writer = csv.writer(file, delimiter=',')
        sUnits = oisStrucUnits.getAllStructuralUnits()
        for c in sUnits:
            if 'code' in c:
                if 'et' in c['name']:
                    t = Text(c['name']['et'].lower())
                    t.tag_layer(['morph_analysis'])
                    writer.writerow([" ".join([x[0] for x in t.morph_analysis.lemma]), c['code'].lower()])
