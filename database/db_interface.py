from Server.server import Server
from database.mongo.mongo_DB import MongoDB


def get_db(server_uri: str, server_port: str):
    if server_uri is not None or server_uri == "" or server_port is not None or server_port == "":
        return MongoDB(server_uri, int(server_port))

    return None


def load_servers(db, client):
    servers_info = db.load_all_server_info()
    server_dict = {}

    for server in servers_info:
        server_dict[server['server_id']] = Server(
            mongo_db=db,
            server_id=server['server_id'],
            discord_client=client
        )
    return server_dict