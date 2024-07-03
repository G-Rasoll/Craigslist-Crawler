import json
from abc import ABC, abstractmethod
from mongo import MongoSet
from pymongo import MongoClient


class StorageBase(ABC):
    @abstractmethod
    def storing(self, data, filename, *args):
        pass

    @abstractmethod
    def load(self, *args, **kwargs):
        pass

    @abstractmethod
    def update_flag(self, data):
        pass


class MongoStore(StorageBase):
    def __init__(self):
        self.client = MongoSet()

    def storing(self, data, collection_name, *args):
        # collection = self.client.database[collection_name]
        collection = getattr(self.client.database, collection_name)
        if isinstance(data, list) and len(data) > 1:
            collection.insert_many(data)
            print(collection)
        else:
            collection.insert_one(data)
            # print(collection)

    def load(self, collection_name, filter_data=None):
        collection = self.client.database[collection_name]
        if filter_data is not None:
            data = collection.find(filter_data)
        else:
            data = collection.find()
        return data

    def update_flag(self, data):

        self.client.database.advertisement_links.find_one_and_update(
            {'_id': data['_id']},
            {'$set': {'flag': True}}
        )


class FileStorage(StorageBase):

    @staticmethod
    def storing(data, filename, *args):
        if filename == "advertisement_data":
            filename = filename = filename + '-' + data['post_id']
        with open(f'data/adv/{filename}.json', "w") as f:
            json.dump(data, f, indent=4)

    def load(self, file_name, filter_data=None):
        with open(f"data/adv/{file_name}.json", "r") as f:
            link_page = json.load(f)

        result_link = list(filter(lambda item: item["flag"] != True, link_page))
        return result_link


    def load_file(self):
        pass

    def update_flag(self, data):
        with open("data/adv/advertisement_links.json", "r") as f:
            link_page = json.load(f)

        for link in link_page:
            if link["url"] == data["url"]:
                link["flag"] = True
                break

        with open("data/adv/advertisement_links.json", "w") as f:
            json.dump(link_page, f, indent=4)
