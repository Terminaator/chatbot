from langprocessing.WordTags import WordTag as wt
from oisbotServer.views.auth import authentication as auth
from oisbotServer.views.auth import user
from langprocessing.questions.Courses import synthesizeWord

class AuthReqQuestions:
    def __init__(self):
        self.questions = [
            StudyBookN(),
            NextCourse()
        ]

    def canAnswer(self, layer):
        return True

    def answer(self, layer, token):
        for q in self.questions:
            if q.canAnswer(layer):
                return q.answer(layer, token)


class StudyBookN:
    def canAnswer(self, layer):
        return layer[wt.pronoun] == "mina" and wt.studybookNr in layer[wt.keywords]

    def answer(self, layer, token):
        """
        asnwers users studybook number (matrikli number)
        :param layer: current layer
        :param token: xAuthToken
        :return: question to the question

        if (auth.isTokkenValid(token).status_code == 200):
            userInf = user.getUserDetails(token)
        else:
        """
        return "Ei tea veel kust seda leiab :("

class NextCourse:
    def canAnswer(self, layer):
        return layer[wt.pronoun] == "mina" and wt.course in layer[wt.keywords] and "järgmine" in layer[wt.timeWord]

    def answer(self, layer, token):
        """
        :param layer: current layer
        :param token: xAuthToken
        :return: next course name
        """
        if (auth.isTokkenValid(token).status_code != 200):
            return "Te peate sisse logima, et ma saaks teile vastata."
        course, event = user.getNextCourseEvent(token)
        if (course == None):
            return "Teil järgmine kuu pole ühtegi kursust."
        ans = "Teil järgmisena toimub "
        if "study_work_type" in event:
            ans += event['study_work_type']['et']
        else:
            ans += event['event_type']['et']
        ans += " aines " + course['info']['title']['et'] + "."
        ans += " See toimub " + synthesizeWord(event['time']['weekday']['et'], "ad") + " kell " + event['time']['begin_time'][:5]
        ans += " ja asub addressil " + event['location']['address'] + "."
        return ans



