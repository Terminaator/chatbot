class Data:
    def __init__(self,askedQuestion,frames,currentFrame):
        self.askedQuestion = askedQuestion
        self.frames = frames
        self.currentFrame = currentFrame

    def __str__(self):
        return str(self.askedQuestion) + " " + str(self.frames) + " " + str(self.currentFrame)