import sqlite3
import kinopoisk

users_dict = {}
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
        Kinopoisk TEXT,
        Category TEXT,
        Watched INTEGER,
        Description TEXT
        USER_ID INTEGER
    )""")
    connect.commit()

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

def addMovie(back):
    #info
    people_id = call.message.chat.id
    film_id = search_film_api(call.message.text)
    film_name = getFullName(film_id)
    film_year = getYear(film_id)
    film_url = getUrl(film_id)
    film_category = getCategory(film_id) 
    film_watched = 0        #По умолчанию не просмотрен
    film_desc = getDescription(film_id)

    #search

def addMovieByTitle(user_id, film_name):
    cursor.execute(f"SELECT id FROM Movies Where USER_ID = {user_id} and Name like '%{film_name}%'")
    data = cursor.fetchone()
    if data is None:
            #BD
            film = [user_id, film_name]
            cursor.execute("INSERT INTO Movies(USER_ID,Name) VALUES(?,?);",film)
            connect.commit()
            #Dict
            movies_dict.update(film)
    else:
        print("Debug: Фильм - " + str(film_name) + " уже есть в списке пользователя с id" + str(user_id))