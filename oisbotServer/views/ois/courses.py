import requests

def coursesId(id):
    request = requests.get('https://ois2dev.ut.ee/api/courses/' + id + '/versions/latest')
    status_code = request.status_code
    if status_code == 200:
        return request.json()
    raise Exception("reguest status code: ", status_code)

def getNCourses(n: int, start: int):
    request = requests.get('https://ois2dev.ut.ee/api/courses?take=' + str(n) + '&start=' + str(start))
    status_code = request.status_code
    if status_code == 200:
        return request.json()
    raise Exception("reguest status code: ", status_code)




