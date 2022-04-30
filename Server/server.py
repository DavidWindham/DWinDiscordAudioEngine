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
        self.callback_block = False

    '''
    Playback specific methods
    '''

    async def play(self, voice_channel, voice_clients, guild_id, url=None):
        # if not already joined(?)
        if voice_clients is None:
            print("it was none")
            await self.join_voice_channel(voice_channel, guild_id)
        elif not voice_clients.is_connected():
            print("not connected")

        if url is None:
            # play voice channel
            await self.voice_channel.play()

        url_object = UrlObject(url)
        print(url_object.get_dict())
        self.db.append_to_history(url_object.get_dict())

        if not self.voice_channel.is_engine_playing():
            self.voice_channel.play_url(url_object.get_url(), self.play_next)
            self.currently_playing = url_object
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

    def pause(self):
        self.voice_channel.pause()

    def resume(self):
        self.voice_channel.resume()

    def stop(self):
        self.callback_block = True
        # this will fire the callback, TODO: fix the bug that comes with this
        self.voice_channel.stop()

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

    def set_server_message(self, message):
        self.message_handler.set_message(message)

    async def update_server_message(self, channel):
        # get queue and status and stuff here
        # self.queue.get_queue()
        # if self.currently_playing is not None
        embedded_content = self.get_embedded_message_content()
        await self.message_handler.update_embedded_message(channel=channel, embedded_content=embedded_content)

    def get_embedded_message_content(self):
        embedded_message = Embed(title="Queue", color=0xeb4034)

        if len(self.queue.get_queue()) == 0:
            embedded_message.add_field(name="Empty", value="Add some tunes", inline=False)
            return embedded_message
        for idx, item in enumerate(self.queue.get_queue()):
            if idx == 0:
                self.get_single_item_field(embedded_message, item, name_prefix="Now Playing: ")
                embedded_message.set_image(url=item.thumbnail_link)
            else:
                self.get_single_item_field(embedded_message, item, name_prefix=str(idx) + ". ")
        return embedded_message

    def get_single_item_field(self, embed, item, name_prefix):
        embed.insert_field_at(
            index=0,
            name=name_prefix + item.title,
            value=str(item.duration_string),
            inline=False
        )

    '''
    Database specific methods
    '''

    def get_history(self, limit=10):
        self.db.get_history(limit=limit)
