class MessageHandler:
    def __init__(self, discord_client, message=None):
        self.discord_client = discord_client
        self.message = message

    async def post_message(self, channel, embedded_content):
        self.message = await channel.send(embed=embedded_content)

    def set_message(self, message):
        self.message = message

    async def update_embedded_message(self, channel, embedded_content):
        if self.message is None:
            await self.post_message(channel, embedded_content)
            return

        try:
            await self.message.edit(
                embed=embedded_content
            )
        except:
            # Likely will fire if message has been deleted
            print("Cannot edit server message")
            self.message = None
