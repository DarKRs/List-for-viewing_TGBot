import sqlite3
import film
import Ikp
import func
import callback
from User import User

users_dict_query = {}
users_dict = {}
movies_dict_query = {}
movies_dict = {}

connect = sqlite3.connect('Main.db',check_same_thread=False)
cursor = connect.cursor()

def Init():
    #Users
    cursor.execute("""CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY,
        UserName TEXT,
        Timer INTEGER
    )""")
    connect.commit()

    #Movie
    cursor.execute("""CREATE TABLE IF NOT EXISTS Movies(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        Name TEXT,
        Year INTEGER,
        Kinopoisk_id INTEGER,
        Kinopoisk_url TEXT,
        Genre TEXT,
        Category TEXT,
        Watched INTEGER,
        Description TEXT,
        USER_ID INTEGER
    )""")
    connect.commit()
    #Dictionarys
    #connect.row_factory = dict_factory
    cursor.execute("SELECT * FROM Users")
    users_dict_query = cursor.fetchall()
    for user in users_dict_query:
        users_dict.update({user[0]:convertSQLToUser(user)})
    cursor.execute("SELECT * FROM Movies")
    movies_dict_query = cursor.fetchall()
    for movie in movies_dict_query:
        if movies_dict.get(movie[9]) is None:
            movies_dict.update({movie[9]:[convertSQLToFilm(movie)]})
        else:
            movies_dict[movie[9]] += [convertSQLToFilm(movie)]


def addUser(message):
    #search
    people_id = message.chat.id
    cursor.execute(f"SELECT id FROM Users Where id = {people_id}")
    data = cursor.fetchone()
    if data is None:
            #BD
            user_id = [message.chat.id, message.from_user.username,1]
            user_id_dict = { message.chat.id: User(message.chat.id,message.from_user.username,1)}
            cursor.execute("INSERT INTO Users VALUES(?,?,?);",user_id)
            connect.commit()
            #Dict
            users_dict.update(user_id_dict)
    else:
        print("Debug: Пользователь с id - " + str(people_id) + " уже существует в БД")

def addMovie(film_id, user_id):
    cursor.execute(f"SELECT id FROM Movies Where USER_ID = {user_id} and Kinopoisk_id = {film_id}")
    data = cursor.fetchone()
    Ikp_film_obj = Ikp.get_film_by_id(film_id)
    film_name = Ikp_film_obj.ru_name + ' (' + Ikp_film_obj.name + ')'
    if data is None:
            #info
            film_year = Ikp_film_obj.year
            film_url = Ikp_film_obj.kp_url
            film_genre = str(Ikp_film_obj.genres)
            film_category = Ikp_film_obj.category
            film_watched = 0        #По умолчанию не просмотрен
            film_desc = Ikp_film_obj.description
            #BD
            film_list = [film_name,film_year,film_id,film_url, film_genre, film_category, film_watched, film_desc, user_id]
            cursor.execute("INSERT INTO Movies( Name,Year,Kinopoisk_id,Kinopoisk_url,Genre,Category,Watched,Description,USER_ID) VALUES(?,?,?,?,?,?,?,?,?);",film_list)
            connect.commit()
            #dict
            f_obj = converIkpToFilm(Ikp_film_obj,user_id)
            if movies_dict.get(user_id) is None:
                movies_dict.update({user_id:[f_obj]})
            else:
                movies_dict[user_id] += [f_obj]
            return True
    else:
        print("Debug: Фильм - " + str(film_name) + " уже есть в списке пользователя с id" + str(user_id))
        return False

    #search

def addMovieByTitle(user_id, film_name):
    cursor.execute(f"SELECT id FROM Movies Where USER_ID = {user_id} and Name like '%{film_name}%'")
    data = cursor.fetchone()
    if data is None:
            #BD
            film_list = [user_id, film_name, 0,"Без категории"]
            cursor.execute("INSERT INTO Movies(USER_ID,Name,Watched,Category) VALUES(?,?,?,?);",film_list)
            connect.commit()
            #Dict
            f_obj = film.Film(user_id=user_id,name=film_name,sqlId=getNewSqlId())
            if movies_dict.get(user_id) is None:
                movies_dict.update({user_id:[f_obj]})
            else:
                movies_dict[user_id] += [f_obj]
            return True
    else:
        print("Debug: Фильм - " + str(film_name) + " уже есть в списке пользователя с id" + str(user_id))
        return False

def getUserFilms(user_id):
    return movies_dict.get(user_id)

def getUser(user_id):
    return users_dict.get(user_id)
    
def convertSQLToUser(user):
    return User(user[0],user[1],user[2])

def convertSQLToFilm(movie):
    return film.Film(movie[9],movie[1],movie[0],movie[2],movie[3],movie[4],movie[5],movie[6],movie[7], movie[8])

def converIkpToFilm(Ikp_film, user_id):
    return film.Film(user_id,Ikp_film.ru_name + ' (' + Ikp_film.name + ')',getNewSqlId(), Ikp_film.year, Ikp_film.kp_id, Ikp_film.kp_url, Ikp_film.genres,
                    Ikp_film.category, 0, Ikp_film.description)

def getNewSqlId():
    cursor.execute("Select max(id) from Movies")
    data = cursor.fetchone()
    return data[0]
    
def getUserMovieCategory(user_id,category):
    if category == 'Не просмотрено':
        return getUserMovieNonWatched(user_id)
    elif category == 'Просмотрено':
        return getUserMovieWatched(user_id)
    else:
        list=[]
        for f in movies_dict.get(user_id):
            if category in f.category:
                list.append(f)
        return list

def getUserMovieWatched(user_id):
    list=[]
    if movies_dict.get(user_id) is None:
        return list
    for f in movies_dict.get(user_id):
        if f.watched == 1:
            list.append(f)
    return list

def getUserMovieNonWatched(user_id):
    list=[]
    if movies_dict.get(user_id) is None:
        return list
    for f in movies_dict.get(user_id):
        if f.watched == 0:
            list.append(f)
    return list

def getUserCategories(user_id):
    list=[]
    if movies_dict.get(user_id) is None:
        return list
    for f in movies_dict.get(user_id):
        if f.category not in list:
            list.append(f.category)
    return list

def getFilmBySqlid(sqlid,user_id):
    for f in movies_dict.get(user_id):
        if f.sqlId == int(sqlid):
            return f

def getFilmIdxBySqlid(sqlid,user_id):
    for i,f in enumerate(movies_dict.get(user_id)):
        if f.sqlId == int(sqlid):
            return i

#Edit film

def editName(message,f_id,bot):
    if message.content_type != 'text':
            callback.editFilmName(bot,message,f_id)
            return
    if message.text == '❌ Отмена':
        bot.send_message(message.chat.id,'Изменение названия отменено',reply_markup=func.getStandKeyboa())
        func.writeFilmInfo(bot,message,f_id)
        return
    else:
        cursor.execute(f"UPDATE Movies SET Name = '{message.text}' WHERE USER_ID = {message.chat.id} and id = {f_id}")
        connect.commit()
        movies_dict[message.chat.id][getFilmIdxBySqlid(f_id,message.chat.id)].name = message.text
        bot.send_message(message.chat.id,'Название фильма изменено на ' + message.text,reply_markup=func.getStandKeyboa())
        func.writeFilmInfo(bot,message,f_id)
   
def editUrl(message,f_id,bot):
    if message.content_type != 'text':
            callback.editFilmUrl(bot,message,f_id)
            return
    if message.text == '❌ Отмена':
        bot.send_message(message.chat.id,'Изменение ссылки отменено',reply_markup=func.getStandKeyboa())
        func.writeFilmInfo(bot,message,f_id)
        return
    else:
        cursor.execute(f"UPDATE Movies SET Kinopoisk_url = '{message.text}' WHERE USER_ID = {message.chat.id} and id = {f_id}")
        connect.commit()
        movies_dict[message.chat.id][getFilmIdxBySqlid(f_id,message.chat.id)].kinopoisk_url = message.text
        bot.send_message(message.chat.id,'Ссылка на фильм изменена на ' + message.text,reply_markup=func.getStandKeyboa())
        func.writeFilmInfo(bot,message,f_id)
    
def editYear(message,f_id,bot):
    if message.content_type != 'text':
            callback.editFilmYear(bot,message,f_id)
            return
    if message.text == '❌ Отмена':
        bot.send_message(message.chat.id,'Изменение года отменено',reply_markup=func.getStandKeyboa())
        func.writeFilmInfo(bot,message,f_id)
        return
    else:
        cursor.execute(f"UPDATE Movies SET Year = '{message.text}' WHERE USER_ID = {message.chat.id} and id = {f_id}")
        connect.commit()
        movies_dict[message.chat.id][getFilmIdxBySqlid(f_id,message.chat.id)].year = message.text
        bot.send_message(message.chat.id,'Год фильма изменен на ' + message.text,reply_markup=func.getStandKeyboa())
        func.writeFilmInfo(bot,message,f_id)

def editGenre(message,f_id,bot):
    if message.content_type != 'text':
            callback.editFilmGenre(bot,message,f_id)
            return
    if message.text == '❌ Отмена':
        bot.send_message(message.chat.id,'Изменение жанров отменено',reply_markup=func.getStandKeyboa())
        func.writeFilmInfo(bot,message,f_id)
        return
    else:
        cursor.execute(f"UPDATE Movies SET Genre = '{message.text}' WHERE USER_ID = {message.chat.id} and id = {f_id}")
        connect.commit()
        movies_dict[message.chat.id][getFilmIdxBySqlid(f_id,message.chat.id)].genre = message.text
        bot.send_message(message.chat.id,'Жанры фильма изменены на ' + message.text,reply_markup=func.getStandKeyboa())
        func.writeFilmInfo(bot,message,f_id)

def editCategory(message,f_id,bot):
    if message.content_type != 'text':
            callback.editFilmCategory(bot,message,f_id)
            return
    if message.text == '❌ Отмена':
        bot.send_message(message.chat.id,'Изменение категории отменено',reply_markup=func.getStandKeyboa())
        func.writeFilmInfo(bot,message,f_id)
        return
    else:
        if len(message.text) > 20:
            msg = bot.send_message(message.chat.id,'Не более 20 символов для названия категории!\nПожалуйста, введите другое название категории',reply_markup=callback.cancelKeyboa())
            bot.register_next_step_handler(msg,editCategory,f_id,bot)
            return
        cursor.execute(f"UPDATE Movies SET Category = '{message.text}' WHERE USER_ID = {message.chat.id} and id = {f_id}")
        connect.commit()
        movies_dict[message.chat.id][getFilmIdxBySqlid(f_id,message.chat.id)].category = message.text
        bot.send_message(message.chat.id,'Категория изменена на ' + message.text,reply_markup=func.getStandKeyboa())
        func.writeFilmInfo(bot,message,f_id)

def editDesc(message,f_id,bot):
    if message.content_type != 'text':
            callback.editFilmDesc(bot,message,f_id)
            return
    if message.text == '❌ Отмена':
        bot.send_message(message.chat.id,'Изменение описания отменено',reply_markup=func.getStandKeyboa())
        func.writeFilmInfo(bot,message,f_id)
        return
    else:
        cursor.execute(f"UPDATE Movies SET Description = '{message.text}' WHERE USER_ID = {message.chat.id} and id = {f_id}")
        connect.commit()
        movies_dict[message.chat.id][getFilmIdxBySqlid(f_id,message.chat.id)].desc = message.text
        bot.send_message(message.chat.id,'Описание изменено на ' + str(message.text), reply_markup=func.getStandKeyboa())
        func.writeFilmInfo(bot,message,f_id)

def editWatch(message,f_id,bot,watched):
    cursor.execute(f"UPDATE Movies SET Watched = '{watched}' WHERE USER_ID = {message.chat.id} and id = {f_id}")
    connect.commit()
    movies_dict[message.chat.id][getFilmIdxBySqlid(f_id,message.chat.id)].watched = watched
    func.editFilmInfo(bot,message,f_id)

def deleteFilm(message,f_id,bot):
    if(message.text == "✔️ Да"):
        cursor.execute(f"DELETE FROM Movies WHERE USER_ID = {message.chat.id} and id = {f_id}")
        connect.commit()
        bot.send_message(message.chat.id,'Фильм '+ movies_dict[message.chat.id][getFilmIdxBySqlid(f_id,message.chat.id)].name + ' удален из списка',reply_markup=func.getStandKeyboa())
        movies_dict[message.chat.id].pop(getFilmIdxBySqlid(f_id,message.chat.id))
    else:
        bot.send_message(message.chat.id,'Удаление отменено',reply_markup=func.getStandKeyboa())
        return

#Edit user

def editTimer(user_id,timer):
    cursor.execute(f"UPDATE Users SET Timer = '{timer}' WHERE id = {user_id}")
    connect.commit()
    users_dict[user_id].timer = timer