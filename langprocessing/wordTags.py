from enum import Enum, unique
@unique
class WordTag(Enum):

    sentence = -1

    #misc
    questionWord = 1
    greeting = 2
    pronoun = 3
    verb = 4
    whatIsQuestionTargetWord = 5
    keywords = 6
    websiteName = 7
    timeWord = 8
    help = 9
    about = 10
    wordNew = 11 # word "uus" has been mentioned
    numbers = 12
    weather = 13
    when = 14
    randomJoke = 15
    randomFunny = 16
    randomXkcd = 17


    #courses
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
    structureUnitCode = 41
    phone = 42
    email = 43
    address = 44

    #User
    notifications = 61
