from langprocessing.wordTags import WordTag as wt


class VideoAnswers:

    def canAnswer(self, layer):
        return wt.video in layer[wt.keywords]


    def answer(self, layer):
        return {"answer": "Rick Astley - Never Gonna Give You Up", "video": "https://www.youtube.com/embed/CFVPW6oV67s?autoplay=1&controls=0"}