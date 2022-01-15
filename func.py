import Ikp
import telebot
import callback
import BDworker

from telebot import types
from keyboa import Keyboa

def search_f(bot,message):
    film_obj_list = Ikp.search_film_by_name(message.text)
    if len(film_obj_list) > 0:
        films = makeFilmList(film_obj_list, message.text)
        text = makeFilmText(film_obj_list, message.text)
        
        kb_films = Keyboa(items=films, items_in_row=3, copy_text_to_callback=True,front_marker="&f_id=")

        bot.send_message(message.chat.id, text, reply_markup=kb_films())

    else:
         bot.send_message(message.chat.id, "Не удалось найти фильм.....\n\r Добавляю \"Как есть\"")
         BDworker.addMovieByTitle(message.chat.id, message.text)


def writeFilmList(bot,message,page=1):
    films = BDworker.getUserFilms(message.chat.id)
    if len(films) > 0:
        text = makeFilmListText(films)
        films_items = makeFilmListKeyboa(films)

        kb_user_film_list = Keyboa(items=films_items, items_in_row=6, copy_text_to_callback=True,front_marker="&p_id=")

        bot.send_message(message.chat.id, text, reply_markup=kb_user_film_list())
    else:
        bot.send_message(message.chat.id, "В вашем списке нет фильмов!\n\rНапишите мне название фильма, и я добавлю его в список!")


def howAreU(bot,message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
    item2 = types.InlineKeyboardButton("Не очень", callback_data='bad')

    markup.add(item1, item2)

    bot.send_message(message.chat.id, 'Отлично, сам как?', reply_markup=markup)

#Formating text (SearchFilm)

def takeName(film_name, user_film_name):
    if film_name is None:
        return user_film_name
    else:
        return film_name

def makeTextFound(film, user_film_name):
    if film.ru_name is None and film.name is None:
        return user_film_name + " ( \"Оригинальное название не найдено\" )"
    elif film.ru_name is None:
        return user_film_name + " (" + film.name + ")"
    elif film.name is None:
        return film.ru_name + " ( \"Оригинальное название не найдено\" )"
    else:
        return film.ru_name + " (" + film.name + ")"

def makeFilmList(film_obj_list, user_film_name):
    films_list = []
    for i,film in enumerate(film_obj_list,1):
        films_list.append({str(i)+". " + takeName(film.ru_name,user_film_name): str(film.kp_id)})
        if i == 3 : break
    films_list.append({"Добавить как есть": "&f_name=" + user_film_name})
    return films_list

def makeFilmText(film_obj_list, user_film_name):
    films_text = 'Вот что мне удалось найти: \n\r'
    for i,film in enumerate(film_obj_list,1):
        films_text += str(i) + '. ' + str(makeTextFound(film,user_film_name)) + '\n\r'
        if i == 3 : break
    films_text += 'Выберите фильм, или нажмите "Добавить как есть"'
    return films_text

#Formating text (WriteFilmList)

def makeFilmListText(films): 
    films_list_text = "Ваш список:\n\r"
    for i,film in enumerate(films,1):
        films_list_text += str(i) + '. ' + str(film.name) + '\n\r'
        if(i % 12) == 0 : 
            print("Не больше 6 фильмов на страницу")
            break 
    return films_list_text
        
def makeFilmListKeyboa(films,page=1):
    film_list_kb=[]
    for i,film in enumerate(films,1):
        id = film.kinopoisk_id
        if film.kinopoisk_id is None:
            id = 0
        film_list_kb.append({str(i):id})
        if i == 12: break
    if page == 1:
        film_list_kb.append({"⏩":"next_page"})
    else:
        film_list_kb.append({"⏪":"&page"})
    return film_list_kb
    