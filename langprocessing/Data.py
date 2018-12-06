class Data:
    def __init__(self,askedQuestion,frames,currentFrame):
        #chatbot
        self.askedQuestion = askedQuestion
        self.frames = frames
        self.currentFrame = currentFrame
        #hangman

    def __str__(self):
        return str(self.askedQuestion) + " " + str(self.frames) + " " + str(self.currentFrame)