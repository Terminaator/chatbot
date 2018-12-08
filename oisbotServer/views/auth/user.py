import requests
import datetime

def getUserBasicDetails(token):
    request = requests.get('https://ois2dev.ut.ee/api/user/', headers={'X-Access-Token': token})
    statusCode = request.status_code
    if statusCode == 200:
        return request.json()
    raise Exception("reguest status code: ", statusCode)


def getNextCourseEvent(token):
    """
    Finds the next user's course
    :param token:
    :return: Next course and its event
    """
    request = requests.get('https://ois2dev.ut.ee/api/timetable/personal', headers={'X-Access-Token': token})
    statusCode = request.status_code
    if statusCode != 200:
        raise Exception("reguest status code: ", statusCode)
    json = request.json()
    course, event = None, -1
    for i in range(4):
        course, event = getCourseNextInWeek(json, i)
        if (course != None):
            break
    return (course, event)


def getCourseNextInWeek(json, deltaWeeks):
    now = datetime.datetime.now()
    comparableTime = datetime.timedelta(weeks=100)
    shortestIndex = -1
    nearestEvent = None
    for i in range(6):
        for event in json['course_events'][i]['events']:
            t = event['time']
            # sorting out all the past events
            eventEndDate = datetime.datetime.strptime(t["until_date"] + " " + t['begin_time'], "%Y-%m-%d %H:%M:%S")
            if now < eventEndDate:
                dayOfWeek = now.weekday() + 1
                eventTimeThisWeek = now + datetime.timedelta(days=int(t['weekday']['code']) - dayOfWeek, weeks=deltaWeeks)
                # if event should be over then end
                if eventEndDate <= eventTimeThisWeek or eventTimeThisWeek <= datetime.datetime.strptime(t["since_date"] + " " + t['begin_time'], "%Y-%m-%d %H:%M:%S"):
                    continue
                beginTime = datetime.datetime.strptime(t['begin_time'], "%H:%M:%S")
                eventTimeThisWeek = eventTimeThisWeek.replace(hour=beginTime.hour, minute=beginTime.minute, second=0)
                if now < eventTimeThisWeek and eventTimeThisWeek - now < comparableTime and eventTimeThisWeek.year == now.year:
                    print(event)
                    comparableTime = eventTimeThisWeek - now
                    shortestIndex = i
                    nearestEvent = event
    if (shortestIndex != -1):
        return (json['course_events'][shortestIndex], nearestEvent)
    return (None, None)



