import views.ois.courses as oisCourses
import estnltk as enl
from estnltk import Text
import itertools
import csv
import os


def getWords(sentence):
    """
    :param sentence: User input
    :return: tagged words in dictionary
    """
    text = Text(sentence)
    text.tag_layer(['morph_analysis'])
    result = _tagWords(text)
    return result



def _tagWords(inputText):
    questionwords = ['kes', 'mis', 'kus', 'mitu'] # todo more or think something else
    result = dict()
    counter = 0
    courses = _getCourses()
    i = 1
    tag = ""
    words = [x[0].lower() for x in inputText.morph_analysis.text]
    while "courseID" not in result and i <= len(words):
        for lemma in itertools.combinations(words, i):
            word = " ".join(lemma)
            if word in courses:
                result['courseID'] = courses[word]
                tag = word
        i += 1

    i = 1
    lemmas = []
    for x, y in zip(inputText.morph_analysis.lemma, inputText.morph_analysis.text):
        if 'courseID' in result and y[0].lower() not in tag.split():
            lemmas += [x[0]]

    while "courseID" not in result and i <= len(lemmas) or i == 1:
        for lemma in itertools.combinations(lemmas, i):
            word = " ".join(lemma)
            if word in courses:
                result['courseID'] = courses[word]
                if i > 1:
                    for l in lemma:
                        del result[l]
            elif word == 'eap':
                result['ects'] = True
            elif word in questionwords:
                result['questionWord'] = word
            elif i == 1:
                result[counter] = word
                counter += 1
        i += 1
    return result

def _getCourses():
    courses = dict()
    with open(os.path.join(os.path.dirname(__file__), 'courses.csv'), encoding="UTF-8") as file:
        reader = csv.reader(file)
        for line in reader:
            courses[line[0].strip()] = line[1].strip()
        return courses

def updateCourses():
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
                        writer.writerow([c['title']['et'].lower(), c['code']])
                    elif 'en' in c['title']:
                        writer.writerow([c['title']['en'].lower(), c['code']])
            i += n
            courses = oisCourses.getNCourses(n, i)
