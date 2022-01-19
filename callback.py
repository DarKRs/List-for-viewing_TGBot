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
    msg = bot.send_message(message.chat.id,'Пожалуйста, введите новое название',reply_markup=cancelKeyboa())
    bot.register_next_step_handler(msg,BDworker.editName,idx,bot)

def editFilmUrl(bot,message,idx):
    msg = bot.send_message(message.chat.id,'Пожалуйста, введите новую ссылку',reply_markup=cancelKeyboa())
    bot.register_next_step_handler(msg,BDworker.editUrl,idx,bot)

def editFilmYear(bot,message,idx):
    msg = bot.send_message(message.chat.id,'Пожалуйста, введите год',reply_markup=cancelKeyboa())
    bot.register_next_step_handler(msg,BDworker.editYear,idx,bot)

def editFilmGenre(bot,message,idx):
    msg = bot.send_message(message.chat.id,'Пожалуйста, введите жанры через запятую',reply_markup=cancelKeyboa())
    bot.register_next_step_handler(msg,BDworker.editGenre,idx,bot)

def editFilmCategory(bot,message,idx):
    msg = bot.send_message(message.chat.id,'Пожалуйста, введите категорию \n Стандартные категории: Фильм, Мультфильм, Аниме фильм, Сериал, Мультсериал, Аниме сериал',reply_markup=cancelKeyboa())
    bot.register_next_step_handler(msg,BDworker.editCategory,idx,bot)

def editFilmDesc(bot,message,idx):
    msg = bot.send_message(message.chat.id,'Пожалуйста, введите новое описание',reply_markup=cancelKeyboa())
    bot.register_next_step_handler(msg,BDworker.editDesc,idx,bot)

def editFilmWatch(bot,message,idx,watched):
    BDworker.editWatch(message,idx,bot,watched)

def deleteFilm(bot,message,idx):
    msg = bot.send_message(message.chat.id,'Вы уверенны что хотите удалить фильм из списка?',reply_markup=delKeyboa())
    bot.register_next_step_handler(msg,BDworker.deleteFilm,idx,bot)

def cancelKeyboa():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    cancel = types.KeyboardButton("❌ Отмена")
    keyboard.add(cancel)
    return keyboard

def delKeyboa():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    yeap = types.KeyboardButton("✔️ Да")
    cancel = types.KeyboardButton("❌ Нет")
    keyboard.add(yeap,cancel)
    return keyboard