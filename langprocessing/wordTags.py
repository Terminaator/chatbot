from enum import Enum, unique
@unique
class WordTag(Enum):

    sentence = -1

    #misc
    misc = 0
    questionWord = 1
    greeting = 2
    pronoun = 3
    verb = 4
    whatIsQuestionTargetWord = 5
    keywords = 6
    websiteName = 7

    #courses
    courses = 20
    courseID = 21
    ects = 22
    preReqs = 23
    courseCodeMentioned = 24
    language = 25
    website = 26
    lecturers = 27
    description = 28
    objective = 29
    courseCodeWords = 30


    #Structure Units
    structureUnits = 40
    structureUnitCode = 41

