import unittest
import langprocessing.chatbot as cbot


class TestSimpleRequests(unittest.TestCase):

    def test_fillFrameLayer(self):
        bot = cbot.chatbot()
        words = {"questionWord": "mitu", "ects": True, "courseID": "LTAT.05.005"}

        expectedLayer = bot.createEmptyLayer()
        expectedLayer["misc"]["questionWord"] = "mitu"
        expectedLayer["courses"]["courseID"] = "LTAT.05.005"
        expectedLayer["courses"]["ects"] = True
        actualLayer = bot.fillFrameLayer(words)

        self.assertEqual(expectedLayer, actualLayer)

    def test_frame(self):
        bot = cbot.chatbot()

        layer0 = bot.createEmptyLayer()
        layer1 = bot.createEmptyLayer()
        layer2 = bot.createEmptyLayer()

        layer0["courses"]["courseID"] = "LTAT.05.005"
        layer1["courses"]["courseID"] = "LTAT.05.005"
        layer2["courses"]["courseID"] = "LTAT.05.005"

        layer1["courses"]["ects"] = True
        layer2["courses"]["ects"] = True

        layer2["misc"]["questionWord"] = "mitu"

        expectedFrames = {"layer 0": layer0, "layer 1": layer1, "layer 2": layer2}

        words = {"courseID": "LTAT.05.005"}
        bot.addFrameLayer(words)
        words = {"ects": True, "courseID": "LTAT.05.005"}
        bot.addFrameLayer(words)
        words = {"questionWord": "mitu", "ects": True, "courseID": "LTAT.05.005"}
        bot.addFrameLayer(words)

        self.assertEqual(expectedFrames, bot.frames)

    def test_simpleCourseQuestions(self):
        bot = cbot.chatbot()
        #TODO: change the words dict to normal sentence once sentenceProcesser is ready
        words = {"questionWord": "mitu", "ects": True, "0": "on", "1": "kursus", "courseID": "LTAT.05.005"}
        self.assertEqual("Tarkvaraprojekti maht on 6 eap.", bot.getResponse(words))
        words = {"questionWord": "mitu", "ects": True, "0": "on", "1": "kursus", "courseID": "MTAT.03.263"}
        self.assertEqual("Kursuse Arvutimängude loomine ja disain maht on 6 eap.", bot.getResponse(words))

        words = {"questionWord": "mis", "0": "on", "1": "kursuse", "courseID": "LTAT.05.005", "2": "kood"}
        self.assertEqual("Tarkvaraprojekti ainekood on LTAT.05.005", bot.getResponse(words))
        words = {"questionWord": "mis", "0": "on", "1": "kursuse", "courseID": "MTAT.03.006", "2": "kood"}
        self.assertEqual("Programmeerimiskeelte ainekood on MTAT.03.006", bot.getResponse(words))
        words = {"questionWord": "mis", "0": "on", "1": "kursuse", "courseID": "MTAT.03.263", "2": "kood"}
        self.assertEqual("Kursuse Arvutimängude loomine ja disain ainekood on MTAT.03.263", bot.getResponse(words))



if __name__ == '__main__':
    unittest.main()
