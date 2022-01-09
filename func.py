import kinopoisk
import telebot

from telebot import types

def search_f(bot,message,film):
    bot.send_message(message.chat.id, 'Это новый фильм для списка - '+ message.text + ' ?')

    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("Да", callback_data='film_Yes')
    item2 = types.InlineKeyboardButton("Нет", callback_data='film_No')


#def randNumber(message):

def howAreU(bot,message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
    item2 = types.InlineKeyboardButton("Не очень", callback_data='bad')

    markup.add(item1, item2)

    bot.send_message(message.chat.id, 'Отлично, сам как?', reply_markup=markup)
    