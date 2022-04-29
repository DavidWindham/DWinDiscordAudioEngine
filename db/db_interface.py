from db.mongo.mongo_DB import MongoDB
from auxillary.server_class import ServerHandler

def get_db(server_uri: str, server_port: str):
    if server_uri is not None or server_uri == "" or server_port is not None or server_port == "":
        return MongoDB(server_uri, int(server_port))

    return None


def load_servers(db, client):
    servers_info = db.load_all_server_info()
    server_dict = {}

    for server in servers_info:
        print(server)
        server_dict[server['server_id']] = ServerHandler(
            db=db,
            server_id=server['server_id'],
            discord_client=client
        )
    return server_dict
