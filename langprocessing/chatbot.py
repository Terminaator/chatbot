
class chatbot():
    def __init__(self):
        frames = {}
        currentFrame = 0

    def generateResponse(self, inputSentence):
        # words = sentProc.getWords(inputSentence)
        words = {"question": "mitu", "ects": "eap", "0": "on", "1": "kursus", "courseID": "LTAT.05.005"}
        self.fillFrame(words)

    def fillFrame(self, words):
        layer = self.createEmptyLayer()




    def createEmptyLayer(self):
        """
        Creates a layer for frame
        Frame structure example:
        frame = {
            layer n: {
                courses : {courseID: "" , ects : boolean}
            }
        }
        """
        courses = {"courseID": "", "ects": ""}
        layer = {"courses": courses}
        return layer


