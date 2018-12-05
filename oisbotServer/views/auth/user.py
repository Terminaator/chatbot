import requests


def getUserBasicDetails(token):
    request = requests.get('https://ois2dev.ut.ee/api/user/', headers={'X-Access-Token': token})
    statusCode = request.status_code
    if statusCode == 200:
        return request.json()
    raise Exception("reguest status code: ", statusCode)
