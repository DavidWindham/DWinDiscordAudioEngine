from .url_object import UrlObject
from .server_supplemental_classes.server_core import ServerCore


class ServerHandler(ServerCore):
    def __init__(self, server_id, discord_client):
        super().__init__(discord_client)
        self.server_id = server_id
        self.queue = []

    async def add_url(self, ctx, url):
        # check if connected to voice channel
        if self.voice_channel is None:
            await self.join_voice_channel(ctx)

        # check if audio interface has been established
        if self.audio_engine.is_audio_interface_set() is False:
            self.set_audio_engine_interface(ctx)

        self.add_to_queue(url)
        # if audio_engine isn't playing, play the next in queue (the song that was just added)
        if not self.audio_engine.is_engine_playing():
            self.play_next_url_in_queue()

    def play_next_url_in_queue(self):
        next_item = self.queue.pop(0)
        self.audio_engine.play_item(next_item.url, self.play_next_url_in_queue)

    def add_to_queue(self, url):
        self.queue.append(
            UrlObject(url)
        )

    # def remove_from_queue(self, url):
    #     url_found_in_queue = False
    #     for idx, url_obj in enumerate(self.queue):
    #         if url_obj.url == url:
    #             idx_to_pop = idx
    #             url_found_in_queue = True
    #             break
    #
    #     if url_found_in_queue:
    #         self.queue.pop(idx_to_pop)
    #
    # def remove_from_queue_at_index(self, idx):
    #     self.queue.pop(idx)
    #
    # def get_queue(self):
    #     return self.queue
    #
    # def get_queue_text(self):
    #     pass
