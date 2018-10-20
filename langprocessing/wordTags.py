from enum import Enum, unique
@unique
class WordTag(Enum):

    sentence = -1

    #misc
    misc = 0
    questionWord = 1
    greeting = 2
    pronoun = 3

    #courses
    courses = 20
    courseID = 21
    ects = 22
    preReqs = 23
    courseCodeMentioned = 24

