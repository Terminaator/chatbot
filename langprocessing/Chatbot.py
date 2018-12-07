# coding: utf-8
import langprocessing.SentenceProcesser as sentProc
from langprocessing.Data import Data
from langprocessing.WordTags import WordTag as wt
from langprocessing.questions import *
import random

class chatbot():
    def __init__(self):
        self.frames = {}
        self.currentFrame = -1
        self.sentenceProcessor = sentProc.SentenceProcessor()
        self.askedQuestion = 0
        self.inputSentence = ""
        self.hangman = Hangman.Hangman()
        self.possibleQuestions = [
            Courses.CourseQuestions(),
            StructureUnits.StructureUnitQuestions(),
            ImportantUniWebsites.ImportantUniWebsites(),
            HelpCommand.HelpCommand(),
            Greeting.Greeting(),
            Weather.Weather(),
            WhoAreYou.WhoAreYou(),
            WhatUp.WhatUp(),
            WhatIsQuestion.WhatIs(),
            RandomPost.RandomRedditFunnyPic(),
            RandomPost.RandomRedditJoke(),
            RandomPost.RandomXkcd(),
            VideoQuestion.VideoAnswers()
        ]
        self.authenticateQuestions = AuthenticationQuestion.Authenticate()
        self.possibleAuthQuestions = AuthenticationReqQuestions.AuthReqQuestions()

    def getResponse(self, inputSentence):
        """
        fills the frame and returns an answer
        :param inputSentence: Question that the client asked
        :return:A response for the client
        """
        words = self.sentenceProcessor.getWords(inputSentence)
        self.setInputSentence(inputSentence)
        self.addFrameLayer(words)
        return self.formDictionary(self.putTogetherAnAnswer())

    def formDictionary(self, answer):
        if isinstance(answer, dict):
            return answer
        return {"answer": answer}

    def putTogetherAnAnswer(self):
        """
        looks at the frame and questions based on that.
        :return: A response for the client
        """
        currentLayer = self.frames["layer " + str(self.currentFrame)]
        possibleTopics = []
        subject = ""
        print(self.authenticateQuestions.xToken)
        # Authentication
        if self.authenticateQuestions.authStepInProgress != 0:
            return self.authenticateQuestions.continueAuth(self.inputSentence)
        if self.authenticateQuestions.canAnswer(currentLayer):
            answer = self.authenticateQuestions.answer(currentLayer)
            if answer is not None:
                self.askedQuestion = 0
                return answer

        # Authentication req questions.
        for question in [self.possibleAuthQuestions]:
            if question.canAnswer(currentLayer):
                answer = question.answer(currentLayer, self.authenticateQuestions.xToken)
                if answer is not None:
                    self.askedQuestion = 0
                    return answer

        # games
        for game in [self.hangman]:
            if game.active:
                return game.createAnswer(self.inputSentence)
            elif game.canAnswer(currentLayer):
                return game.answer(currentLayer)

        # Simple questions
        for question in self.possibleQuestions:
            if question.canAnswer(currentLayer):
                answer = question.answer(currentLayer)
                if answer is not None:
                    self.askedQuestion = 0
                    return answer

        # Questions with memory
        for question in [Courses.CourseQuestions(), StructureUnits.StructureUnitQuestions()]:
            if question.canAnswer(currentLayer):
                possibleTopics = question.possibleTopics
                subject = question.subject

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
                if key in words:
                    layer[key] = words[key]
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
            if key in words:
                layer[key] = words[key]
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
                questionWord: String,
                pronoun: String,
                verb: String,
                timeWord; String,
                websiteName: String,
                about: String,
                weather: String,
                when: String,
                keywords: list,
                username: String,
                password: String,
                courseID: [String]
                structuralUnitCode: [String]
            }
        }
        """
        # , wt.greeting: False , wt.ects: False, wt.preReqs: False, wt.courseCodeMentioned: False
        layer = {wt.questionWord: "", wt.pronoun: "", wt.verb: "", wt.websiteName: "", wt.timeWord: "", wt.about: "",
                 wt.weather: "", wt.when: "", wt.keywords: [], wt.courseID: "", wt.structureUnitCode: "",
                 wt.sentence: [], wt.hangman: "", wt.what: ""}
        return layer

    def askExtraInfo(self, subject, possibleTopics):
        """
        Creates response if user asks question without sufficent informations
        :param subject: user asked question subject
        :param possibleTopics: What user can ask about that subject
        :return: response
        """
        result = "Mulle tundub, et sa tahtsid küsida infot " + subject + " kohta. " + subject.capitalize() + " kohta " \
                                                                                                             "saad " \
                                                                                                             "küsida "
        if len(possibleTopics) == 1:
            result += possibleTopics[0] + "."
        else:
            for i in possibleTopics[:-2]:
                result += i + ", "
            result += possibleTopics[-2] + " ja "
            result += possibleTopics[-1] + "."
        result += "\nPalun täpsusta!"
        return result

    def setInputSentence(self, sentence):
        """
        sets the user sentence to one of the class variable
        hangman game uses the user sentence to get all the chars and words inputted, nothing filtered out
        :param sentence: user sentence
        """
        self.inputSentence = sentence

    def getData(self):
        return Data(self.askedQuestion, self.frames, self.currentFrame, self.hangman.getData(), self.authenticateQuestions.getData())

    def setData(self, data):
        self.currentFrame = data.currentFrame
        self.frames = data.frames
        self.askedQuestion = data.askedQuestion
        self.hangman.setData(data.hangmanData)
        self.authenticateQuestions.setData(data.authData)
