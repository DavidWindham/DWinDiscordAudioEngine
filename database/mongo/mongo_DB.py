from pymongo import MongoClient

from database.abstracts.base import DB
from .server_db_object import get_mongo_server_object


class MongoDB(DB):
    def __init__(self, db_server_address, db_port):
        self.db_server_address = db_server_address
        self.db_port = db_port
        self.client = None
        self.db = None

    def connect(self):
        # if this fails, I need some kinda checking, maybe just break the program
        # or just resort back to stateless
        # for now, let's ignore checking
        self.client = MongoClient(host=self.db_server_address, port=self.db_port)
        self.db = self.client.DWinAudioEngine

    def add_server(self, server_id: int):
        # TODO: need a check if the server already exists
        server_obj = get_mongo_server_object(server_id)
        self.db.servers.insert_one(server_obj)

    def update_server_info(self, server_id: int, queue_message_id: int = None, history: list = None) -> None:
        db_server_obj = self.db.servers.find_one({'server_id': server_id})
        updated_server_obj = get_mongo_server_object(
            server_id=server_id,
            queue_message_id=queue_message_id
        )
        self.db.servers.update_one({'_id': db_server_obj.get('_id')}, {"$set": updated_server_obj})

    def load_all_server_info(self):
        # TODO: Add probably decorators on all these functions to ensure DB connection is successful?
        return self.db.servers.find({})

    def load_single_server_info(self, server_id: int):
        return self.db.find_one({'server_id': server_id})

    def add_item_to_server_history(self, server_id: int, item_to_add: dict):
        self.db.servers.update_one({'server_id': server_id}, {"$push": {'history': item_to_add}})

    def get_server_history(self, server_id, limit=10):
        # TODO: No functionality here yet
        test = self.db.find_one({'server_id': server_id}, {"history"}).limit(limit)
        return []

    def get_queue_message_id(self, server_id: int) -> int or None:
        return self.db.servers.find_one({'server_id': server_id}, {"queue_message_id"})['queue_message_id']

    def set_queue_message_id(self, server_id: int, queue_message_id: int):
        self.db.servers.update_one({'server_id': server_id}, {"$set": {'queue_message_id': queue_message_id}})
