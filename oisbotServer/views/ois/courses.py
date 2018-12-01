import requests

def coursesId(id):
    request = requests.get('https://ois2dev.ut.ee/api/courses/' + id + '/versions/latest')
    statusCode = request.status_code
    if statusCode == 200:
        return request.json()
    raise Exception("reguest status code: ", statusCode)

def getNCourses(n: int, start: int):
    request = requests.get('https://ois2dev.ut.ee/api/courses?take=' + str(n) + '&start=' + str(start))
    statusCode = request.status_code
    if statusCode == 200:
        return request.json()
    raise Exception("reguest status code: ", statusCode)

