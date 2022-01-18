class Film:
    """description of class"""

    def __init__(self, user_id, name, sqlId=None,  year=None, kinopoisk_id=None, kinopoisk_url=None, genre=None,  category=None, watched=0, desc=None):
        self.sqlId = sqlId
        self.user = user_id
        self.kinopoisk_id = kinopoisk_id
        self.name = name
        self.year = str(year)
        self.kinopoisk_url = kinopoisk_url
        self.genre = genre
        self.category = category
        self.watched = watched
        self.desc = desc

    def getUser(self):
        return self.user

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getYear(self):
        return self.year

    def getUrl(self):
        return self.url

    def getCategory(self):
        return self.category

    def getWatched(self):
        return self.watched

    def getDesc(self):
        return self.desc