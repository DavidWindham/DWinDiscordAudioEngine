from discord.ext import commands
from discord.utils import get

import config
from database.db_interface import get_db
from decorators import inject_server_and_remove_message_factory
from servers_handler import ServersHandler

client = commands.Bot(command_prefix='_')
db = get_db(config.DB_URI, config.DB_PORT)
db.connect()
servers_handler = ServersHandler(db=db, client=client)


@client.event
async def on_ready():
    print("Audio Engine online")


@client.command(pass_context=True, help="Leave the voice channel the bot is currently in")
@inject_server_and_remove_message_factory(servers_handler)
async def leave(server, ctx):
    await server.leave_voice_channel(ctx.guild.voice_client)


@client.command(pass_context=True, help="Use a URL for a youtube video to be added to the queue")
@inject_server_and_remove_message_factory(servers_handler)
async def play(server, ctx, url=None):
    voice_channel = ctx.message.author.voice.channel
    voice_clients = get(client.voice_clients, guild=ctx.guild)
    await server.play(voice_channel, voice_clients, ctx.guild, url)


@client.command(pass_context=True, help="Pause the current playback")
@inject_server_and_remove_message_factory(servers_handler)
async def pause(server, ctx):
    server.pause()


@client.command(pass_context=True, help="Resume if the audio is paused")
@inject_server_and_remove_message_factory(servers_handler)
async def resume(server, ctx):
    server.resume()


@client.command(pass_context=True, help="Stop playback, does not remove the current song from the queue")
@inject_server_and_remove_message_factory(servers_handler)
async def stop(server, ctx):
    server.stop()


@client.command(pass_context=True, help="Skips the current track and plays the next in the queue")
@inject_server_and_remove_message_factory(servers_handler)
async def skip(server, ctx):
    server.skip()


@client.command(pass_context=True, help="Embeds the playback queue in a message")
@inject_server_and_remove_message_factory(servers_handler)
async def queue(server, ctx):
    await server.handle_server_message(channel=ctx.channel)


@client.command(pass_context=True, help="Embeds the playback queue in a message")
@inject_server_and_remove_message_factory(servers_handler)
async def history(server, ctx, history_length):
    server.get_history(limit=history_length)


@client.command(pass_context=True, help="Clears all items in the playback queue")
@inject_server_and_remove_message_factory(servers_handler)
async def clear(server, ctx):
    server.clear_queue()


@client.command(pass_context=True, help="Remove an item at a specific index, see the index using 'queue'")
@inject_server_and_remove_message_factory(servers_handler)
async def remove(server, ctx, index):
    server.remove_from_queue_at_index(int(index))


@client.command(pass_context=True, help="Debug, WIP")
async def clear_messages(ctx, amount=1000):
    amount += 1
    if ctx.channel.name == "dwin_audio":
        await ctx.channel.purge(limit=amount)
    else:
        await ctx.reply("Cannot clear this channel, please create a text channel named 'dwin_audio'")


client.run(config.DISCORD_TOKEN)
