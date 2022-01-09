import sqlite3

connect = sqlite3.connect('Main.db')
cursor = connect.cursor()

def Init():
    #Users
    cursor.execute("""CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY
    )""")
    connect.commit()

    #Movie
    cursor.execute("""CREATE TABLE IF NOT EXISTS Movies(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        Name TEXT,
        Kinopoisk TEXT,
        Category TEXT,
        Watched INTEGER,
        USER_ID INTEGER
    )""")
    connect.commit()

def addUser(message):
    #search
    people_id = message.chat.id
    cursor.execute(f"SELECT id FROM Users Where id = {people_id}")
    data = cursor.fetchone()
    if data is None:
            #values
            user_id = [message.chat.id]
            cursor.execute("INSERT INTO Users VALUES(?);",user_id)
            connect.commit()
    else:
        print("Debug: Пользователь с id - " + str(people_id) + " уже существует в БД")

def addMovie():
    pass