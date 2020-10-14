import pymongo
from config import systemConfig
from bson.json_util import dumps
import json
from time import time


class Executionary:

    def __init__(self):
        mongodb_url = systemConfig.get_mongo_url()
        db_name = systemConfig.mongodb_database

        self.client = pymongo.MongoClient(mongodb_url)

        self.database = self.client[db_name]

    @staticmethod
    def mongo_doc_to_json(doc):
        data = list(doc)
        return data

    def get_document_count(self, collection, filters):
        query = {}
        if filters:
            query.update(filters)

        collection_count = self.database[collection].count_documents(query)

        return collection_count

    def get_all_data(self, collection, filters=None):
        query = {}
        if filters != None:
            query.update(filters)
        data_ob = self.database[collection].find(query, {"_id": 0})

        data = Executionary.mongo_doc_to_json(data_ob)
        return data

    def register_token(self, data):
        try:
            self.database["users"].insert(data)
            return True
        except Exception:
            return None

    def get_user(self, user, password):

        query = {"username": {"$eq": user}, "password": {"$eq": password}}
        collection_count = self.database['rr_users'].count_documents(query)
        return collection_count

    def insert_data(self, collection, data):
        self.database[collection].insert_one(data)

    def remove_data(self, collection, id, value):

        self.database[collection].delete_many({id: {"$in": value}})
