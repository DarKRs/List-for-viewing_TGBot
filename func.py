import Ikp
import telebot
import callback
import BDworker
import random

from telebot import types
from keyboa import Keyboa

def search_f(bot,message):
    film_obj_list = Ikp.search_film_by_name(message.text)
    if len(film_obj_list) > 0:
        films = makeFilmList(film_obj_list, message.text)
        text = makeFilmText(film_obj_list, message.text)
        
        kb_films = Keyboa(items=films, items_in_row=3, copy_text_to_callback=True,front_marker="&ff_id=") #Found film

        bot.send_message(message.chat.id, text, reply_markup=kb_films())

    else:
         bot.send_message(message.chat.id, "Не удалось найти фильм.....\n\r Добавляю \"Как есть\"")
         BDworker.addMovieByTitle(message.chat.id, message.text)


def writeFilmList(bot,message):
    films = BDworker.getUserFilms(message.chat.id)
    if films != None:
        text = makeFilmListText(films,1)
        films_items = makeFilmListKeyboa(films,1)
        if len(films) % 12 == 0:
            end_idx = len(films) - 11
        else:
            end_idx = (len(films) - len(films) % 12)+1
        items_control =[{"⏮":"&page=1"}, {"⏪":"&page=-1"}, {"⏹":"&page=1"}, {"⏩":"&page=13"}, {"⏭":"&page=" + str(end_idx)}]

        kb_film = Keyboa(items=films_items, items_in_row=6, copy_text_to_callback=True,front_marker="&sf_id=").keyboard #Selected film
        kb_control = Keyboa(items=items_control, items_in_row=5, copy_text_to_callback=True,front_marker="&sf_id=").keyboard

        keyboard = Keyboa.combine(keyboards=(kb_film, kb_control))

        bot.send_message(message.chat.id, text, reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "В вашем списке нет фильмов!\n\rНапишите мне название фильма, и я добавлю его в список!")

def writeFilmListPage(bot,call,idx):
    message = call.message
    films = BDworker.getUserFilms(message.chat.id)
    if films != None:
        if idx < 1 or idx > len(films):
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=getRndEndMessage())
            return
        text = makeFilmListText(films,idx)
        films_items = makeFilmListKeyboa(films,idx)
        if len(films) % 12 == 0:
            end_idx = len(films) - 11
        else:
            end_idx = (len(films) - len(films) % 12)+1
        items_control =[{"⏮":"&page=1"},{"⏪":"&page=" + str(idx-12)}, {"⏹":"&page=" + str(idx)}, {"⏩":"&page=" + str(idx+12)}, {"⏭":"&page=" + str(end_idx)}]
        
        kb_film = Keyboa(items=films_items, items_in_row=6, copy_text_to_callback=True,front_marker="&sf_id=").keyboard #Selected film
        kb_control = Keyboa(items=items_control, items_in_row=5, copy_text_to_callback=True,front_marker="&sf_id=").keyboard

        keyboard = Keyboa.combine(keyboards=(kb_film, kb_control))

        if text == message.text + "\n":
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=getRndPushMessage())
            return
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text,reply_markup=keyboard)

    else:
        bot.send_message(message.chat.id, "В вашем списке нет фильмов!\n\rНапишите мне название фильма, и я добавлю его в список!")

def writeFilmInfo(bot,message,idx):
    film = BDworker.getUserFilms(message.chat.id)[int(idx)]
    text = makeMovieText(film)
    edit_film_items = [
        {"Изм. название":"name=" + str(idx)},{"Изм. ссылку":"url="+ str(idx)},{"Изм. год":"year="+str(idx)},
        {"Изм. жанры":"genre="+str(idx)},{"Изм. категорию":"category="+str(idx)},{"Изм. описание":"desc="+str(idx)},
        ]
    edit_film_items_watch = []
    if film.watched == 0:
        edit_film_items_watch.append({"Просмотрено":"watched="+str(idx)})
    else:
        edit_film_items_watch.append({"Не просмотренно":"nonwatched="+str(idx)})
    edit_film_items_watch.append({"Удалить фильм":"delete="+str(idx)})

    kb_edit = Keyboa(items=edit_film_items, items_in_row=3, copy_text_to_callback=True,front_marker="&ef_id=").keyboard #Edit film
    kb_watch = Keyboa(items=edit_film_items_watch, items_in_row=2, copy_text_to_callback=True,front_marker="&ef_id=").keyboard

    keyboard = Keyboa.combine(keyboards=(kb_edit, kb_watch))

    bot.send_message(message.chat.id, text, reply_markup=keyboard, parse_mode= "Markdown")

def editFilmInfo(bot,message,idx):
    film = BDworker.getUserFilms(message.chat.id)[int(idx)]
    text = makeMovieText(film)
    edit_film_items = [
        {"Изм. название":"name=" + str(idx)},{"Изм. ссылку":"url="+ str(idx)},{"Изм. год":"year="+str(idx)},
        {"Изм. жанры":"genre="+str(idx)},{"Изм. категорию":"category="+str(idx)},{"Изм. описание":"desc="+str(idx)},
        ]
    edit_film_items_watch = []
    if film.watched == 0:
        edit_film_items_watch.append({"Просмотрено":"watched="+str(idx)})
    else:
        edit_film_items_watch.append({"Не просмотренно":"nonwatched="+str(idx)})
    edit_film_items_watch.append({"Удалить фильм":"delete="+str(idx)})

    kb_edit = Keyboa(items=edit_film_items, items_in_row=3, copy_text_to_callback=True,front_marker="&ef_id=").keyboard #Edit film
    kb_watch = Keyboa(items=edit_film_items_watch, items_in_row=2, copy_text_to_callback=True,front_marker="&ef_id=").keyboard

    keyboard = Keyboa.combine(keyboards=(kb_edit, kb_watch))

    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text,reply_markup=keyboard, parse_mode= "Markdown")



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
    films_list.append({"Добавить как есть": "&f_name=" + user_film_name[:20]})
    return films_list

def makeFilmText(film_obj_list, user_film_name):
    films_text = 'Вот что мне удалось найти по запросу "' + user_film_name + '": \n\r'
    for i,film in enumerate(film_obj_list,1):
        films_text += str(i) + '. ' + str(makeTextFound(film,user_film_name)) + ' ' + film.year + ' ' + film.category + '\n\r'
        if i == 3 : break
    films_text += "Выберите фильм, или нажмите 'Добавить как есть'"
    return films_text

#Formating text (WriteFilmList)

def makeFilmListText(films,idx): 
    films_list_text = "Ваш список"
    if idx + 11 >= len(films):
        films_list_text += " (" + str(len(films)) + "/" + str(len(films)) + ") " + ":\n"
    else:
        films_list_text += " (" + str(idx+11) + "/" + str(len(films)) + ") " + ":\n"
    for i,film in enumerate(films,idx):
        if(films[i-1].watched == 1):
            films_list_text += str(i) + '. ' + str(films[i-1].name) + '  👁‍🗨\n'
        else:
            films_list_text += str(i) + '. ' + str(films[i-1].name) + '\n'
        if(i % 12) == 0 or i > len(films)-1 : break 
    return films_list_text
        
def makeFilmListKeyboa(films,idx):
    film_list_kb=[]
    for i,film in enumerate(films,idx):
        film_list_kb.append({str(i):i-1})
        if(i % 12) == 0 or i > len(films)-1: break
    return film_list_kb
    
def getRndEndMessage():
    messages = ["Ты не пройдешь", "Дальше ничего нет","Это край мира, дальше живут драконы","Матерь милосердная, это конец?", 
                "Дальше идут пустыни Дейи, там только смерть", "Все что имеет начало, имеет и конец","Не думайте, что это конец. Конца нет и быть не может.",
                "Твой путь… оканчивается здесь, лорд ситхов.", "Это — конец вашего пути.", "Конец песни — приглашение к началу.", "А дальше уже некуда идти",
                "— Стоп, — сказала она себе. — Это ещё не конец. Ты увидишь их снова.", "Ты не в ту сторону листаешь, друг", "Дальше вы не пройдете, пока не получите бумаги",
               "Ну ты и соня, даже вчерашний шторм тебя не разбудил"]
    return random.choice(messages)

def getRndPushMessage():
    messages = ["Жмак", "Тык", "Пум", "Паф", "Ты все ещё жмакаешь не на те кнопки?", "Чего ты хочешь добиться?", "Бам", "Позравляю! Вы сломали бота", "Гыгыгыгыгы",
                "Пуньк","Скидыщ!", "Error: 404 not found ;)", "Пиу", "Пау", "Кчау", "Ахахахах, зачем?", "Ты думал что-то здесь будет? Оййеее.....", "Хватит меня тыкать",
                "Неправильно! Попробуй ещё раз", "Попробуй тыкнуть в другую кнопку", "Тыкни в кого-нибудь другого"]
    return random.choice(messages)

#Formating Text (Selected Film)

def makeMovieText(film):
    text = film.name
    if film.kinopoisk_url is None:
        text += " ( Ссылка не указана ) "
    else:
        text += " ( " + film.kinopoisk_url + " ) "
    if film.watched == 1:
        text += "\n\r*Просмотрено*"
    else:
        text += "\n"
    if film.year is None:
        text += "\n\n\r Год не указан"
    else:
        text += "\n\n\r Год:" + film.year
    if film.genre is None:
        text += "\n\n\r Жанры не указаны"
    else:
        text += "\n\n\r Жанры:" + str(film.genre)
    if film.desc is None:
        text += "\n\n\r Описание не указано"
    else:
        text += "\n\n\r" + film.desc
    return text
