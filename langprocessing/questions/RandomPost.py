from langprocessing.WordTags import WordTag as wt
from oisbotServer.views.ois import misc
from random import randint



class RandomRedditJoke:

    def canAnswer(self, layer):
        return wt.randomJoke in layer[wt.keywords]


    def answer(self, layer):
        data = misc.getRandomPost("jokes")
        post = data["data"]["children"][randint(0, 24)]["data"]
        return post["title"] + "\n" + post["selftext"]


class RandomRedditFunnyPic:
    def canAnswer(self, layer):
        return wt.randomFunny in layer[wt.keywords]

    def answer(self, layer):
        data = misc.getRandomPost("funny")
        post = data["data"]["children"][randint(0, 24)]["data"]
        if post["url"].endswith(".jpg") or post["url"].endswith(".png"):
            return {"answer": post["title"], "img": post["url"]}
        return {"answer": "Software lifecycle", "img": "https://wisevishvesh.files.wordpress.com/2010/10/sdlc.jpg"}


class RandomXkcd:

    def canAnswer(self, layer):
        return wt.randomXkcd in layer[wt.keywords]


    def answer(self, layer):
        data = misc.getRandomXkcd()
        return {"answer": data["safe_title"], "img": data["img"]}