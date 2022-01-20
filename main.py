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

    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\nЯ - , бот созданный чтобы запоминать фильмы, мультфильмы, сериалы и т.д. необходымые к просмотру. \nЧто то вроде блокнотика с фильмами ;).".format(
                         message.from_user),
                     parse_mode='html', reply_markup=func.getStandKeyboa())


@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
       match message.text:
           case '🔎 Мой список (фильтр)': callback.writeCategoryKeyboa(bot,message)
           case '📄 Мой список': func.writeFilmList(bot,message)
           case _ : func.search_f(bot,message)
            

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if '&ff_id=' in call.data:      #Found film
                if '&f_name=' in call.data:
                    film_name = findFilmInMessage(call.message, call.data.split("=")[2])
                    BDworker.addMovieByTitle(call.message.chat.id, film_name)
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Фильм - ' + film_name + '.\n\rДобавлен в список без дополнительной информации')
                else:
                    BDworker.addMovie(call.data.split("=")[1], call.message.chat.id)
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Фильм - ' + str(Ikp.get_film_by_id(call.data.split("=")[1]).name) + ' Добавлен в ваш список :)')
            elif '&sf_id' in call.data:     #Selected film
                if '&page=' in call.data:
                    func.writeFilmListPage(bot,call,int(call.data.split("=")[2]))
                else:
                    func.writeFilmInfo(bot,call.message,call.data.split("=")[1])
            elif '&ef_id=' in call.data:    #Edit film
                match call.data.split("=")[1]:
                    case 'name': callback.editFilmName(bot,call.message,call.data.split("=")[2])
                    case 'url': callback.editFilmUrl(bot,call.message,call.data.split("=")[2])
                    case 'year': callback.editFilmYear(bot,call.message,call.data.split("=")[2])
                    case 'genre': callback.editFilmGenre(bot,call.message,call.data.split("=")[2])
                    case 'category': callback.editFilmCategory(bot,call.message,call.data.split("=")[2])
                    case 'desc': callback.editFilmDesc(bot,call.message,call.data.split("=")[2])
                    case 'watched': callback.editFilmWatch(bot,call.message,call.data.split("=")[2],1)
                    case 'nonwatched': callback.editFilmWatch(bot,call.message,call.data.split("=")[2],0)
                    case 'delete': callback.deleteFilm(bot,call.message,call.data.split("=")[2])
            else:
                match call.data:
                    case _ : bot.send_message(call.message.chat.id, 'Я не знаю что ответить')
    except Exception as e:
        print(repr(e))


def findFilmInMessage(message, data):
    text = message.text[message.text.index(data):message.text.rindex('"')]
    return text


# RUN
while(True):
    try:
        bot.polling(none_stop=True, interval=0)
    except:
        pass
