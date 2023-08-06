from deep_translator import GoogleTranslator
import telebot
from telebot import types
import detectlanguage
detectlanguage.configuration.api_key = "19be5e73276c5371d559241062b80aab"
f =  open('a', 'r')
token = f.read()
f.close()
text_on_lang_input = ''
text_out = ''
run = False
bot = telebot.TeleBot(token)
unlist = []
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global run
    global unlist
    translated1 = "Hello"
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Привет, я бот-переводчик. Могу прислать тебе разные варианты перевода одного предложения или слова. При написании команд, пиши пожалуйста их с большой буквы")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, 'Напиши "Начнем"')
    elif message.text == "Начнем":
        bot.send_message(message.from_user.id, 'Сейчас ты можешь прислать сообщение, а потом я скину тебе варианты его перевода.')
        run = True
    else:
        if run:
            language = detectlanguage.simple_detect(message.text)
            bot.send_message(message.from_user.id, language)
            if language == 'en':
                translated1 = GoogleTranslator(source='en', target='ru').translate(message.text)
            elif language == 'ru':
                translated1 = GoogleTranslator(source='ru', target='en').translate(message.text)
            bot.send_message(message.from_user.id, translated1)
bot.polling(none_stop=True, interval=0)
