import requests


def req():
    r = requests.get('https://ois2.ut.ee/api/structural-units')
    print(r)
    return r