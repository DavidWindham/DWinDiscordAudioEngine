from .url_object import UrlObject
from .server_supplemental_classes.server_core import ServerCore
from .message_creator import get_embedded_message_from_queue


class ServerHandler(ServerCore):
    def __init__(self, server_id, discord_client):
        super().__init__(discord_client)
        self.server_id = server_id
        self.queue = []

    def is_queue_empty(self):
        if len(self.queue) == 0:
            return True

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
        next_item = self.queue[0]
        self.audio_engine.play_item(next_item.url, self.go_to_next_item)

    def skip(self):
        self.stop()
        self.go_to_next_item()

    def go_to_next_item(self):
        self.queue.pop(0)
        if len(self.queue) == 0:
            return
        self.play_next_url_in_queue()

    def add_to_queue(self, url):
        self.queue.append(
            UrlObject(url)
        )

    def clear_queue(self):
        self.queue = []
        self.stop()

    def remove_from_queue_at_index(self, idx):
        self.queue.pop(idx)

    def get_embedded_queue_message(self):
        return get_embedded_message_from_queue(self.queue)

    def play(self):
        self.audio_engine.play()

    def pause(self):
        self.audio_engine.pause()

    def resume(self):
        self.audio_engine.resume()

    def stop(self):
        self.audio_engine.stop()
