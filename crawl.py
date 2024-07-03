import json
from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup
from config import Link, STORAGE_TYPE
from parser import AdvertisementParser
from storage import MongoStore, FileStorage


class BaseCrawler(ABC):

    def __init__(self):
        self.storage = self.__storage_set()

    @staticmethod
    def __storage_set():
        if STORAGE_TYPE == "mongo":
            return MongoStore()
        return FileStorage()

    @abstractmethod
    def start(self, store=False):
        pass

    @abstractmethod
    def store(self, data=None, filename=None):
        pass

    def get(self, url):
        try:
            res = requests.get(url)
        except:
            return None
        return res


class LinkCrawler(BaseCrawler):

    def __init__(self, cities, link=Link):
        self.cities = cities
        self.link = link
        super().__init__()

    def find_li(self, html_doc):
        soup = BeautifulSoup(html_doc, 'html.parser')
        elements = soup.find_all("li")
        return elements

    def find_links(self, li_tags):
        count = 0
        a_tag_list = list()
        for li_tag in li_tags:
            a_tags = li_tag.find_all("a")
            for a_tag in a_tags:
                a_tag_list.append(a_tag.get('href'))
        return a_tag_list

    def start(self, store=False):
        adv_links = list()
        for city in self.cities:
            response = self.get(self.link.format(city))
            li_tags = self.find_li(response.text)
            links = self.find_links(li_tags)
            print(f"{city}: {len(links)}")
            adv_links.extend(links)

        if store:
            adv_links = [{"url": i, "flag": False} for i in adv_links]
            self.store(adv_links, "data")

    def store(self, links, filename, *args):

        self.storage.storing(links, "advertisement_links")


class DataCrawler(BaseCrawler):

    def __init__(self):
        super().__init__()
        self.links = self.__load_links()
        self.adver = AdvertisementParser()

    def __load_links(self):
        # with open("data/adv/advertisement_links.json", "r") as f:
        #     link_page = json.load(f)
        self.link_page = self.storage.load("advertisement_links",
                                           {"flag": False})
        return self.link_page

    def start(self, store=False):
        for link in self.links:
            response = self.get(link["url"])
            data = self.adver.parser(response.content)
            if store:
                self.store(data, data.get("post_id", "sample"))

            self.storage.update_flag(link)

    def store(self, data=None, filename=None):

        self.storage.storing(data, "advertisement_data")


class ImageCrwaler(BaseCrawler):
    def __init__(self):
        super().__init__()
        self.advertisments = self.__loads_advertisments()

    def __loads_advertisments(self):
        return self.storage.load("advertisement_data")

    def get(self, url):
        try:
            response = requests.get(url, stream=True)
        except requests.HTTPError:
            return None
        return response

    def start(self, store=True):
        for advertisment in self.advertisments:
            counter = 0
            for image in advertisment["images"]:
                response = self.get(image["url"])
                if store:
                    self.store(response, advertisment["post_id"], counter)
                counter = counter + 1

    def store(self, data, adv_id, image_number):
        filename = f"{adv_id}-{image_number}"
        return self.save_to_disk(data, filename)

    def save_to_disk(self, response, filname):
        with open(f"data/images/{filname}.jpg", "ab") as f:
            f.write(response.content)
            for _ in response.iter_content():
                f.write(response.content)
        print(filname)
        return filname
