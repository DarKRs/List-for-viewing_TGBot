import kinopoisk
import telebot
import callback
import BDworker

from telebot import types
from keyboa import Keyboa

def search_f(bot,message):
    film_list = kinopoisk.search_film_api(message.text)
    if len(film_list) > 0:
        
        films = [
            {"1. " + takeName(film_list[0].name_ru,message.text): str(film_list[0].kinopoisk_id)}, 
            {"2. " + takeName(film_list[1].name_ru,message.text): str(film_list[1].kinopoisk_id)}, 
            {"3. " + takeName(film_list[2].name_ru,message.text): str(film_list[2].kinopoisk_id)},
            {"Добавить как есть": "$film_name=" + message.text}
            ]


        text = 'Вот что мне удалось найти: \n\r' + '1. ' + str(makeTextFound(film_list[0],message.text)) + '\n\r' + '2. ' + str(makeTextFound(film_list[1],message.text)) + '\n\r' + '3. ' + str(makeTextFound(film_list[2],message.text)) + '\n\r' + 'Выберите фильм, или нажмите "Добавить как есть"'
        kb_films = Keyboa(items=films, items_in_row=3, copy_text_to_callback=True,front_marker="&film_id=")

        bot.send_message(message.chat.id, text, reply_markup=kb_films())

    else:
         bot.send_message(message.chat.id, "Не удалось найти фильм.....\n\r Добавляю \"Как есть\"")
         BDworker.addMovieByTitle(message.text)


#def randNumber(message):

def howAreU(bot,message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
    item2 = types.InlineKeyboardButton("Не очень", callback_data='bad')

    markup.add(item1, item2)

    bot.send_message(message.chat.id, 'Отлично, сам как?', reply_markup=markup)

def takeName(film_name, user_film_name):
    if film_name is None:
        return user_film_name
    else:
        return film_name

def makeTextFound(film, film_name_user):
    if film.name_ru is None and film.name_original:
        return film_name_user + " ( \"Оригинальное название не найдено\" )"
    elif film.name_ru is None:
        return film_name_user + " (" + film.name_original + ")"
    elif film.name_original is None:
        return film.name_ru + " ( \"Оригинальное название не найдено\" )"
    else:
        return film.name_ru + " (" + film.name_original + ")"