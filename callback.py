import kinopoisk
import telebot
import kinopoisk

from telebot import types

def howAreU_back(bot,call):
    if call.data == 'good':
               bot.send_message(call.message.chat.id, 'Вот и отличненько 😊')
    elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Бывает 😢')

    # remove inline buttons
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="😊 Как дела?",
                                  reply_markup=None)

    # show alert
    bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!11")

def newFilm_back(bot,id):
    if id == "0":
        pass
    else:

      