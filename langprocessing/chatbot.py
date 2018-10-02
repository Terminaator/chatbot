class chatbot():
    def __init__(self):
        self.frames = {}
        self.currentFrame = -1

    def getResponse(self, inputSentence):
        # words = sentProc.getWords(inputSentence)
        words = {"questionWord": "mitu", "ects": True, "0": "on", "1": "kursus", "courseID": "LTAT.05.005"}
        self.addFrameLayer(words)

    def addFrameLayer(self, words):
        """
        creates a new frame layer
        :param words:  dictionary of words to be added to the new frame layer
        """
        self.currentFrame += 1
        self.frames["layer " + str(self.currentFrame)] = self.fillFrameLayer(words)

    def fillFrameLayer(self, words):
        """
        fills a frame layer
        :param words: dictionary of words to be added to the layer
        :return: filled frame layer
        """
        layer = self.createEmptyLayer()
        for key in layer:
            for k in layer[key]:
                if (k in words):
                    layer[key][k] = words[k]
        return layer

    def createEmptyLayer(self):
        """
        Creates a layer for frame
        Frame with 1 layer structure
        frame = {
            layer 0: {
                misc : {questionWord: String}
                courses : {courseID: String , ects : boolean}
            }
        }
        """
        misc = {"questionWord": ""}
        courses = {"courseID": "", "ects": ""}
        layer = {"misc": misc, "courses": courses}
        return layer
