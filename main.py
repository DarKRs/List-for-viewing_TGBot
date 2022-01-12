import telebot
import config
import random
import kinopoisk
import func
import sys
import callback
import BDworker

from BDworker import users_dict
from telebot import types
from keyboa import Keyboa

bot = telebot.TeleBot(config.TOKEN)

def Init():
    BDworker.Init()
    print(sys.version)


Init()


@bot.message_handler(commands=['start'])
def welcome(message):
    BDworker.addUser(message)
    sti = open('static/bersHi.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🎲 Рандомное число")
    item2 = types.KeyboardButton("😊 Как дела?")
    item3 = types.KeyboardButton("📄 Мой список")

    markup.add(item1, item2, item3)

    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\nЯ - , бот созданный чтобы запоминать фильмы, мультфильмы, сериалы и т.д. необходымые к просмотру. \nЧто то вроде блокнотика с фильмами ;).".format(
                         message.from_user),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
       match message.text:
           #case "test": bot.send_message(message.chat.id, "text")
           case '🎲 Рандомное число': bot.send_message(message.chat.id, str(random.randint(0, 100)))
           case '😊 Как дела?': func.howAreU(bot,message)
           case 'test': 
            menu = ["spam", "eggs", "ham"]
            keyboard = Keyboa(items=menu)
            bot.send_message(chat_id=message.chat.id, text="Test Keyboa", reply_markup=keyboard())
           case _ : bot.register_next_step_handler(message, func.search_f(bot,message)); #следующий шаг func.search_f
            

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if '&film_id=' in call.data:
                if '&film_name=' in call.data:
                    BDworker.addMovieByTitle(call.message.chat.id, call.data.split("=")[2])
                    bot.send_message(call.message.chat.id, 'Фильм - ' + call.data.split("=")[2] + '.\n\rДобавлен в список без дополнительной информации')
                else:
                    call.data.split("=")[1]
            else:
                match call.data:
                    case 'good' | 'bad': callback.howAreU_back(bot,call)
                    case _ : bot.send_message(call.message.chat.id, 'Я не знаю что ответить')
    except Exception as e:
        print(repr(e))





# RUN
bot.polling(none_stop=True, interval=0)