import telebot
import config
import random
import Ikp
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
           case '📄 Мой список': func.writeFilmList(bot,message)
           case _ : func.search_f(bot,message)
            

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if '&ff_id=' in call.data:      #Found film
                if '&f_name=' in call.data:
                    BDworker.addMovieByTitle(call.message.chat.id, call.data.split("=")[2])
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Фильм - ' + call.data.split("=")[2] + '.\n\rДобавлен в список без дополнительной информации')
                else:
                    BDworker.addMovie(call.data.split("=")[1], call.message.chat.id)
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Фильм - ' + str(Ikp.get_film_by_id(call.data.split("=")[1]).name) + ' Добавлен в ваш список :)')
            elif '&sf_id' in call.data: #Selected film
                if '&page=' in call.data:
                    func.writeFilmListPage(bot,call,int(call.data.split("=")[2]))
                else:
                    pass
            else:
                match call.data:
                    case 'good' | 'bad': callback.howAreU_back(bot,call)
                    case _ : bot.send_message(call.message.chat.id, 'Я не знаю что ответить')
    except Exception as e:
        print(repr(e))





# RUN
while(True):
    try:
        bot.polling(none_stop=True, interval=0)
    except:
        pass
