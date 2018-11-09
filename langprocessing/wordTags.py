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
    timeWord = 8

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
    grade = 31
    course = 32 # if course word has been mentioned



    #Structure Units
    structureUnits = 40
    structureUnitCode = 41
    phone = 42
    email = 43
    address = 44

