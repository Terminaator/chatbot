import requests


def req():
    r = requests.get('https://ois2.ut.ee/api/courses/LTAT.05.005')
    print(r.json())
    return r

req()