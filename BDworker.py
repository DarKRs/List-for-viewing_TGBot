import sqlite3
import kinopoisk
import film
import Ikp
import func

users_dict = {}
movies_dict_query = {}
movies_dict = {}
id_movie_sql = 1

connect = sqlite3.connect('Main.db',check_same_thread=False)
cursor = connect.cursor()

def Init():
    #Users
    cursor.execute("""CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY,
        UserName TEXT
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
    users_dict = cursor.fetchall()
    cursor.execute("SELECT * FROM Movies")
    movies_dict_query = cursor.fetchall()
    global id_movie_sql
    id_movie_sql = movies_dict_query[-1][0]
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
            user_id = [message.chat.id, message.from_user.username]
            user_id_dict = { message.chat.id: message.from_user.username}
            cursor.execute("INSERT INTO Users VALUES(?,?);",user_id)
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
            global id_movie_sql
            f_obj = converIkpToFilm(Ikp_film_obj,user_id)
            id_movie_sql +=1
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
            film_list = [user_id, film_name, 0]
            cursor.execute("INSERT INTO Movies(USER_ID,Name,Watched) VALUES(?,?,?);",film_list)
            connect.commit()
            #Dict
            global id_movie_sql
            f_obj = film.Film(user_id=user_id,name=film_name,sqlId=id_movie_sql)
            id_movie_sql += 1
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
    
def convertSQLToFilm(movie):
    return film.Film(movie[9],movie[1],movie[0],movie[2],movie[3],movie[4],movie[5],movie[6],movie[7], movie[8])

def converIkpToFilm(Ikp_film, user_id):
    return film.Film(user_id,Ikp_film.ru_name + ' (' + Ikp_film.name + ')',id_movie_sql, Ikp_film.year, Ikp_film.kp_id, Ikp_film.kp_url, Ikp_film.genres,
                    Ikp_film.category, 0, Ikp_film.description)

#Edit film

def editName(message,idx,bot):
    f_id = getUserFilms(message.chat.id)[int(idx)].sqlId
    cursor.execute(f"UPDATE Movies SET Name = '{message.text}' WHERE USER_ID = {message.chat.id} and id = {f_id}")
    connect.commit()
    movies_dict[message.chat.id][int(idx)].name = message.text
    bot.send_message(message.chat.id,'Название фильма изменено на ' + message.text)
    func.writeFilmInfo(bot,message,idx)
    
def editUrl(message,idx,bot):
    f_id = getUserFilms(message.chat.id)[int(idx)].sqlId
    cursor.execute(f"UPDATE Movies SET Kinopoisk_url = '{message.text}' WHERE USER_ID = {message.chat.id} and id = {f_id}")
    connect.commit()
    movies_dict[message.chat.id][int(idx)].kinopoisk_url = message.text
    bot.send_message(message.chat.id,'Ссылка на фильм изменена на ' + message.text)
    func.writeFilmInfo(bot,message,idx)
    
def editYear(message,idx,bot):
    f_id = getUserFilms(message.chat.id)[int(idx)].sqlId
    cursor.execute(f"UPDATE Movies SET Year = '{message.text}' WHERE USER_ID = {message.chat.id} and id = {f_id}")
    connect.commit()
    movies_dict[message.chat.id][int(idx)].year = message.text
    bot.send_message(message.chat.id,'Год фильма изменен на ' + message.text)
    func.writeFilmInfo(bot,message,idx)

def editGenre(message,idx,bot):
    f_id = getUserFilms(message.chat.id)[int(idx)].sqlId
    cursor.execute(f"UPDATE Movies SET Genre = '{message.text}' WHERE USER_ID = {message.chat.id} and id = {f_id}")
    connect.commit()
    movies_dict[message.chat.id][int(idx)].genre = message.text
    bot.send_message(message.chat.id,'Жанры фильма изменены на ' + message.text)
    func.writeFilmInfo(bot,message,idx)

def editCategory(message,idx,bot):
    f_id = getUserFilms(message.chat.id)[int(idx)].sqlId
    cursor.execute(f"UPDATE Movies SET Category = '{message.text}' WHERE USER_ID = {message.chat.id} and id = {f_id}")
    connect.commit()
    movies_dict[message.chat.id][int(idx)].category = message.text
    bot.send_message(message.chat.id,'Категория изменена на ' + message.text)
    func.writeFilmInfo(bot,message,idx)

def editDesc(message,idx,bot):
    f_id = getUserFilms(message.chat.id)[int(idx)].sqlId
    cursor.execute(f"UPDATE Movies SET Description = '{message.text}' WHERE USER_ID = {message.chat.id} and id = {f_id}")
    connect.commit()
    movies_dict[message.chat.id][int(idx)].desc = message.text
    bot.send_message(message.chat.id,'Описание изменено ' + message.text)
    func.writeFilmInfo(bot,message,idx)

def editWatch(message,idx,bot,watched):
    f_id = getUserFilms(message.chat.id)[int(idx)].sqlId
    cursor.execute(f"UPDATE Movies SET Watched = '{watched}' WHERE USER_ID = {message.chat.id} and id = {f_id}")
    connect.commit()
    movies_dict[message.chat.id][int(idx)].watched = watched
    func.editFilmInfo(bot,message,idx)