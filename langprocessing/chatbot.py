import views.ois.courses as oisCourses
from estnltk.vabamorf.morf import synthesize, analyze
import langprocessing.sentenceProcesser as sentProc


class chatbot():
    def __init__(self):
        self.frames = {}
        self.currentFrame = -1
        self.sentenceProcessor = sentProc.SentenceProcessor()

    def getResponse(self, inputSentence):
        words = self.sentenceProcessor.getWords(inputSentence)
        # words = inputSentence  # TODO: remove this line once sentenceProcesser is ready
        self.addFrameLayer(words)
        return self.putTogetherAnAnswer()

    def putTogetherAnAnswer(self):
        currentLayer = self.frames["layer " + str(self.currentFrame)]
        misc = currentLayer["misc"]
        courses = currentLayer["courses"]

        if len(courses["courseID"]) != 0:
            if courses["ects"]:
                return self.answerCourseEcts(courses["courseID"])
            if misc["questionWord"] == "mis":
                return self.answerCourseCode(courses["courseID"])

        return "Kahjuks ma ei saanud teist aru."

    def addFrameLayer(self, words):
        """
        creates a new frame layer
        :param words:  dictionary of words to be added to the new frame layer
        """
        self.currentFrame += 1
        self.frames["layer " + str(self.currentFrame)] = self.fillFrameLayer(words)

    def fillFrameLayer(self, words):
        """
        fills a frame layer
        :param words: dictionary of words to be added to the layer
        :return: filled frame layer
        """
        layer = self.createEmptyLayer()
        for key in layer:
            for k in layer[key]:
                if (k in words):
                    layer[key][k] = words[k]
        return layer

    def createEmptyLayer(self):
        """
        Creates a layer for frame
        Frame with 1 layer structure
        frame = {
            layer 0: {
                misc : {questionWord: String}
                courses : {courseID: String, ects : boolean}
            }
        }
        """
        misc = {"questionWord": ""}
        courses = {"courseID": "", "ects": False}
        layer = {"misc": misc, "courses": courses}
        return layer

    def answerCourseEcts(self, courseId):
        json = oisCourses.coursesId(courseId)
        title = json["title"]["et"]
        if " " in title:
            return "Kursuse " + title + " maht on " + str(json["credits"]) + " eap."
        return self.synthesizeWord(title, "g").capitalize() + " maht on " + str(json["credits"]) + " eap."

    def answerCourseCode(self, courseId):
        json = oisCourses.coursesId(courseId)
        title = json["title"]["et"]
        if " " in title:
            return "Kursuse " + title + " ainekood on " + courseId
        return self.synthesizeWord(title, "g").capitalize() + " ainekood on " + courseId

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