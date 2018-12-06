import requests


def getRandomPost(subreddit: str):
    request = requests.get("https://www.reddit.com/r/" + subreddit + ".json", headers={'User-agent': 'SisBot 1.0'})
    statusCode = request.status_code
    if statusCode == 200:
        return request.json()
    raise Exception("reguest status code: ", statusCode)


def getRandomXkcd():
    request = requests.get("https://c.xkcd.com/random/comic/", headers={'User-agent': 'SisBot 1.0'})
    statusCode = request.status_code
    if statusCode == 200:
        request = requests.get(request.url + "info.0.json", headers={'User-agent': 'SisBot 1.0'})
        statusCode = request.status_code
        if statusCode == 200:
            return request.json()
    raise Exception("reguest status code: ", statusCode)
