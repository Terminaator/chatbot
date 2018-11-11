import requests

def getStructuralUnit(code):
    request = requests.get('https://ois2dev.ut.ee/api/structural-units/' + code.upper())
    status_code = request.status_code
    if status_code == 200:
        return request.json()
    raise Exception("reguest status code: ", status_code)

def getAllStructuralUnits():
    request = requests.get('https://ois2dev.ut.ee/api/structural-units/all')
    status_code = request.status_code
    if status_code == 200:
        return request.json()
    raise Exception("reguest status code: ", status_code)