# coding: utf-8
import views.ois.courses as oisCourses
import views.ois.structuralUnits as oisStructuralUnits
from estnltk.vabamorf.morf import synthesize, analyze
import langprocessing.sentenceProcesser as sentProc
from random import randint
from langprocessing.wordTags import WordTag as wt


class chatbot():
    def __init__(self):
        self.frames = {}
        self.currentFrame = -1
        self.sentenceProcessor = sentProc.SentenceProcessor()
        self.askedQuestion = 0

    def getResponse(self, inputSentence):
        """
        fills the frame and returns an answer
        :param inputSentence: Question that the client asked
        :return:A response for the client
        """
        words = self.sentenceProcessor.getWords(inputSentence)
        self.addFrameLayer(words)
        return self.putTogetherAnAnswer()

    def putTogetherAnAnswer(self):
        """
        looks at the frame and answers based on that.
        :return: A response for the client
        """
        currentLayer = self.frames["layer " + str(self.currentFrame)]
        misc = currentLayer[wt.misc]
        courses = currentLayer[wt.courses]
        sUnits = currentLayer[wt.structureUnits]
        possibleTopics = []
        subject = ""

        # COURSES questions
        if len(courses[wt.courseID]) != 0:
            if wt.ects in misc[wt.keywords]:
                self.askedQuestion = 0
                return self.answerCourseEcts(courses[wt.courseID])
            if wt.courseCodeMentioned in misc[wt.keywords]:
                self.askedQuestion = 0
                return self.answerCourseCode(courses[wt.courseID])
            if wt.preReqs in misc[wt.keywords]:
                self.askedQuestion = 0
                return self.answerCoursePreReqs(courses[wt.courseID])
            if wt.language in misc[wt.keywords]:
                self.askedQuestion = 0
                return self.answerLanguage(courses[wt.courseID])
            if wt.description in misc[wt.keywords]:
                self.askedQuestion = 0
                return self.answerDescription(courses[wt.courseID])
            if wt.objective in misc[wt.keywords]:
                self.askedQuestion = 0
                return self.answerObjective(courses[wt.courseID])
            if wt.website in misc[wt.keywords]:
                self.askedQuestion = 0
                return self.answerWebsite(courses[wt.courseID])
            if wt.lecturers in misc[wt.keywords]:
                self.askedQuestion = 0
                return self.answerLecturers(courses[wt.courseID])
            if wt.grade in misc[wt.keywords]:
                self.askedQuestion = 0
                return self.answerGrade(courses[wt.courseID])

            # If doesn't know what to answer
            subject = "kursuse"  # todo käänamine või panna kõik juba sobivasse käändesse
            possibleTopics = ["eelduaineid", "eapde arvu", "ainekoodi", "õpetamiskeelt", "kodulehte", "õppejõude",
                              "kirjeldust", "eesmärki", "hindamist"]  # todo add words if you add questions

        # Structure Units
        if len(sUnits[wt.structureUnitCode]) != 0:
            if wt.website in misc[wt.keywords]:
                self.askedQuestion = 0
                return self.answerStructeUnitWebsite(sUnits[wt.structureUnitCode])
            if wt.phone in misc[wt.keywords]:
                self.askedQuestion = 0
                return self.answerPhoneStructUnit(sUnits[wt.structureUnitCode])
            if wt.email in misc[wt.keywords]:
                self.askedQuestion = 0
                return self.answerEmailStructUnit(sUnits[wt.structureUnitCode])
            if wt.address in misc[wt.keywords] or misc[wt.questionWord] in ['kus'] and (
                    'olema' in misc[wt.verb] or 'asuma' in misc[wt.verb]):
                self.askedQuestion = 0
                return self.answerAddressStructUnit(sUnits[wt.structureUnitCode])

            subject = "struktuuriüksuse"
            possibleTopics = ['kodulehte', 'telefoninumbrit', 'asukohta', 'emaili']

        # Other Important Uni websites
        if wt.website in misc[wt.keywords] and len(misc[wt.websiteName]) != 0:
            self.askedQuestion = 0
            return self.answerImportantUniWebsites(misc[wt.websiteName])

        # Authentication required questions
        if misc[wt.pronoun] == "mina" and misc[wt.timeWord] == "järgmine" and wt.course in misc[wt.keywords] and misc[wt.questionWord]:
            self.askedQuestion = 0
            return self.answerAuthMyNextCourse(misc[wt.questionWord])

        # Greeting
        if wt.greeting in misc[wt.keywords]:
            self.askedQuestion = 0
            return self.sayHello()

        # WHAT IS questions
        if self.isWhatIsQuestionAsked(currentLayer):
            if sUnits[wt.structureUnitCode] != "":
                self.askedQuestion = 0
                return self.answerWhatIsStructureCode(sUnits[wt.structureUnitCode])
            if courses[wt.courseID] != "":
                return self.answerWhatIsCourseCode(courses[wt.courseID])

        # Who you are
        if misc[wt.questionWord] in ['mis', 'kes'] and misc[wt.pronoun] == 'sina' and 'olema' in misc[wt.verb]:
            self.askedQuestion = 0
            return self.answerWhoYouAre()

        # Questions with memory
        if self.askedQuestion == 1:
            self.askedQuestion = 2
            temp = self.currentFrame
            self.currentFrame = -1
            answer = self.putTogetherAnAnswer()
            self.currentFrame = temp
            self.askedQuestion = 0
            return answer
        if len(possibleTopics) != 0 and self.askedQuestion == 0:
            self.askedQuestion = 1
            return self.askExtraInfo(subject, possibleTopics)

        self.askedQuestion = False
        return "Kahjuks ma ei saanud teist aru."

    def addFrameLayer(self, words):
        """
        creates a new frame layer
        :param words:  dictionary of words to be added to the new frame layer
        """
        self.currentFrame += 1
        self.frames["layer " + str(self.currentFrame)] = self.fillFrameLayer(words)
        if self.askedQuestion:
            self.frames["layer -1"] = self.updateFrameLayer(words)

    def updateFrameLayer(self, words):
        """
        Adds words to existing layer. Used if bot asked extra questions
        :param words: dictionary of words to be added to the layer
        :return: updated frame layer
        """
        layer = self.frames["layer " + str(self.currentFrame - 1)]
        for key in layer:
            if key != wt.sentence:
                for k in layer[key]:
                    if k in words:
                        layer[key][k] = words[k]
        for k in words:
            layer[wt.sentence].append(k)
        return layer

    def fillFrameLayer(self, words):
        """
        fills a frame layer
        :param words: dictionary of words to be added to the layer
        :return: filled frame layer
        """
        layer = self.createEmptyLayer()
        for key in layer:
            for k in layer[key]:
                if k in words:
                    layer[key][k] = words[k]
        for k in words:
            layer[wt.sentence].append(k)
        return layer

    def createEmptyLayer(self):
        """
        Creates a layer for frame
        Frame with 1 layer structure
        frame = {
            layer 0: {
                sentence : [words]
                misc : {questionWord: String, pronoun: String, verb: String, timeWord; String, websiteName: String, keywords: list}
                courses : {courseID: String}
                structuralUnits: {structuralUnitCode: String}
            }
        }
        """
        # , wt.greeting: False , wt.ects: False, wt.preReqs: False, wt.courseCodeMentioned: False
        misc = {wt.questionWord: "", wt.pronoun: "", wt.verb: "", wt.websiteName: "", wt.timeWord: "", wt.keywords: []}
        courses = {wt.courseID: ""}
        sUnit = {wt.structureUnitCode: ""}
        layer = {wt.sentence: [], wt.misc: misc, wt.courses: courses, wt.structureUnits: sUnit}
        return layer

    def isWhatIsQuestionAsked(self, currentLayer):
        """
        tries to see if user asked a "What is x" question
        :param currentLayer: currently used layer
        :return: Returns if client asked a term explanation question
        """
        misc = currentLayer[wt.misc]
        sentence = currentLayer[wt.sentence]
        if len(sentence) < 3:
            return False
        if sentence[1] != wt.verb or sentence[0] != wt.questionWord:
            return False

        return (misc[wt.questionWord] in ["mis"] and len(
            set(misc[wt.verb]).intersection({"tähendama", "olema"}))) != 0 and (
                   sentence[2] == wt.structureUnitCode or sentence[2] == wt.courseID)

    def askExtraInfo(self, subject, possibleTopics):
        """
        Creates response if user asks question without sufficent informations
        :param subject: user asked question subject
        :param possibleTopics: What user can ask about that subject
        :return: response
        """
        result = "Mulle tundub, et sa tahtsid küsida infot " + subject + " kohta. " + subject.capitalize() + " kohta saad küsida "
        if len(possibleTopics) == 1:
            result += possibleTopics[0] + "."
        else:
            for i in possibleTopics[:-2]:
                result += i + ", "
            result += possibleTopics[-2] + " ja "
            result += possibleTopics[-1] + "."
        result += "\nPalun täpsusta!"
        return result

    def answerGrade(self, courseIds):
        """
        Creates answer for grade question
        :param courseIds: asked courses
        :return: courses grading
        """
        results = []
        for id in courseIds:
            json = oisCourses.coursesId(id)
            result = "Aine " + json['title']['et'] + "(" + id + ")" + " hindamine on " + json['grading']['assessment_scale']['et']
            if "et" in json['grading']['grade_evaluation']:
                result += ".\nLõpphinne:\n" + json['grading']['grade_evaluation']['et']
            if "et" in json['grading']['debt_elimination']:
                result += "\nVõlgnevuste likvideerimine:\n" + json['grading']['debt_elimination']['et']
            results.append(result)
        return "\n".join(results)

    def answerPhoneStructUnit(self, structUnits):
        """
        Creates answer for phone question
        :param structUnits: asked structuralunits
        :return: structuralunits phonenumber
        """
        results = []
        for id in structUnits:
            json = oisStructuralUnits.getStructuralUnit(id)
            name = json['name']['et'].split(" ")
            name[-1] = synthesize(name[-1], 'sg g')[0]
            results.append(" ".join(name).capitalize() + " telefoni number on " + json['phone'])
        return "\n".join(results) + "."

    def answerEmailStructUnit(self, structUnits):
        """
        Creates answer for email question
        :param structUnits: asked structuralunits
        :return: structuralunits email
        """
        results = []
        for id in structUnits:
            json = oisStructuralUnits.getStructuralUnit(id)
            name = json['name']['et'].split(" ")
            name[-1] = synthesize(name[-1], 'sg g')[0]
            results.append(" ".join(name).capitalize() + " email on " + json['email'])
        return "\n".join(results) + "."

    def answerAddressStructUnit(self, structUnits):
        """
        Creates answer for address question
        :param structUnits: asked structuralunits
        :return: structuralunits address
        """
        results = []
        for id in structUnits:
            json = oisStructuralUnits.getStructuralUnit(id)
            name = json['name']['et'].split(" ")
            name[-1] = synthesize(name[-1], 'sg g')[0]
            results.append(" ".join(name).capitalize() + " aadress on " + json['street'] + ", " + json['city'])
        return "\n".join(results) + "."

    def answerLanguage(self, courseIds):
        """
        Creates answer for language question
        :param courseIds: asked courses
        :return: courses language
        """
        results = []
        for id in courseIds:
            json = oisCourses.coursesId(id)
            lang = json['target']['language']['et'].split(" ")
            lang[-1] = synthesize(lang[-1], "sg in", "S")[0]
            results.append("Aine " + json['title']['et'] + "(" + id + ")" + " on " + " ".join(lang))
        return "\n".join(results) + "."

    def answerDescription(self, courseIds):
        """
        Creates answer for description question
        :param courseIds: asked courses
        :return: courses description
        """
        results = []
        for id in courseIds:
            json = oisCourses.coursesId(id)
            results.append(
                "Aine " + json['title']['et'] + "(" + id + ")" + " kirjeldus:\n" + json['overview']['description'][
                    'et'])
        return "\n".join(results)

    def answerObjective(self, courseIds):
        """
        Creates answer for objectives question
        :param courseIds: asked courses
        :return: courses objective
        """
        results = []
        for id in courseIds:
            json = oisCourses.coursesId(id)
            results.append(
                "Aine " + json['title']['et'] + "(" + id + ")" + " eesmärk:\n" + json['overview']['objectives'][0][
                    'et'])
        return "\n".join(results)

    def answerWebsite(self, courseIds):
        """
        Creates answer for website question
        :param courseIds: asked courses
        :return: courses website
        """
        results = []
        for id in courseIds:
            json = oisCourses.coursesId(id)
            results.append(
                "Aine " + json['title']['et'] + "(" + id + ")" + " veebileht on " + json['resources']['website_url'])
        return "\n".join(results)

    def answerStructeUnitWebsite(self, StructUnit):
        """
        finds and gives possible links as an answer to the asked question
        :param StructUnit: Structure units, that were in the question
        :return: Structure unit websites
        """
        possibleLinks = set()
        linkMap = {}
        for unit in StructUnit:
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

    def answerImportantUniWebsites(self, siteName):
        """
        Returns commonly used university's webpage links
        :param siteName: webpage name, that was in the question
        :return: answer with link to asked site
        """
        if siteName == "course":
            return "Courses asub aadressil https://courses.cs.ut.ee/"
        elif siteName == "moodle":
            return "Moodle asub aadressil https://moodle.ut.ee/"
        elif siteName == "õis" or siteName == "õppeinfosüsteem":
            return "Tartu ülikooli ÕIS asub aadressil https://www.is.ut.ee/pls/ois_sso/tere.tulemast"
        elif siteName == "raamatukogu":
            return "Tartu ülikooli raamatukogu asub aadressil https://utlib.ut.ee/"
        elif siteName == "ester":
            return "Ester asub aadressil https://www.ester.ee/"
        elif siteName == "esileht":
            return "Tartu ülikooli esileht asub aadressil https://www.ut.ee/"
        return "Arendajad unustasid antud veebilehe lingi lisada või midagi läks valesti."

    def answerLecturers(self, courseIds):
        """
        Creates answer for lecturers question
        :param courseIds: asked courses
        :return: courses lecturers
        """
        results = []
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

    def answerWhatIsStructureCode(self, structureCode):
        """
        Creates an answer for a what is structure code question
        :param structureCode: structure code, that the client wants to know about
        :return: answer about the structure unit
        """
        json = oisStructuralUnits.getStructuralUnit(structureCode[0])
        return "Antud koodi kasutab struktuuriüksus: " + json["name"]["et"] + "."

    def answerWhatIsCourseCode(self, courseCode):
        json = oisCourses.coursesId(courseCode)
        return "Antud koodi kasutab kursus: " + json["name"]["et"] + "."

    def answerCourseEcts(self, courseId):
        """
        Creates an answer for questions about course ects.
        :param courseId: Courses which, were asked for
        :return: an answer
        """
        if len(courseId) == 1:
            json = oisCourses.coursesId(courseId[0])
            title = json["title"]["et"]
            if " " in title:
                return "Kursuse " + title + " maht on " + str(json["credits"]) + " eap."
            return self.synthesizeWord(title, "g").capitalize() + " maht on " + str(json["credits"]) + " eap."

        else:
            response = "Selle nimega on " + str(len(courseId)) + " erinevat kursust."
            json = oisCourses.coursesId(courseId[0])
            response += " " + courseId[0] + " mille maht on " + str(json["credits"]) + " eap"
            for i in courseId[1:-1]:
                json = oisCourses.coursesId(i)
                response += ", " + i + " mille maht on " + str(json["credits"]) + " eap"
            json = oisCourses.coursesId(courseId[-1])
            response += " ja " + courseId[-1] + " mille maht on " + str(json["credits"]) + " eap."
            return response

    def answerWhoYouAre(self):
        """
        Creates an answer for question who you are
        :return: Describtion of bot
        """
        return "Mina olen sõbralik Õis2 bot. Mina aitan sul saada vastust küsimustele, mis sind vaevavad."

    def answerCourseCode(self, courseId):
        """
        Creates an answer for questions about course code. like "mis on masinõppe ainekood"
        :param courseId: Courses which, were asked for
        :return: an answer with course code(s)
        """
        if len(courseId) == 1:
            id = courseId.pop()
            json = oisCourses.coursesId(id)
            title = json["title"]["et"]
            if " " in title:
                return "Kursuse " + title + " ainekood on " + id
            return self.synthesizeWord(title, "g").capitalize() + " ainekood on " + id
        else:
            response = "Selle nimega on " + str(len(courseId)) + " erinevat kursust. Nende ainekoodid on "
            for i in courseId[:-2]:
                response += i + ", "
            response += courseId[-2] + " ja "
            return response + courseId[-1] + "."

    def answerCoursePreReqs(self, courseId):
        """
        Creates an answer for question about prerequired courses
        :param courseId: Courses which, were asked for
        :return: An answer, that contains prerequired courses
        """
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

    def answerAuthMyNextCourse(self, questionWord):
        """
        answers a question about users next course
        :param questionWord: word we use to distinguish what the user wants
        :return: question to the question
        """
        return "Kahjuks ma ei saa teile vastata kuna te pole sisse logitud."


    def sayHello(self):
        greetings = ['Tere!', 'Hello!', 'Ahoi!', 'Tervitus!', 'Ära ehmata! Hommikust sullegi!',
                     '01010100 01100101 01110010 01100101 00001010', 'Tsau tsau!']
        return greetings[randint(0, len(greetings) - 1)]

    def synthesizeWord(self, word, f):
        """
        Changes the word's form without changing it form plural to singular or vice versa
        :param word: word to be formed
        :param f: desired form
        :return: word in desired form
        """
        # need to check if the title is plural or not.
        form = analyze(word)[0]["analysis"][0]["form"]
        return synthesize(word, form[:2] + " " + f, "S")[0]
