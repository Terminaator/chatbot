import requests

def getStructuralUnit(code):
    request = requests.get('https://ois2dev.ut.ee/api/structural-units/' + code.upper())
    statusCode = request.status_code
    if statusCode == 200:
        return request.json()
    raise Exception("reguest status code: ", statusCode)

def getAllStructuralUnits():
    request = requests.get('https://ois2dev.ut.ee/api/structural-units/all')
    statusCode = request.status_code
    if statusCode == 200:
        return request.json()
    raise Exception("reguest status code: ", statusCode)