import requests
from bs4 import BeautifulSoup


def findMeaning(word):
    """
    Finds out what the word given means and returns what the word means according to eki dictionary.
    :param word: the word with no meaning
    :return: word meaning
    """
    page_response = requests.get("http://www.eki.ee/dict/ekss/index.cgi?Q=" + word + "&F=M", timeout=5)
    if page_response.status_code == 200:
        page_content = BeautifulSoup(page_response.content, "html.parser")
        meanings = [pt.get_text() for pt in page_content.find_all('span', class_="d")]
        if meanings == []:
            return "Mul pole halli aimugi, mida " + word + " tähendab. "
        inf = [pt.get_text() for pt in page_content.find_all('p', class_="inf")]
        if "Küsitud" in inf[0].split(" "):

            answerToSend = "Päris täpselt ei tea, aga võib-olla küsisid midagi siit: \n"

            founded = [pt.get_text() for pt in page_content.find_all('span', class_="leitud_ss")]
            defs = meanings
            meanings = [pt.get_text() for pt in page_content.find_all('span', class_=["leitud_ss", "d"])]

            for el in meanings:
                if el in defs:
                    answerToSend += el + ". "
                if el in founded:
                    answerToSend += el.capitalize() + " - "
            if founded == []:
                answerToSend = "Mul pole õrna aimugi, mis " + word + " üldse tähendada võiks. "
        else:
            answerToSend = "Minu arvates tähendab sõna " + word + " umbes seda: \n"
            for answer in meanings:
                answerToSend += answer + " "
        return answerToSend
    else:
        return []


