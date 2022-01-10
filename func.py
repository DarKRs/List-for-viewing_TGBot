import kinopoisk
import telebot
import main
from telebot import types

async def search_f(bot,message):
    film_list = kinopoisk.search_film_api(message.text)
    await bot.send_message(message.chat.id, 'Вот что мне удалось найти: \n\r' + 
                     '1.' + film_list[0].name_ru + ' (' + film_list[0].name_original + ') \n\r' + 
                     '2.' + film_list[1].name_ru + ' (' + film_list[1].name_original + ') \n\r' + 
                     '3.' + film_list[2].name_ru + ' (' + film_list[2].name_original + ') \n\r' + 
                     'Выберите фильм, или нажмите "Добавить как есть"')
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.add(types.InlineKeyboardButton(text=film_list[0].name_ru, callback_data="test"))
    results = []
    single_msg = types.InlineQueryResultArticle(
        id="1", title="Press me",
        input_message_content=types.InputTextMessageContent(message_text="Я – сообщение из инлайн-режима"),
        reply_markup=kb
    )
    item1 = types.InlineKeyboardButton("Да", callback_data='film_Yes')
    item2 = types.InlineKeyboardButton("Нет", callback_data='film_No')


#def randNumber(message):

def howAreU(bot,message):
    print(main.sda)
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
    item2 = types.InlineKeyboardButton("Не очень", callback_data='bad')

    markup.add(item1, item2)

    bot.send_message(message.chat.id, 'Отлично, сам как?', reply_markup=markup)
    