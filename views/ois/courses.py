import requests

def coursesId(id):
    request = requests.get('https://ois2.ut.ee/api/courses/' + id)
    status_code = request.status_code
    if status_code == 200:
        return request.json()
    raise Exception("reguest status code: " + status_code)