from Server.server import Server


class ServersHandler:
    def __init__(self, db, client):
        self.db = db
        self.client = client
        self.servers = {}
        self.load_servers()

    def load_servers(self):
        servers_info = self.db.load_all_server_info()
        self.servers = {}

        for server in servers_info:
            self.servers[server['server_id']] = Server(
                mongo_db=self.db,
                server_id=server['server_id'],
                discord_client=self.client
            )

    def get_server(self, ctx):
        if ctx.guild.id not in self.servers:
            self.servers[ctx.guild.id] = Server(
                mongo_db=self.db,
                server_id=ctx.guild.id,
                discord_client=self.client
            )
            self.db.add_server(ctx.guild.id)
        return self.servers[ctx.guild.id]
