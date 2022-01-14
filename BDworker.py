import sqlite3
import kinopoisk
import film

users_dict = {}
movies_dict_query = {}
movies_dict = {}

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
    for movie in movies_dict_query:
        if movies_dict.get(movie[9]) is None:
            movies_dict.update({movie[9]:[convertToFilm(movie)]})
        else:
            movies_dict[movie[9]] += [convertToFilm(movie)]


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
    if data is None:
            #info
            film_name = kinopoisk.getFullName(film_id)
            film_year = kinopoisk.getYear(film_id)
            film_url = kinopoisk.getUrl(film_id)
            film_genre = convertGenretoStr(kinopoisk.getGenres(film_id))
            film_category = kinopoisk.getCategory(film_id) 
            film_watched = 0        #По умолчанию не просмотрен
            film_desc = kinopoisk.getDescription(film_id)
            #BD
            film_list = [film_name,film_year,film_id,film_url, film_genre, film_category, film_watched, film_desc, user_id]
            cursor.execute("INSERT INTO Movies( Name,Year,Kinopoisk_id,Kinopoisk_url,Genre,Category,Watched,Description,USER_ID) VALUES(?,?,?,?,?,?,?,?,?);",film_list)
            connect.commit()
            #dict
            f_obj = film.Film(user_id,film_name,film_year,film_id,film_url, film_genre, film_category, film_watched, film_desc)
            if movies_dict.get(user_id) is None:
                movies_dict.update({user_id:[f_obj]})
            else:
                movies_dict[user_id] += [f_obj]
            return True
    else:
        print("Debug: Фильм - " + str(film_name) + " уже есть в списке пользователя с id" + str(user_id))
        return false

    #search

def addMovieByTitle(user_id, film_name):
    cursor.execute(f"SELECT id FROM Movies Where USER_ID = {user_id} and Name like '%{film_name}%'")
    data = cursor.fetchone()
    if data is None:
            #BD
            film_list = [user_id, film_name]
            cursor.execute("INSERT INTO Movies(USER_ID,Name) VALUES(?,?);",film_list)
            connect.commit()
            #Dict
            f_obj = film.Film(user_id=user_id,name=film_name )
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
    
def convertToFilm(movie):
    return film.Film(movie[9],movie[1],movie[2],movie[3],movie[4],movie[5],movie[6],movie[7], movie[8])

def convertGenretoStr(genre_obj):
    if genre_obj is None: return None
    genres = ""
    for g in genre_obj:
       genres += g.genre + " "
    return genres