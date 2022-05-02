from database.mongo.mongo_DB import MongoDB
from database.stateless.stateless_DB import StatelessDB

def get_db(server_uri: str, server_port: str):
    if server_uri is not None or server_uri == "" or server_port is not None or server_port == "":
        #return MongoDB(server_uri, int(server_port))
        return StatelessDB()

    return None
