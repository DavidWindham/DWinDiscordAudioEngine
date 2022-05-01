class MessageHandler:
    def __init__(self, discord_client, message=None):
        self.discord_client = discord_client
        self.message = message

    async def post_message(self, channel, embedded_content):
        self.message = await channel.send(embed=embedded_content)

    async def delete_old_message(self):
        try:
            print("attempting to delete")
            await self.message.delete()
            print("delete should be successful")
        except:
            print("Old message was not found")

    async def create_message(self, channel, embedded_content):
        if self.message is not None:
            await self.delete_old_message()

        await self.post_message(channel, embedded_content)

    async def handle_message(self, embedded_content, channel=None):
        if self.message is not None:
            try:
                await self.message.edit(
                    embed=embedded_content
                )
                return
            except:
                # Likely will fire if message has been deleted
                print("Cannot edit server message")
                self.message = None

        if channel is not None:
            await self.create_message(channel=channel, embedded_content=embedded_content)
