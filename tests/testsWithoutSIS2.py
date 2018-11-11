# coding: utf-8
import unittest
from langprocessing import chatbot as cbot
from langprocessing import sentenceProcesser as sentProc
from langprocessing.wordTags import WordTag as wt


class TestSimpleRequests(unittest.TestCase):

    def test_fillFrameLayer(self):
        bot = cbot.chatbot()
        words = {wt.questionWord: "mitu", wt.keywords: [wt.ects], wt.courseID: "LTAT.05.005"}

        expectedLayer = bot.createEmptyLayer()
        expectedLayer[wt.sentence] = [wt.questionWord, wt.keywords, wt.courseID]
        expectedLayer[wt.misc][wt.questionWord] = "mitu"
        expectedLayer[wt.courses][wt.courseID] = "LTAT.05.005"
        expectedLayer[wt.misc][wt.keywords] = [wt.ects]
        actualLayer = bot.fillFrameLayer(words)

        self.assertEqual(expectedLayer, actualLayer)

    def test_frame(self):
        bot = cbot.chatbot()

        layer0 = bot.createEmptyLayer()
        layer1 = bot.createEmptyLayer()
        layer2 = bot.createEmptyLayer()

        layer0[wt.sentence] = [wt.courseID]
        layer1[wt.sentence] = [wt.keywords, wt.courseID]
        layer2[wt.sentence] = [wt.questionWord, wt.keywords, wt.courseID]

        layer0[wt.courses][wt.courseID] = "LTAT.05.005"
        layer1[wt.courses][wt.courseID] = "LTAT.05.005"
        layer2[wt.courses][wt.courseID] = "LTAT.05.005"

        layer1[wt.misc][wt.keywords] = [wt.ects]
        layer2[wt.misc][wt.keywords] = [wt.ects]

        layer2[wt.misc][wt.questionWord] = "mitu"

        expectedFrames = {"layer 0": layer0, "layer 1": layer1, "layer 2": layer2}

        words = {wt.courseID: "LTAT.05.005"}
        bot.addFrameLayer(words)
        words = {wt.keywords: [wt.ects], wt.courseID: "LTAT.05.005"}
        bot.addFrameLayer(words)
        words = {wt.questionWord: "mitu", wt.keywords: [wt.ects], wt.courseID: "LTAT.05.005"}
        bot.addFrameLayer(words)

        self.assertEqual(expectedFrames, bot.frames)

    def test_importantUniWebSite(self):
        #NOTE: This question doesn't require ÕIS 2.0 API
        bot = cbot.chatbot()
        sentence = "Mis on moodle link?"
        self.assertEqual("Moodle asub aadressil https://moodle.ut.ee/", bot.getResponse(sentence))
        sentence = "Mis on estri link?"
        self.assertEqual("Ester asub aadressil https://www.ester.ee/", bot.getResponse(sentence))
        sentence = "Mis on courses link?"
        self.assertEqual("Courses asub aadressil https://courses.cs.ut.ee/", bot.getResponse(sentence))


    def test_simpleGetWords(self):
        sentProcessor = sentProc.SentenceProcessor()
        self.assertEqual(
            {wt.questionWord: "mitu", wt.keywords: [wt.ects, wt.course], wt.verb: ["olema"], 0: "mitu", 1: "eap", 2: "aine",
             wt.courseID: ["LTAT.05.005"]},
            sentProcessor.getWords("Mitu eap'd on aine Tarkvaraprojekt"))
        self.assertEqual(
            {wt.questionWord: "mitu", wt.keywords: [wt.ects, wt.course], wt.verb: ["olema"], 0: "mitu", 1: "eap", 2: "aine",
             wt.courseID: ["MTAT.03.263"]},
            sentProcessor.getWords("Mitu eap'd on aine Arvutimängude loomine ja disain"))
        self.assertEqual(
            {wt.questionWord: "mitu", wt.keywords: [wt.ects, wt.course], wt.verb: ["olema"], 0: "mitu", 1: "eap", 2: "aine",
             wt.courseID: ["LTAT.05.004", "P2NC.01.094"]},
            sentProcessor.getWords("Mitu eap'd on aine Veebirakenduste loomine"))

        self.assertEqual({wt.keywords: [wt.courseCodeMentioned, wt.preReqs], 0: 'ainekood', 1: 'eeldusaine'},
                         sentProcessor.getWords("ainekood eeldusained"))



if __name__ == '__main__':
    unittest.main()