from langprocessing.wordTags import WordTag as wt
import oisbotServer.views.ois.courses as oisCourses
from estnltk.vabamorf.morf import synthesize, analyze


class CourseQuestions:
    def __init__(self):
        self.subject = "kursuse"  # todo käänamine või panna kõik juba sobivasse käändesse
        self.possibleTopics = ["eelduaineid", "eapde arvu", "ainekoodi", "õpetamiskeelt", "kodulehte", "õppejõude",
                               "kirjeldust", "eesmärki", "hindamist"]  # todo add words if you add questions

        self.questions = [
            CourseCode(),
            Ects(),
            PreReqs(),
            Language(),
            Description(),
            Objective(),
            Website(),
            Lecturers(),
            Grade()
        ]

    def canAnswer(self, layer):
        return len(layer[wt.courseID]) != 0

    def answer(self, layer):
        for q in self.questions:
            if q.canAnswer(layer):
                return q.answer(layer)


class CourseCode:
    def canAnswer(self, layer):
        return wt.courseCodeMentioned in layer[wt.keywords]

    def answer(self, layer):
        """
        Creates an answer for questions about course code. like "mis on masinõppe ainekood"
        :param layer: Current frame layer
        :return: an answer with course code(s)
        """
        courseId = layer[wt.courseID]
        if len(courseId) == 1:
            id = courseId.pop()
            json = oisCourses.coursesId(id)
            title = json["title"]["et"]
            if " " in title:
                return "Kursuse " + title + " ainekood on " + id
            return synthesizeWord(title, "g").capitalize() + " ainekood on " + id
        else:
            response = "Selle nimega on " + str(len(courseId)) + " erinevat kursust. Nende ainekoodid on "
            for i in courseId[:-2]:
                response += i + ", "
            response += courseId[-2] + " ja "
            return response + courseId[-1] + "."


class Ects:
    def __init__(self):
        pass

    def canAnswer(self, layer):
        return wt.ects in layer[wt.keywords]

    def answer(self, layer):
        """
        Creates an answer for questions about course ects.
        :param layer: Current frame layer
        :return: an answer
        """
        courseId = layer[wt.courseID]
        if len(courseId) == 1:
            json = oisCourses.coursesId(courseId[0])
            title = json["title"]["et"]
            if " " in title:
                return "Kursuse " + title + " maht on " + str(json["credits"]) + " EAP."
            return synthesizeWord(title, "g").capitalize() + " maht on " + str(json["credits"]) + " EAP."

        else:
            response = "Selle nimega on " + str(len(courseId)) + " erinevat kursust."
            json = oisCourses.coursesId(courseId[0])
            response += " " + courseId[0] + " mille maht on " + str(json["credits"]) + " EAP"
            for i in courseId[1:-1]:
                json = oisCourses.coursesId(i)
                response += ", " + i + " mille maht on " + str(json["credits"]) + " EAP"
            json = oisCourses.coursesId(courseId[-1])
            response += " ja " + courseId[-1] + " mille maht on " + str(json["credits"]) + " EAP."
            return response


class PreReqs:
    def canAnswer(self, layer):
        return wt.preReqs in layer[wt.keywords]

    def answer(self, layer):
        """
        Creates an answer for question about prerequired courses
        :param layer: Current frame layer
        :return: An answer, that contains prerequired courses
        """
        courseId = layer[wt.courseID]
        if len(courseId) == 1:
            result = "Selle kursuse"
        else:
            result = "Selle nimega on " + str(len(courseId)) + " erinevat kursust."

        for id in courseId:

            json = oisCourses.coursesId(id)
            if "prerequisites" in json["additional_info"]:
                if len(courseId) > 1:
                    result += " Kursuse " + id

                preReqs = json["additional_info"]["prerequisites"]
                if len(preReqs) == 1:
                    result += " eeldusaine on"
                else:
                    result += " eeldusained on"

                for req in preReqs:
                    result += " " + req["code"] + " \"" + req["title"]["et"] + "\""
                    if "alternatives" in req:
                        alternatives = req["alternatives"]
                        for alt in alternatives:
                            result += " või " + alt["code"] + " \"" + alt["title"]["et"] + "\""
            elif len(courseId) > 1:
                result += " Kursusel " + id + " eeldusained puuduvad"
            else:
                return "Sellel kursusel pole eeldusaineid."
        return result + "."


class Language:
    def canAnswer(self, layer):
        return wt.language in layer[wt.keywords]

    def answer(self, layer):
        """
        Creates answer for language question
        :param layer: Current frame layer
        :return: courses language
        """
        courseIds = layer[wt.courseID]
        results = []
        for id in courseIds:
            json = oisCourses.coursesId(id)
            lang = json['target']['language']['et'].split(" ")
            lang[-1] = synthesize(lang[-1], "sg in", "S")[0]
            results.append("Aine " + json['title']['et'] + "(" + id + ")" + " on " + " ".join(lang))
        return "\n".join(results) + "."


class Description:
    def canAnswer(self, layer):
        return wt.description in layer[wt.keywords]

    def answer(self, layer):
        """
        Creates answer for description question
        :param layer: Current frame layer
        :return: courses description
        """
        results = []
        courseIds = layer[wt.courseID]
        for id in courseIds:
            json = oisCourses.coursesId(id)
            results.append(
                "Aine " + json['title']['et'] + "(" + id + ")" + " kirjeldus:\n" + json['overview']['description'][
                    'et'])
        return "\n".join(results)


class Objective:

    def canAnswer(self, layer):
        return wt.objective in layer[wt.keywords]

    def answer(self, layer):
        """
        Creates answer for objectives question
        :param layer: Current frame layer
        :return: courses objective
        """
        results = []
        courseIds = layer[wt.courseID]
        for id in courseIds:
            json = oisCourses.coursesId(id)
            results.append(
                "Aine " + json['title']['et'] + "(" + id + ")" + " eesmärk:\n" + json['overview']['objectives'][0][
                    'et'])
        return "\n".join(results)


class Website:
    def canAnswer(self, layer):
        return wt.website in layer[wt.keywords]

    def answer(self, layer):
        """
        Creates answer for website question
        :param layer: Current frame layer
        :return: courses website
        """
        results = []
        courseIds = layer[wt.courseID]
        for id in courseIds:
            json = oisCourses.coursesId(id)
            results.append(
                "Aine " + json['title']['et'] + "(" + id + ")" + " veebileht on " + json['resources']['website_url'])
        return "\n".join(results)


class Lecturers:
    def canAnswer(self, layer):
        return wt.lecturers in layer[wt.keywords]

    def answer(self, layer):
        """
        Creates answer for lecturers question
        :param layer: Current frame layer
        :return: courses lecturers
        """
        results = []
        courseIds = layer[wt.courseID]
        for id in courseIds:
            json = oisCourses.coursesId(id)
            lecturers = json['participants']['lecturers']
            result = ""
            result += "Aine " + json['title']['et'] + "(" + id + ") "
            responsible = []
            otherLecturers = []
            for lecturer in lecturers:
                if lecturer['is_responsible']:
                    responsible.append(lecturer['person_name'])
                else:
                    otherLecturers.append(lecturer['person_name'])
            if len(responsible) == 1:
                result += "vastutav õppejõud on " + responsible[0] + "."
            else:
                result += "vastutavad õppejõud on " + ", ".join(responsible) + "."
            if len(otherLecturers) != 0:
                result += "\nTeised õppejõud on " + ", ".join(otherLecturers)
            results.append(result)
        return "\n".join(results)


class Grade:
    def canAnswer(self, layer):
        return wt.grade in layer[wt.keywords]

    def answer(self, layer):
        """
        Creates answer for grade question
        :param layer: Current frame layer
        :return: courses grading
        """
        results = []
        courseIds = layer[wt.courseID]
        for id in courseIds:
            json = oisCourses.coursesId(id)
            result = "Aine " + json['title']['et'] + "(" + id + ")" + " hindamine on " + \
                     json['grading']['assessment_scale']['et']
            if "et" in json['grading']['grade_evaluation']:
                result += ".\nLõpphinne:\n" + json['grading']['grade_evaluation']['et']
            if "et" in json['grading']['debt_elimination']:
                result += "\nVõlgnevuste likvideerimine:\n" + json['grading']['debt_elimination']['et']
            results.append(result)
        return "\n".join(results)


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
