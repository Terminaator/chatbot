class Data:
    def __init__(self, askedQuestion, frames, currentFrame, hangmanData, authData):
        # chatbot
        self.askedQuestion = askedQuestion
        self.frames = frames
        self.currentFrame = currentFrame
        self.authData = authData
        # hangman
        self.hangmanData = hangmanData

    def __str__(self):
        return str(self.askedQuestion) + " " + str(self.frames) + " " + str(self.currentFrame) + " " + str(
            self.hangmanData)
