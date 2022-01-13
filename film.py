class Film:
    """description of class"""

    def __init__(self, user_id, id, name, year, url, category, watched, desc):
        self.user = user_id
        self.id = id
        self.name = name
        self.year = year
        self.url = url
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