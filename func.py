import kinopoisk
import telebot
import callback
import BDworker

from telebot import types
from keyboa import Keyboa

def search_f(bot,message):
    film_obj_list = kinopoisk.search_film_api(message.text)
    if len(film_obj_list) > 0:
        films = makeFilmList(film_obj_list, message.text)
        text = makeFilmText(film_obj_list, message.text)
        
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

def makeTextFound(film, user_film_name):
    if film.name_ru is None and film.name_original:
        return user_film_name + " ( \"Оригинальное название не найдено\" )"
    elif film.name_ru is None:
        return user_film_name + " (" + film.name_original + ")"
    elif film.name_original is None:
        return film.name_ru + " ( \"Оригинальное название не найдено\" )"
    else:
        return film.name_ru + " (" + film.name_original + ")"

def makeFilmList(film_obj_list, user_film_name):
    films_list = []
    i=1
    for film in film_obj_list:
        films_list.append({str(i)+". " + takeName(film.name_ru,user_film_name): str(film.kinopoisk_id)})
        i+=1
        if i > 3 : break
    films_list.append({"Добавить как есть": "&film_name=" + user_film_name})
    return films_list

def makeFilmText(film_obj_list, user_film_name):
    films_text = 'Вот что мне удалось найти: \n\r'
    i=1
    for film in film_obj_list:
        films_text += str(i) + '. ' + str(makeTextFound(film,user_film_name)) + '\n\r'
        i+=1
        if i > 3 : break
    films_text += 'Выберите фильм, или нажмите "Добавить как есть"'
    return films_text