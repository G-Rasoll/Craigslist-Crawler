import json
from pymongo import MongoClient
import datetime


def create_db():
    # اتصال به پایگاه داده MongoDB
    client = MongoClient('localhost', 27017)

    # انتخاب دیتابیس "crawler"
    db = client["crawler"]

    # انتخاب کلکسیون "advertisement_links"
    collection = db["advertisement_links"]

    # پیدا کردن و به‌روزرسانی اسناد با فیلد "flag" برابر False
    result = collection.update_many(
        {"flag": True},
        {"$set": {"flag": False}}
    )

    # چاپ تعداد اسنادی که به‌روزرسانی شده‌اند
    print(f"Number of documents updated: {result.modified_count}")

    # کدهای زیر کامنت شده‌اند، در صورت نیاز آن‌ها را فعال کنید
    # db = client["test_database"]
    # collection1 = db["collection1"]
    # collection2 = db["collection2"]
    # with open("data/adv/data.json", "r") as f:
    #     list_item = json.load(f)
    # collection2.insert_many(list_item)
    # print(list_item)


if __name__ == "__main__":
    create_db()
