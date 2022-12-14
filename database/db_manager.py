import datetime
import json
from typing import Union
import random
from pymongo import MongoClient
from bson.json_util import dumps, loads

import os
import uuid


# Now you can perfom any CRUD operations on the DB
# testes
# colecao
class DBManager:
    client = None
    MONGODB_HOST = None
    MONGODB_PORT = None
    MONGODB_PWD = None
    MONGODB_USER = None

    @staticmethod
    def set_var_if_exists(var_name, default):
        if os.environ is None:
            return default

        value = default
        try:
            value = os.environ[var_name]
            if value is None:
                return default
        except Exception as e:
            print(e)
            return default
        return os.environ[var_name]

    def __init__(self):
        self.MONGODB_HOST = self.set_var_if_exists("MONGODB_HOST", "localhost")
        self.MONGODB_PORT = self.set_var_if_exists("MONGODB_PORT", "27017")
        self.MONGODB_PWD = self.set_var_if_exists("MONGODB_PWD", "root")
        self.MONGODB_USER = self.set_var_if_exists("MONGODB_USER", "root")

        connection_url = "mongodb://" + self.MONGODB_USER + ":" + self.MONGODB_PWD + "@" + self.MONGODB_HOST + ":" + self.MONGODB_PORT
        print(connection_url)
        self.client = MongoClient(connection_url)

    def toJson(self, json_object, format_json=False):
        if format_json:
            return json.loads(dumps(json_object))
        return json_object

    def list_all(self, db_name: str, collection: str, filter: Union[dict, None] = None):
        db = self.client[db_name]
        collection = db[collection]
        cursor = None
        if filter is not None:
            cursor = collection.find(filter)
            list_cur = list(cursor)
            return self.toJson(list_cur, True)
        cursor = collection.find()
        list_cur = list(cursor)
        return self.toJson(list_cur, True)

    def add_track(self, artist_id, album_id, track_id):
        db = self.client['spotipy_db']
        collection = db['tracks']
        collection.insert_one({
            'artist_id': artist_id,
            'album_id': album_id,
            'track_id': track_id
        })

    def add_album(self, album):
        db = self.client['spotipy_db']
        collection = db['album']
        collection.insert_one(album)

    def find_artist(self, artist):
        db = self.client['spotipy_db']
        collection = db['artist']
        return collection.find_one(artist)

    def find_tracks_by_artist(self, artist_id, limit=5):
        db = self.client['spotipy_db']
        collection = db['tracks']
        cursor = collection.aggregate([
            {'$match': {'artist_id': artist_id}},
            {'$sample': { 'size': limit}},
            # {'$match': {'$expr': {'$lte': [0, {'$rand': {}}]}}},
            # {'$limit': limit}
        ])
        # cursor = collection.find({'artist_id': artist_id, '$expr': {'$lt': [0.5, {'$rand: {}'}]}}).limit(limit)
        return list(cursor)

    def add_artist(self, artist):
        db = self.client['spotipy_db']
        collection = db['artist']
        collection.insert_one(artist)

    def insert(self, db_name: str, collection: str, data: dict):
        db = self.client[db_name]
        collection = db[collection]
        try:
            collection.insert_one(data)
            saved = collection.find_one(data)
            return self.toJson({'response': 'Saved', 'success': True, 'saved': self.toJson(saved, True)})
        except Exception as e:
            print(e)
            return self.toJson({'response': 'Can\'t save', 'success': False})

    def store_item(self, data: dict):
        db = self.client['generics']
        collection = db['objects']
        uuid_str = str(uuid.uuid4())
        generic_data = {
            "uuid": uuid_str,
            "data": data,
            "date_created": datetime.datetime.utcnow()
        }
        try:
            result = collection.insert_one(generic_data)
            if not result.acknowledged:
                return self.toJson({'response': 'Can\'t save', 'success': False})
            return self.toJson({'response': 'Saved', 'success': True, 'uuid': uuid_str})
        except Exception as e:
            print(e)
            return self.toJson({'response': 'Can\'t save', 'success': False})

    def get_item(self, uuid_str: str):
        db = self.client['generics']
        collection = db['objects']

        filter_obj = {
            "uuid": uuid_str
        }
        try:
            founded = collection.find_one(filter_obj)
            return self.toJson({'response': 'Founded', 'success': True, 'data': self.toJson(founded, True)})
        except Exception as e:
            print(e)
            return self.toJson({'response': 'Can\'t save', 'success': False})

    def update_item(self, uuid_str: str, data: dict):
        db = self.client['generics']
        collection = db['objects']

        filter_obj = {
            "uuid": uuid_str
        }
        try:
            collection.update_one(filter_obj, {"$set": {
                "data": data,
                "date_updated": datetime.datetime.utcnow()
            }})
            founded = collection.find_one(filter_obj)
            return self.toJson({'response': 'Founded', 'success': True, 'data': self.toJson(founded, True)})
        except Exception as e:
            print(e)
            return self.toJson({'response': 'Can\'t update', 'success': False})

    def get_last_topic(self, topic: str):
        db = self.client['mqtt']
        collection = db['topics']
        filter_obj = {'topic': topic}
        return self.toJson(collection.find_one(filter_obj), True)

    def save_last_topic(self, topic: str, data: dict):
        db = self.client['mqtt']
        collection = db['topics']
        filter_obj = {'topic': topic}
        cursor = collection.find_one(filter_obj)
        if cursor is None:
            try:
                collection.insert_one(data)
                return self.toJson({'response': 'Saved', 'success': True, 'data': data})
            except Exception as e:
                print(e)
                return self.toJson({'response': 'Can\'t save', 'success': False})

        try:
            collection.update_one(filter_obj, {"$set": data})
            return self.toJson({'response': 'Saved', 'success': True, 'data': data})
        except Exception as e:
            print(e)
            return self.toJson({'response': 'Can\'t save', 'success': False})
