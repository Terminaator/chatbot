from langprocessing.wordTags import WordTag as wt
import langprocessing.questions.answers.whatAnswers as wa
import oisbotServer.views.ois.courses as oisCourses
import oisbotServer.views.ois.structuralUnits as oisStructuralUnits



class WhatIs:
    def __init__(self):
        self.questions = [
            GeneralWhatQuestion(),
            StructCode(),
            CourseCode()
        ]

    def canAnswer(self, layer):
        """
        tries to see if user asked a "What is x" question
        :param currentLayer: currently used layer
        :return: Returns if client asked a term explanation question
        """
        sentence = layer[wt.sentence]
        if len(sentence) < 3:
            return False
        if sentence[1] != wt.verb or sentence[0] != wt.questionWord:
            return False
        return (layer[wt.questionWord] in ["mis", "mida"] and len(
            set(layer[wt.verb]).intersection({"tähendama", "olema"}))) != 0 and (
                       sentence[2] == wt.structureUnitCode or sentence[2] == wt.courseID or sentence[2] == wt.about or
                       sentence[2] == wt.verb)

    def answer(self, layer):
        for q in self.questions:
            if q.canAnswer(layer):
                return q.answer(layer)


class GeneralWhatQuestion:
    def canAnswer(self, layer):
        return layer[wt.about] != ""

    def answer(self, layer):
        """
                Answers general what questions about UT
                :param word: Job title that user asks from chatbot
                :param verbs: at the moment for later development
                :return: return answer if chatbot knows the answer, otherwise says that it does not know.
                """
        word = layer[wt.about]
        answer = wa.Answers
        try:
            a = answer.__getattribute__(answer, word)
        except AttributeError:
            a = "Ma ei tea mis " + word + " on."
        return a


class StructCode:
    def canAnswer(self, layer):
        return layer[wt.structureUnitCode] != ""

    def answer(self, layer):
        """
        Creates an answer for a what is structure code question
        :param structureCode: structure code, that the client wants to know about
        :return: answer about the structure unit
        """
        json = oisStructuralUnits.getStructuralUnit(layer[wt.structureUnitCode][0])
        return "Antud koodi kasutab struktuuriüksus: " + json["name"]["et"] + "."


class CourseCode:
    def canAnswer(self, layer):
        return layer[wt.structureUnitCode] != ""

    def answer(self, layer):
        """
        Creates an answer for what course has this structure code
        :param courseCode:
        :return:
        """
        json = oisCourses.coursesId(layer[wt.courseID])
        return "Antud koodi kasutab kursus: " + json["name"]["et"] + "."

