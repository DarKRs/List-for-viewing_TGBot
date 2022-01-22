import telebot
import BDworker
import func

from telebot import types

#Category film

def writeCategoryKeyboa(bot,message):
    msg = bot.send_message(message.chat.id,'Выберите категорию из списка', reply_markup=func.getCategoryKeyboa(message.chat.id))
    bot.register_next_step_handler(msg,func.writeFilmListCategory,bot)
   

# Edit film

def editFilmName(bot,message,id):
    msg = bot.send_message(message.chat.id,'Пожалуйста, введите новое название',reply_markup=cancelKeyboa())
    bot.register_next_step_handler(msg,BDworker.editName,id,bot)

def editFilmUrl(bot,message,id):
    msg = bot.send_message(message.chat.id,'Пожалуйста, введите новую ссылку',reply_markup=cancelKeyboa())
    bot.register_next_step_handler(msg,BDworker.editUrl,id,bot)

def editFilmYear(bot,message,id):
    msg = bot.send_message(message.chat.id,'Пожалуйста, введите год',reply_markup=cancelKeyboa())
    bot.register_next_step_handler(msg,BDworker.editYear,id,bot)

def editFilmGenre(bot,message,id):
    msg = bot.send_message(message.chat.id,'Пожалуйста, введите жанры через запятую',reply_markup=cancelKeyboa())
    bot.register_next_step_handler(msg,BDworker.editGenre,id,bot)

def editFilmCategory(bot,message,id):
    msg = bot.send_message(message.chat.id,'Пожалуйста, введите категорию \nСтандартные категории: Фильм, Мультфильм, Аниме фильм, Сериал, Мультсериал, Аниме сериал \nВнимание! Название категории не более 20 символов',reply_markup=cancelKeyboa())
    bot.register_next_step_handler(msg,BDworker.editCategory,id,bot)

def editFilmDesc(bot,message,id):
    msg = bot.send_message(message.chat.id,'Пожалуйста, введите новое описание',reply_markup=cancelKeyboa())
    bot.register_next_step_handler(msg,BDworker.editDesc,id,bot)

def editFilmWatch(bot,message,id,watched):
    BDworker.editWatch(message,id,bot,watched)

def deleteFilm(bot,message,id):
    msg = bot.send_message(message.chat.id,'Вы уверенны что хотите удалить фильм из списка?',reply_markup=delKeyboa())
    bot.register_next_step_handler(msg,BDworker.deleteFilm,id,bot)

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