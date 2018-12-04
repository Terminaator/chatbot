from random import randint
from langprocessing.wordTags import WordTag as wt
import  langprocessing.questions.answers.dictionary as d

class Hangman:
    def __init__(self):
        self.wordLen = randint(3, 31)
        self.dictionary = self.createDict()
        self.word = ""
        self.wordKnown = self.createWordKnown()
        self.guessedChars = []
        self.guessedRight = []

    def canAnswer(self, layer):
        """
        checks if this question is for this class
        :param layer: layer where to extract information
        :return: return boolean
        """
        return layer[wt.hangman] != ""

    def answer(self, layer):
        """
        Creates first answer to start the hangman game.
        :param layer: not used, because not needed, other questions require
        :return: returns first answer for the hangman game
        """
        return "HANGMAN", "Teretulemast mängu HANGMAN! \n Ülesanne on ülilihtne, sina pakud tähti ja mina ütlen, " \
                          "et seda tähte " \
                          "minu mõeldud sõnas ei ole. Okei, nali, kindlasti suudad mõne tähe ka ära arvata. Aga " \
                          "alustame. Paku täht või miks ma " \
                          "mitte terve sõna."

    def createAnswer(self, input):
        """
        Creates answer for the inputted char or word
        :param input: char or full word
        :return: answer and state of the game
        """
        input = input.strip()

        if len(input) == 1:
            if input in self.guessedChars:
                return False, "Oled juba tähte " + input + " pakkunud. Paku midagi muud. \nHetkel proovitud " + ' '.join(
                    self.guessedChars) + "\n" + self.wordKnown
            else:
                self.addChar(input)
                if self.isWordSet():
                    return self.answerIsSet(input)
                else:
                    self.filterDict(input)
                    if self.isWordSet():
                        return self.answerIsSet(input)
                    else:
                        return False, "Kahjuks tähte " + input + " sõnas ei ole. Vaja veel " + str(
                            self.wordKnown.count("_")) + " ära arvata. \nHetkel proovitud " + ' '.join(
                            self.guessedChars) + " \n" + self.wordKnown
        elif input == "":
            return False, "Võiks midagi ikka sisestada ka...\nHetkel proovitud " + ' '.join(
                self.guessedChars) + " \n" + self.wordKnown
        else:
            if self.word == input:
                return True, "Arvasid ära, mõtlesin tõesti sõna " + self.word + "."
            else:
                self.removeWordFromDict(input)
                return False, "Ei, ma kohe kindlasti ei mõelnud sõna " + input + "... Proovi veel. \nHetkel proovitud " \
                                                                                 "" \
                                                                                 "" \
                                                                                 "" + ' '.join(self.guessedChars) \
                       + " \n" + self.wordKnown

    def answerIsSet(self, input):
        """
        Now when word is set, then we can check if inputted chars are in this word.
        :param input: char or word.
        :return: returns answer and bool (guessed right or not)
        """
        if input in self.word:
            self.guessedRight.append(input)
            self.setWordKnown()
            if "_" not in self.wordKnown:
                return True, "Kaua läks, aga asja sai. Arvasid ära, sõna on tõesti " + self.wordKnown + "."
            return False, "Täht " + input + " on tõesti sõnas sees. Tubli. Veel on vaja arvata " + str(
                self.wordKnown.count("_")) + " tähte\n" + "Hetkel proovitud " + ' '.join(
                self.guessedChars) + "\n" + self.wordKnown
        return False, "Kahjuks tähte " + input + " sõnas ei ole. Vaja veel " + str(
            self.wordKnown.count("_")) + " ära arvata. \nHetkel proovitud " + ' '.join(
            self.guessedChars) + " \n" + self.wordKnown

    def removeWordFromDict(self, word):
        """
        if somehow the user inputted word is in the dictionary then exclude it from the dictionary
        :param word:
        """
        if word in self.getCurDict():
            self.setDict(self.getCurDict().remove(word))

    def checkChar(self, char):
        """
        checks if inputted char is in the already guessed chars
        :param char: user input
        :return: boolean value
        """
        return char not in self.guessedChars

    def addChar(self, char):
        """
        adds user inputted char to the guessed chars
        :param char: user input
        """
        self.guessedChars.append(char)

    def setWord(self, word):
        """
        sets the word to be guessed
        :param word:
        """
        self.word = word

    def isWordSet(self):
        """
        returns if the word to be guessed is set or not
        :return:
        """
        return len(self.getWord()) != 0

    def getWord(self):
        """
        returns the word what to guess
        :return: word to be guessed
        """
        return self.word

    def setWordKnown(self):
        """
        sets the word with '_' that the user has guessed so far
        :param char: user input
        """
        self.wordKnown = ''.join(['_ ' if w not in self.guessedRight else w for w in self.getWord()])

    def getCurDict(self):
        """
        :return: current dictionary
        """
        return self.dictionary

    def setDict(self, newDict):
        """
        sets new dictionary
        :param newDict: new dictionary
        """
        self.dictionary = newDict

    def setNewLen(self):
        """
        if there is no word with randomly selected length then set new random word length
        """
        self.wordLen = randint(3, 31)

    def createDict(self):
        """
        creates dictionary from iputfile, filters out all the words that are not the right length
        :return: returns all the words that the game choses the final word to be guessed
        """
        data = d.Dictionary.dictionary
        while True:
            filtered = [line.strip() for line in data if len(line) == self.wordLen]
            if len(filtered) == 0:
                self.setNewLen()
            else:
                break
        return filtered

    def filterDict(self, char):
        """
        filters the dictionary, takes out all the words that do not contain the inputted char from user
        :param char: user input
        """
        newDict = [word for word in self.getCurDict() if char not in word.lower()]
        if len(newDict) < 5:
            dictlen = len(self.getCurDict())
            word = self.getCurDict()[randint(0, dictlen - 1)]
            self.setWord(word)
        else:
            self.setDict(newDict)

    def createWordKnown(self):
        """
        creates the inital string that only contains '_'
        :return: returns the hidden word that the user has to guess
        """
        return ''.join(['_ ' for m in range(self.wordLen)])
