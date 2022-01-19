import telebot
import BDworker
import func

from telebot import types

def howAreU_back(bot,call):
    if call.data == 'good':
               bot.send_message(call.message.chat.id, 'Вот и отличненько 😊')
    elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Бывает 😢')

    # remove inline buttons
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="😊 Как дела?",
                                  reply_markup=None)


def editFilmName(bot,message,idx):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("❌ Отмена")
    markup.add(item1)
    msg = bot.send_message(message.chat.id,'Пожалуйста, введите новое название',reply_markup=markup)
    bot.register_next_step_handler(msg,BDworker.editName,idx,bot)

def editFilmUrl(bot,message,idx):
    msg = bot.send_message(message.chat.id,'Пожалуйста, введите новую ссылку')
    bot.register_next_step_handler(msg,BDworker.editUrl,idx,bot)

def editFilmYear(bot,message,idx):
    msg = bot.send_message(message.chat.id,'Пожалуйста, введите год')
    bot.register_next_step_handler(msg,BDworker.editYear,idx,bot)

def editFilmGenre(bot,message,idx):
    msg = bot.send_message(message.chat.id,'Пожалуйста, введите жанры через запятую')
    bot.register_next_step_handler(msg,BDworker.editGenre,idx,bot)

def editFilmCategory(bot,message,idx):
    msg = bot.send_message(message.chat.id,'Пожалуйста, введите категорию \n Стандартные категории: Фильм, Мультфильм, Аниме фильм, Сериал, Мультсериал, Аниме сериал')
    bot.register_next_step_handler(msg,BDworker.editCategory,idx,bot)

def editFilmDesc(bot,message,idx):
    msg = bot.send_message(message.chat.id,'Пожалуйста, введите новое описание')
    bot.register_next_step_handler(msg,BDworker.editDesc,idx,bot)

def editFilmWatch(bot,message,idx,watched):
    BDworker.editWatch(message,idx,bot,watched)

def deleteFilm(bot,message,idx):
    msg = bot.send_message(message.chat.id,'Вы уверенны что хотите удалить фильм из списка?\nНапишите "Да" если уверены')
    bot.register_next_step_handler(msg,BDworker.deleteFilm,idx,bot)