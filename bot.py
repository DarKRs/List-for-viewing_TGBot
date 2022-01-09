import telebot
import config
import random
import kinopoisk
import func
import sys;

from telebot import types



bot = telebot.TeleBot(config.TOKEN)
#switch_case_text = {
#    '🎲 Рандомное число': bot.send_message(message.chat.id, str(random.randint(0, 100)))
#}
#switch_case_commands = {
#
#}
print(sys.version)


@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('static/bersHi.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🎲 Рандомное число")
    item2 = types.KeyboardButton("😊 Как дела?")

    markup.add(item1, item2)

    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\nЯ - , бот созданный чтобы запоминать фильмы, мультфильмы, сериалы и т.д. необходымые к просмотру. \n Что то вроде блокнотика с фильмами ;).".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):

    if message.chat.type == 'private':
       match message.text:
           case "test": bot.send_message(message.chat.id, "text")
           case '🎲 Рандомное число': bot.send_message(message.chat.id, str(random.randint(0, 100)))
           case '😊 Как дела?': func.howAreU(bot,message)
           case _ : bot.send_message(message.chat.id, 'Я не знаю что ответить 😢')
            


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Вот и отличненько 😊')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Бывает 😢')

            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="😊 Как дела?",
                                  reply_markup=None)

            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!11")

    except Exception as e:
        print(repr(e))


# RUN
bot.polling(none_stop=True, interval=0)