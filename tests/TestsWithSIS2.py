import unittest
import langprocessing.Chatbot as cbot
import langprocessing.SentenceProcesser as sentProc
from langprocessing.WordTags import WordTag as wt


class TestSimpleRequests(unittest.TestCase):

    def testSimpleCourseQuestions(self):
        bot = cbot.chatbot()
        # words = {"questionWord": "mitu", "ects": True, "0": "on", "1": "kursus", "courseID": {"LTAT.05.005"}}
        words = "Mitu eap'd on kursus Tarkvaraprojekt?"
        self.assertEqual("Tarkvaraprojekti maht on 6 EAP.", bot.getResponse(words)["answer"])
        # words = {"questionWord": "mitu", "ects": True, "0": "on", "1": "kursus", "courseID": {"MTAT.03.263"}}
        words = "Mitu eap'd on kursus Arvutimängude loomine ja disain?"
        self.assertEqual("Kursuse Arvutimängude loomine ja disain maht on 6 EAP.", bot.getResponse(words)["answer"])

        # words = {"questionWord": "mis", "0": "on", "1": "kursuse", "courseID": {"LTAT.05.005"}, "2": "kood"}
        words = "Mis on kursuse Tarkvaraprojekt kood?"
        self.assertEqual("Tarkvaraprojekti ainekood on LTAT.05.005", bot.getResponse(words)["answer"])
        # words = {"questionWord": "mis", "0": "on", "1": "kursuse", "courseID": {"MTAT.03.006}"}, "2": "kood"}
        words = "Mis on kursuse Programmeerimiskeeled kood?"
        self.assertEqual("Programmeerimiskeelte ainekood on MTAT.03.006", bot.getResponse(words)["answer"])
        # words = {"questionWord": "mis", "0": "on", "1": "kursuse"e, "courseID": {"MTAT.03.263"}, "2": "kood"}
        words = "Mis on kursuse Arvutimängude loomine ja disain kood?"
        self.assertEqual("Kursuse Arvutimängude loomine ja disain ainekood on MTAT.03.263",
                         bot.getResponse(words)["answer"])

        sentence = "mis on Programmeerimiskeelte eeldusained"
        self.assertEqual(
            "Selle kursuse eeldusaine on LTAT.03.005 \"Algoritmid ja andmestruktuurid\" või MTAT.03.133 \"Algoritmid "
            "ja andmestruktuurid\".",
            bot.getResponse(sentence)["answer"])
        sentence = "mis on Tarkvaraprojekti eeldusained"
        self.assertEqual("Sellel kursusel pole eeldusaineid.", bot.getResponse(sentence)["answer"])
        sentence = "mis on veebirakenduste loomise eeldusained"
        self.assertEqual(
            "Selle nimega on 2 erinevat kursust. Kursuse LTAT.05.004 eeldusaine on LTAT.03.003 \"Objektorienteeritud "
            "programmeerimine\" või MTAT.03.130 \"Objektorienteeritud programmeerimine\" Kursusel P2NC.01.094 "
            "eeldusained puuduvad.",
            bot.getResponse(sentence)["answer"])

    def testWhatisQuestions(self):
        bot = cbot.chatbot()
        sentence = "mida tähendab MTAT?"
        self.assertEqual("Antud koodi kasutab struktuuriüksus: arvutiteaduse instituut.",
                         bot.getResponse(sentence)["answer"])
        sentence = "mis on MTAT?"
        self.assertEqual("Antud koodi kasutab struktuuriüksus: arvutiteaduse instituut.",
                         bot.getResponse(sentence)["answer"])

    def testMultipleCourseIdsWithSameName(self):
        bot = cbot.chatbot()
        sentence = "Mitu eap'd annab veebirakenduste loomise läbimine?"
        self.assertEqual(
            "Selle nimega on 2 erinevat kursust. LTAT.05.004 mille maht on 6 EAP ja P2NC.01.094 mille maht on 5 EAP.",
            bot.getResponse(sentence)["answer"])

        sentence = "Mis on veebirakenduste loomise ainekood."
        self.assertEqual("Selle nimega on 2 erinevat kursust. Nende ainekoodid on LTAT.05.004 ja P2NC.01.094.",
                         bot.getResponse(sentence)["answer"])

    def testStructureUnitWebSite(self):
        bot = cbot.chatbot()
        sentence = "mis on matemaatika instituudi veebileht"
        self.assertEqual(
            "Selle struktuuriüksuse veebileht asub aadressil http://www.math.ut.ee/mm",
            bot.getResponse(sentence)["answer"])
        sentence = "mis on KKKE veebileht"
        self.assertEqual(
            "Sain küsimusest valesti aru või küsitud struktuuriüksusel ei ole veebilehte.",
            bot.getResponse(sentence)["answer"])

    def test_getStructureUnitCodes(self):
        sentProcessor = sentProc.SentenceProcessor()
        self.assertEqual({1: [], wt.what: [], wt.structureUnitCode: ['ltat'], wt.numbers: []}, sentProcessor.getWords("LTAT"))
        self.assertEqual({1: [], wt.what: [], wt.structureUnitCode: ['bgom01', 'loom01', 'ltom01'], wt.numbers: []},
                         sentProcessor.getWords("Botaanika osakond"))

    def testExtraQuestions(self):
        bot = cbot.chatbot()
        sentence = "Anna infot tarkvaraprojekti kohta?"
        self.assertTrue(bot.getResponse(sentence)["answer"].startswith(
            "Mulle tundub, et sa tahtsid küsida infot kursuse kohta. Kursuse kohta saad küsida"))
        sentence = "eap"
        self.assertEqual("Tarkvaraprojekti maht on 6 EAP.", bot.getResponse(sentence)["answer"])

        sentence = "Anna infot tarkvaraprojekti kohta?"
        self.assertTrue(bot.getResponse(sentence)["answer"].startswith(
            "Mulle tundub, et sa tahtsid küsida infot kursuse kohta. Kursuse kohta saad küsida"))
        sentence = "django on jama"
        self.assertEqual("Kahjuks ma ei saanud teist aru.", bot.getResponse(sentence)["answer"])

    def testExtraQuestions2(self):
        bot = cbot.chatbot()
        sentence = "Anna infot tarkvaraprojekti kohta?"
        self.assertTrue(bot.getResponse(sentence)["answer"].startswith(
            "Mulle tundub, et sa tahtsid küsida infot kursuse kohta. Kursuse kohta saad küsida"))
        sentence = "Mitu eap'd annab veebirakenduste loomise läbimine?"
        self.assertEqual(
            "Selle nimega on 2 erinevat kursust. LTAT.05.004 mille maht on 6 EAP ja P2NC.01.094 mille maht on 5 EAP.",
            bot.getResponse(sentence)["answer"])

    def testLanguageQuestion(self):
        bot = cbot.chatbot()
        sentence = "Mis keeles õpetatakse ainet tarkvaraprojekt?"
        self.assertEqual("Aine Tarkvaraprojekt(LTAT.05.005) on inglise keeles.", bot.getResponse(sentence)["answer"])

    def testWebsiteQuestion(self):
        bot = cbot.chatbot()
        sentence = "Mis on tarkvaraprojekti koduleht?"
        self.assertEqual("Aine Tarkvaraprojekt(LTAT.05.005) veebileht on https://courses.cs.ut.ee/",
                         bot.getResponse(sentence)["answer"])

    def testLecturersQuestion(self):
        bot = cbot.chatbot()
        sentence = "Kes on tarkvaraprojekti õppejõud?"
        self.assertEqual(
            "Aine Tarkvaraprojekt(LTAT.05.005) vastutav õppejõud on Marlon Gerardo Dumas Menjivar.\nTeised õppejõud "
            "on Jaanus Jaggo, Mykhailo Dorokhov",
            bot.getResponse(sentence)["answer"])

    def testDescriptionQuestion(self):
        bot = cbot.chatbot()
        sentence = "Mis on tarkvaraprojekti kirjeldus?"
        self.assertTrue(
            bot.getResponse(sentence)["answer"].startswith(
                "Aine Tarkvaraprojekt(LTAT.05.005) kirjeldus:\nTarkvara arendustöö"))

    def testObjectiveQuestion(self):
        bot = cbot.chatbot()
        sentence = "Mis on tarkvaraprojekti eesmärk?"
        self.assertTrue(
            bot.getResponse(sentence)["answer"].startswith(
                "Aine Tarkvaraprojekt(LTAT.05.005) eesmärk:\nKursuse eesmärgiks"))

    def testPhoneSUQuestion(self):
        bot = cbot.chatbot()
        sentence = "Mis on LTAT telefoninumber?"
        self.assertEqual(
            "Arvutiteaduse instituudi(LTAT) telefoni number on +372 737 5445.",
            bot.getResponse(sentence)["answer"])

    def testEmailSUQuestion(self):
        bot = cbot.chatbot()
        sentence = "Mis on LTAT email?"
        self.assertEqual(
            "Arvutiteaduse instituudi(LTAT) email on ics@ut.ee.",
            bot.getResponse(sentence)["answer"])

    def testAddressSUQuestion(self):
        bot = cbot.chatbot()
        sentence = "Kus asub LTAT?"
        self.assertEqual(
            "Arvutiteaduse instituudi(LTAT) aadress on J. Liivi 2, Tartu linn.",
            bot.getResponse(sentence)["answer"])

    def testGradeQuestion(self):
        bot = cbot.chatbot()
        sentence = "Milline on Tarkvaratehnika hindamine?"
        self.assertTrue(
            bot.getResponse(sentence)["answer"].startswith(
                "Aine Tarkvaratehnika(LTAT.05.003) hindamine on Eristav (A, B, C, D, E, F, mi)"))


if __name__ == '__main__':
    unittest.main()
