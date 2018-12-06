from langprocessing import Chatbot

print('Hello i am õisBot! Ask me anything. To exit type "!exit".')
bot = Chatbot.chatbot()
while 1:
    text = input('>> ')
    if text == '!exit':
        break
    print(bot.getResponse(text))