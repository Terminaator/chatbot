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



        #WHAT IS questions
        if self.isWhatIsQuestionAsked(currentLayer):
            if sUnits[wt.structureUnitCode] != "":
                self.askedQuestion = False
                return self.answerWhatIsStructureCode(sUnits[wt.structureUnitCode])



        #COURSES questions
        if len(courses[wt.courseID]) != 0:
            if courses[wt.ects]:
                self.askedQuestion = 0
                return self.answerCourseEcts(courses[wt.courseID])
            if courses[wt.courseCodeMentioned]:
                self.askedQuestion = 0
                return self.answerCourseCode(courses[wt.courseID])
            if courses[wt.preReqs]:
                self.askedQuestion = 0
                return self.answerCoursePreReqs(courses[wt.courseID])

            # If doesn't know what to answer
            subject = "kursuse"  # todo käänamine või panna kõik juba sobivasse käändesse
            possibleTopics = ["eelduaineid", "eapde arvu", "ainekoodi"]  # todo add words if you add questions



        if misc[wt.greeting]:
            self.askedQuestion = 0
            return self.sayHello()

        if misc[wt.questionWord] in ['mis', 'kes'] and misc[wt.pronoun] == 'sina' and 'olema' in misc[wt.verb]:
            self.askedQuestion = 0
            return self.answerWhoYouAre()

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
                misc : {questionWord: String, greeting: boolean, pronoun: String, verb: String}
                courses : {courseID: String, ects : boolean, preReqs : boolean, CourseCodeMentioned: boolean}
                structuralUnits: {structuralUnitCode: String}
            }
        }
        """
        misc = {wt.questionWord: "", wt.greeting: False, wt.pronoun: "", wt.verb: ""}
        courses = {wt.courseID: "", wt.ects: False, wt.preReqs: False, wt.courseCodeMentioned: False}
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

        return (misc[wt.questionWord] in ["mis"] and len(set(misc[wt.verb]).intersection({"tähendama", "olema"}))) != 0 and (sentence[2] == wt.structureUnitCode or sentence[2] == wt.courseID)

    def askExtraInfo(self, subject, possibleTopics):
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


    def answerWhatIsStructureCode(self, structureCode):
        """
        Creates an answer for a what is structure code question
        :param structureCode: structure code, that the client wants to know about
        :return: answer about the structure unit
        """
        json = oisStructuralUnits.getStructuralUnit(structureCode)
        return "Antud koodi kasutab struktuuriüksus: " + json["name"]["et"] + "."

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

    def sayHello(self):
        greetings = ['Tere!', 'Hello!', 'Ahoi!', 'Tervitus!', 'Ära ehmata! Hommikust sullegi!', '01010100 01100101 01110010 01100101 00001010', 'Tsau tsau!']
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