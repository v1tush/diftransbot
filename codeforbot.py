import telebot
from telebot import types
f =  open('a', 'r')
token = f.read()
f.close()
text_on_lang_input = ''
text_out = ''
bot = telebot.TeleBot(token)
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, я бот-переводчик. Могу прислать тебе разные варианты перевода одного предложения или слова. При написании команд, пиши пожалуйста их с большой буквы")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, 'Напиши "Начнем"')
    elif message.text == "Начнем":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Английский🇬🇧")
        btn2 = types.KeyboardButton("Русский🇷🇺")
        markup.add(btn1, btn2)
        bot.send_message(message.from_user.id, "Выбери пожалуйста язык, с которого я буду переводить.", reply_markup=markup)
    elif message.text == "Английский🇬🇧":
        #код сохранения данных, или их обработки
        bot.send_message(message.from_user.id, 'Сейчас ты можешь прислать сообщение, а потом я скину тебе варианты его перевода.')
        bot.send_message(message.from_user.id, 'Если ты ошибся с выбором языка, то напиши слово "Назад"')
    elif message.text == "Русский🇷🇺":
        #код сохранения данных, или их обработки
        bot.send_message(message.from_user.id, 'Сейчас ты можешь прислать сообщение, а потом я скину тебе варианты его перевода.')
        bot.send_message(message.from_user.id, 'Если ты ошибся с выбором языка, то напиши слово "Назад"')
    elif message.text == "Назад": 
        pass
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
bot.polling(none_stop=True, interval=0)
