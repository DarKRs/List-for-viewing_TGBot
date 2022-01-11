import kinopoisk
import telebot
import callback

from telebot import types
from keyboa import Keyboa

def search_f(bot,message):
    film_list = kinopoisk.search_film_api(message.text)
    if len(film_list) > 0:
    
        films = [
            {str(film_list[0].name_ru): str(film_list[0].kinopoisk_id)}, 
            {str(film_list[1].name_ru): str(film_list[1].kinopoisk_id)}, 
            {str(film_list[2].name_ru): str(film_list[2].kinopoisk_id)},
            {"Добавить как есть": "0"}
            ]


        text = 'Вот что мне удалось найти: \n\r' + '1.' + str(film_list[0].name_ru) + ' (' + str(film_list[0].name_original) + ') \n\r' + '2.' + str(film_list[1].name_ru) + ' (' + str(film_list[1].name_original) + ') \n\r' + '3.' + str(film_list[2].name_ru) + ' (' + str(film_list[2].name_original) + ') \n\r' + 'Выберите фильм, или нажмите "Добавить как есть"'

        kb_films = Keyboa(items=films, copy_text_to_callback=True,front_marker="&film_id=")

        bot.send_message(message.chat.id, text, reply_markup=kb_films())

    else:
         bot.send_message(message.chat.id, "Не удалось найти фильм.....\n\r Добавляю \"Как есть\"")
        # callback.


#def randNumber(message):

def howAreU(bot,message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
    item2 = types.InlineKeyboardButton("Не очень", callback_data='bad')

    markup.add(item1, item2)

    bot.send_message(message.chat.id, 'Отлично, сам как?', reply_markup=markup)
