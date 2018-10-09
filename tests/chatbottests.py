import unittest
import langprocessing.chatbot as cbot
import langprocessing.sentenceProcesser as sentProc


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
        # words = {"questionWord": "mitu", "ects": True, "0": "on", "1": "kursus", "courseID": {"LTAT.05.005"}}
        words = "Mitu eap'd on kursus Tarkvaraprojekt?"
        self.assertEqual("Tarkvaraprojekti maht on 6 eap.", bot.getResponse(words))
        # words = {"questionWord": "mitu", "ects": True, "0": "on", "1": "kursus", "courseID": {"MTAT.03.263"}}
        words = "Mitu eap'd on kursus Arvutimängude loomine ja disain?"
        self.assertEqual("Kursuse Arvutimängude loomine ja disain maht on 6 eap.", bot.getResponse(words))

        # words = {"questionWord": "mis", "0": "on", "1": "kursuse", "courseID": {"LTAT.05.005"}, "2": "kood"}
        words = "Mis on kursuse Tarkvaraprojekt kood?"
        self.assertEqual("Tarkvaraprojekti ainekood on LTAT.05.005", bot.getResponse(words))
        # words = {"questionWord": "mis", "0": "on", "1": "kursuse", "courseID": {"MTAT.03.006}"}, "2": "kood"}
        words = "Mis on kursuse Programmeerimiskeeled kood?"
        self.assertEqual("Programmeerimiskeelte ainekood on MTAT.03.006", bot.getResponse(words))
        # words = {"questionWord": "mis", "0": "on", "1": "kursuse"e, "courseID": {"MTAT.03.263"}, "2": "kood"}
        words = "Mis on kursuse Arvutimängude loomine ja disain kood?"
        self.assertEqual("Kursuse Arvutimängude loomine ja disain ainekood on MTAT.03.263", bot.getResponse(words))

    def test_multipleCourseIdsWithSameName(self):
        bot = cbot.chatbot()
        sentence = "Mitu eap'd annab veebirakenduste loomise läbimine?"
        self.assertEqual("Selle nimega on 2 erinevat kursust. LTAT.05.004 mille maht on 6 eap ja P2NC.01.094 mille maht on 5 eap.", bot.getResponse(sentence))

        sentence = "Mis on veebirakenduste loomise ainekood."
        self.assertEqual("Selle nimega on 2 erinevat kursust. Nende ainekoodid on LTAT.05.004 ja P2NC.01.094.", bot.getResponse(sentence))


    def test_simpleGetWords(self):
        sentProcessor = sentProc.SentenceProcessor()
        self.assertEqual({'questionWord': "mitu", "ects": True, 0: "olema", 1: "aine", "courseID": ["LTAT.05.005"]},
                         sentProcessor.getWords("Mitu eap'd on aine Tarkvaraprojekt"))
        self.assertEqual({'questionWord': "mitu", "ects": True, 0: "olema", 1: "aine", "courseID": ["MTAT.03.263"]},
                         sentProcessor.getWords("Mitu eap'd on aine Arvutimängude loomine ja disain"))
        self.assertEqual(
            {'questionWord': "mitu", "ects": True, 0: "olema", 1: "aine", "courseID": ["LTAT.05.004", "P2NC.01.094"]},
            sentProcessor.getWords("Mitu eap'd on aine Veebirakenduste loomine"))


if __name__ == '__main__':
    unittest.main()
