from auxillary.Server.message_creator import get_embedded_message_from_queue


class MessageHandler:
    def __init__(self, discord_client, message=None):
        self.discord_client = discord_client
        self.message = message

    def set_message(self, message):
        self.message = message

    async def update_message(self, queue):
        if self.message is None:
            return
        message_to_send = get_embedded_message_from_queue(queue=queue)
        try:
            await self.message.edit(
                embed=message_to_send
            )
        except:
            self.message = None
