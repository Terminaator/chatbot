# coding: utf-8
import unittest
from langprocessing import chatbot as cbot
from langprocessing import sentenceProcesser as sentProc
from langprocessing.wordTags import WordTag as wt

class TestSimpleRequests(unittest.TestCase):
    def test(self):
        self.assertEqual("k", "k")


if __name__ == '__main__':
    unittest.main()
