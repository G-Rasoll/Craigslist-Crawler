from pymongo import MongoClient


class MongoSet:
    instance = None

    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls.instance == None:
            cls.instance = super().__new__(*args, **kwargs)
        return cls.instance

    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.database = self.client["crawler"]
