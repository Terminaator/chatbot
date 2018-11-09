import unittest
import langprocessing.chatbot as cbot
import langprocessing.sentenceProcesser as sentProc
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

        sentence = "mis on Programmeerimiskeelte eeldusained"
        self.assertEqual(
            "Selle kursuse eeldusaine on LTAT.03.005 \"Algoritmid ja andmestruktuurid\" või MTAT.03.133 \"Algoritmid ja andmestruktuurid\".",
            bot.getResponse(sentence))
        sentence = "mis on Tarkvaraprojekti eeldusained"
        self.assertEqual("Sellel kursusel pole eeldusaineid.", bot.getResponse(sentence))
        sentence = "mis on veebirakenduste loomise eeldusained"
        self.assertEqual(
            "Selle nimega on 2 erinevat kursust. Kursuse LTAT.05.004 eeldusaine on LTAT.03.003 \"Objektorienteeritud programmeerimine\" või MTAT.03.130 \"Objektorienteeritud programmeerimine\" Kursusel P2NC.01.094 eeldusained puuduvad.",
            bot.getResponse(sentence))

    def test_whatisQuestions(self):
        bot = cbot.chatbot()
        sentence = "mida tähendab MTAT?"
        self.assertEqual("Antud koodi kasutab struktuuriüksus: arvutiteaduse instituut.", bot.getResponse(sentence))
        sentence = "mis on MTAT?"
        self.assertEqual("Antud koodi kasutab struktuuriüksus: arvutiteaduse instituut.", bot.getResponse(sentence))

    def test_multipleCourseIdsWithSameName(self):
        bot = cbot.chatbot()
        sentence = "Mitu eap'd annab veebirakenduste loomise läbimine?"
        self.assertEqual(
            "Selle nimega on 2 erinevat kursust. LTAT.05.004 mille maht on 6 eap ja P2NC.01.094 mille maht on 5 eap.",
            bot.getResponse(sentence))

        sentence = "Mis on veebirakenduste loomise ainekood."
        self.assertEqual("Selle nimega on 2 erinevat kursust. Nende ainekoodid on LTAT.05.004 ja P2NC.01.094.",
                         bot.getResponse(sentence))

    def test_structureUnitWebSite(self):
        bot = cbot.chatbot()
        sentence = "mis on matemaatika instituudi veebileht"
        self.assertEqual(
            "Selle struktuuriüksuse veebileht asub aadressil http://www.math.ut.ee/mm",
            bot.getResponse(sentence))
        sentence = "mis on KKKE veebileht"
        self.assertEqual(
            "Sain küsimusest valesti aru või küsitud struktuuriüksusel ei ole veebilehte.",
            bot.getResponse(sentence))


    def test_simpleGetWords(self):
        sentProcessor = sentProc.SentenceProcessor()
        self.assertEqual(
            {wt.questionWord: "mitu", wt.keywords: [wt.ects], wt.verb: ["olema"], 0: "mitu", 1: "eap", 2: "aine",
             wt.courseID: ["LTAT.05.005"]},
            sentProcessor.getWords("Mitu eap'd on aine Tarkvaraprojekt"))
        self.assertEqual(
            {wt.questionWord: "mitu", wt.keywords: [wt.ects], wt.verb: ["olema"], 0: "mitu", 1: "eap", 2: "aine",
             wt.courseID: ["MTAT.03.263"]},
            sentProcessor.getWords("Mitu eap'd on aine Arvutimängude loomine ja disain"))
        self.assertEqual(
            {wt.questionWord: "mitu", wt.keywords: [wt.ects], wt.verb: ["olema"], 0: "mitu", 1: "eap", 2: "aine",
             wt.courseID: ["LTAT.05.004", "P2NC.01.094"]},
            sentProcessor.getWords("Mitu eap'd on aine Veebirakenduste loomine"))

        self.assertEqual({wt.keywords: [wt.courseCodeMentioned, wt.preReqs], 0: 'ainekood', 1: 'eeldusaine'},
                         sentProcessor.getWords("ainekood eeldusained"))

    def test_getStructureUnitCodes(self):
        sentProcessor = sentProc.SentenceProcessor()
        self.assertEqual({wt.structureUnitCode: ['ltat']}, sentProcessor.getWords("LTAT"))
        self.assertEqual({wt.structureUnitCode: ['bgom01', 'loom01', 'ltom01']},
                         sentProcessor.getWords("Botaanika osakond"))

    def test_ExtraQuestions(self):
        bot = cbot.chatbot()
        sentence = "Anna infot tarkvaraprojekti kohta?"
        self.assertTrue(bot.getResponse(sentence).startswith("Mulle tundub, et sa tahtsid küsida infot kursuse kohta. Kursuse kohta saad küsida"))
        sentence = "eap"
        self.assertEqual("Tarkvaraprojekti maht on 6 eap.", bot.getResponse(sentence))

        sentence = "Anna infot tarkvaraprojekti kohta?"
        self.assertTrue(bot.getResponse(sentence).startswith(
            "Mulle tundub, et sa tahtsid küsida infot kursuse kohta. Kursuse kohta saad küsida"))
        sentence = "django on jama"
        self.assertEqual("Kahjuks ma ei saanud teist aru.", bot.getResponse(sentence))

    def test_ExtraQuestions2(self):
        bot = cbot.chatbot()
        sentence = "Anna infot tarkvaraprojekti kohta?"
        self.assertTrue(bot.getResponse(sentence).startswith(
            "Mulle tundub, et sa tahtsid küsida infot kursuse kohta. Kursuse kohta saad küsida"))
        sentence = "Mitu eap'd annab veebirakenduste loomise läbimine?"
        self.assertEqual(
            "Selle nimega on 2 erinevat kursust. LTAT.05.004 mille maht on 6 eap ja P2NC.01.094 mille maht on 5 eap.",
            bot.getResponse(sentence))

    def test_languageQuestion(self):
        bot = cbot.chatbot()
        sentence = "Mis keeles õpetatakse ainet tarkvaraprojekt?"
        self.assertEqual("Aine Tarkvaraprojekt(LTAT.05.005) on inglise keeles.", bot.getResponse(sentence))

    def test_websiteQuestion(self):
        bot = cbot.chatbot()
        sentence = "Mis on tarkvaraprojekti koduleht?"
        self.assertEqual("Aine Tarkvaraprojekt(LTAT.05.005) veebileht on https://courses.cs.ut.ee/",
                         bot.getResponse(sentence))

    def test_importantUniWebSite(self):
        #NOTE: This question doesn't require ÕIS 2.0 API
        bot = cbot.chatbot()
        sentence = "Mis on moodle link?"
        self.assertEqual("Moodle asub aadressil https://moodle.ut.ee/", bot.getResponse(sentence))
        sentence = "Mis on estri link?"
        self.assertEqual("Ester asub aadressil https://www.ester.ee/", bot.getResponse(sentence))
        sentence = "Mis on courses link?"
        self.assertEqual("Courses asub aadressil https://courses.cs.ut.ee/", bot.getResponse(sentence))


    def test_lecturersQuestion(self):
        bot = cbot.chatbot()
        sentence = "Kes on tarkvaraprojekti õppejõud?"
        self.assertEqual(
            "Aine Tarkvaraprojekt(LTAT.05.005) vastutav õppejõud on Marlon Gerardo Dumas Menjivar.\nTeised õppejõud on Jaanus Jaggo, Mykhailo Dorokhov",
            bot.getResponse(sentence))

    def test_descriptionQuestion(self):
        bot = cbot.chatbot()
        sentence = "Mis on tarkvaraprojekti kirjeldus?"
        self.assertTrue(
            bot.getResponse(sentence).startswith("Aine Tarkvaraprojekt(LTAT.05.005) kirjeldus:\nTarkvara arendustöö"))

    def test_objectiveQuestion(self):
        bot = cbot.chatbot()
        sentence = "Mis on tarkvaraprojekti eesmärk?"
        self.assertTrue(
            bot.getResponse(sentence).startswith("Aine Tarkvaraprojekt(LTAT.05.005) eesmärk:\nKursuse eesmärgiks"))

    def test_phoneSUQuestion(self):
        bot = cbot.chatbot()
        sentence = "Mis on LTAT telefoninumber?"
        self.assertEqual(
            "Arvutiteaduse instituudi telefoni number on (+372) 737 5445.",
            bot.getResponse(sentence))

    def test_emailSUQuestion(self):
        bot = cbot.chatbot()
        sentence = "Mis on LTAT email?"
        self.assertEqual(
            "Arvutiteaduse instituudi email on ics@ut.ee.",
            bot.getResponse(sentence))

    def test_addressSUQuestion(self):
        bot = cbot.chatbot()
        sentence = "Kus asub LTAT?"
        self.assertEqual(
            "Arvutiteaduse instituudi aadress on J. Liivi 2, Tartu linn.",
            bot.getResponse(sentence))

    def test_gradeQuestion(self):
        bot = cbot.chatbot()
        sentence = "Milline on Tarkvaratehnika hindamine?"
        self.assertTrue(
            bot.getResponse(sentence).startswith("Aine Tarkvaratehnika(LTAT.05.003) hindamine on Eristav (A, B, C, D, E, F, mi)"))

if __name__ == '__main__':
    unittest.main()
