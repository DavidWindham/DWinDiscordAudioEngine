from discord import Embed
from discord.utils import get

from .supporting_classes.db import ServerDB
from .supporting_classes.queue import Queue
from .supporting_classes.server_message import MessageHandler
from .supporting_classes.url_object import UrlObject
from .supporting_classes.voice_channel_handler.voice_channel import VoiceChannel


class Server:
    def __init__(self, mongo_db, server_id, discord_client):
        self.db = ServerDB(db=mongo_db, server_id=server_id)
        self.discord_client = discord_client
        self.queue = Queue()
        self.message_handler = MessageHandler(discord_client=discord_client)
        self.voice_channel = VoiceChannel()
        self.currently_playing = None
        self.playback_status = "Stopped"
        self.callback_block = False

    '''
    Playback specific methods
    '''

    async def play(self, voice_channel, voice_clients, guild_id, url=None):
        # if not already joined(?)
        if voice_clients is None:
            await self.join_voice_channel(voice_channel, guild_id)
        elif not voice_clients.is_connected():
            print("not connected")

        if url is None:
            # play voice channel with self.currently_playing
            if self.currently_playing is not None:
                self.voice_channel.play_url(self.currently_playing.get_url(), self.play_next)
                self.playback_status = "Playing"
            return

        url_object = UrlObject(url)
        self.db.append_to_history(url_object.get_dict())

        if not self.voice_channel.is_engine_playing():
            self.voice_channel.play_url(url_object.get_url(), self.play_next)
            self.currently_playing = url_object
            self.playback_status = "Playing"
            return

        self.queue.add_to_queue(
            url_object
        )

    def play_next(self):
        if self.callback_block:
            self.callback_block = False
            return

        self.stop()
        # TODO: I likely need some kinda pause or stop here
        if self.queue.is_empty():
            print("is empty so returning")
            return

        next_item_to_play = self.queue.get_next_from_queue()
        self.voice_channel.play_url(next_item_to_play.get_url(), self.play_next)
        self.currently_playing = next_item_to_play
        self.playback_status = "Playing"

    # def play(self):
    #     if self.currently_playing is not None:
    #         self.voice_channel.play()
    #         self.playback_status = "Playing"

    def pause(self):
        self.voice_channel.pause()
        self.playback_status = "Paused"

    def resume(self):
        self.voice_channel.resume()
        self.playback_status = "Playing"

    def stop(self):
        self.callback_block = True
        # this will fire the callback, TODO: fix the bug that comes with this
        self.voice_channel.stop()
        # self.currently_playing = None
        self.playback_status = "Stopped"

    '''
    VoiceChannel specific methods
    '''

    async def join_voice_channel(self, voice_channel, guild_id):
        await self.voice_channel.join_voice_channel(voice_channel)
        voice_clients = get(self.discord_client.voice_clients, guild=guild_id)
        self.voice_channel.set_engine_interface(voice_clients)

    async def leave_voice_channel(self, voice_channel):
        await self.voice_channel.leave_voice_channel(voice_channel)

    '''
    Queue specific methods
    '''

    def remove_item_from_queue(self, idx):
        self.queue.remove_item_from_queue(idx)

    def clear_queue(self):
        self.queue.empty_queue()

    '''
    Message specific methods
    '''

    # def set_server_message(self, message):
    #     self.message_handler.set_message(message)

    # async def update_or_create_server_message(self, channel):
    #     print("Update called")
    #     try:
    #         print("Trying to update")
    #         await self.update_server_message()
    #     except:
    #         print("update failed, now trying to create")
    #         await self.create_server_message(channel)

    async def create_server_message(self, channel):
        embedded_content = get_embedded_message_content(
            queue=self.queue.get_queue(),
            currently_playing=self.currently_playing,
            playback_status=self.playback_status
        )
        await self.message_handler.create_embedded_message(channel=channel, embedded_content=embedded_content)

    async def update_server_message(self, channel=None):
        embedded_content = get_embedded_message_content(
            queue=self.queue.get_queue(),
            currently_playing=self.currently_playing,
            playback_status=self.playback_status
        )
        await self.message_handler.update_embedded_message(embedded_content=embedded_content, channel=channel)

    '''
    Database specific methods
    '''

    def get_history(self, limit=10):
        self.db.get_history(limit=limit)


def get_embedded_message_content(queue, currently_playing, playback_status):
    embedded_message = Embed(title="Queue", color=0xeb4034)

    if len(queue) == 0 and currently_playing is None:
        embedded_message.add_field(name="Empty", value="Add some tunes", inline=False)
        return embedded_message

    embedded_message.insert_field_at(
        index=0,
        name=playback_status,
        value="_",
        inline=False
    )

    if currently_playing is not None:
        get_single_item_field(embedded_message, currently_playing, name_prefix="Now Playing: ")
        embedded_message.set_image(url=currently_playing.thumbnail_link)

    for idx, item in enumerate(queue):
        get_single_item_field(embedded_message, item, name_prefix=str(idx + 1) + ". ")

    return embedded_message


def get_single_item_field(embed, item, name_prefix):
    embed.insert_field_at(
        index=0,
        name=name_prefix + item.title,
        value=str(item.duration_string),
        inline=False
    )
