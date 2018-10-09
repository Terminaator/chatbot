import views.ois.courses as oisCourses
from collections import defaultdict
import estnltk as enl
from estnltk import Text
import itertools
import logging
import csv
import os


class SentenceProcessor:
    def __init__(self):
        self.courses = self._getCourses()
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
        return result

    def _tagWords(self, inputText: Text):
        """
        Tags words and forms result dictionary
        :param inputText: Text object with morph_analysis layer
        :return: tagged words in dictionary
        """
        questionwords = ['kes', 'mis', 'kus', 'mitu']  # todo more or think something else
        result = defaultdict(list)
        counter = 0
        courses = self._getCourses()
        inputText.tag_layer(['morph_analysis'])

        # looks for courses from lemmatized courses dictionary
        lemmas = [x[0] for x in inputText.morph_analysis.lemma]
        i = len(lemmas)
        coursesWords = []
        while i > 0:
            for lemma in itertools.combinations(lemmas, i):
                word = " ".join(lemma)
                if word in courses:
                    result['courseID'] = courses[word]
                    coursesWords += lemma
                elif word == 'eap':
                    result['ects'] = True
                elif word in questionwords:
                    result['questionWord'] = word
                elif i == 1 and word not in coursesWords:
                    result[counter] = word
                    counter += 1
            i -= 1
        return result

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
