import inspect
from functools import wraps

from discord.errors import NotFound
from discord.ext import commands
from discord.utils import get

import config
from Server.server import Server
from database.db_interface import get_db, load_servers

client = commands.Bot(command_prefix='_')

db = get_db(config.DB_URI, config.DB_PORT)
db.connect()

servers = load_servers(db, client)


# Decorator to remove a command message after running relevant command
def remove_message_post_func_and_inject_server(func_to_run):
    @wraps(func_to_run)
    async def return_func(ctx, *args, **kwargs):
        server = get_server(ctx)
        await func_to_run(server, ctx, *args, **kwargs)
        await ctx.message.delete()
        await server.update_server_message(ctx.channel)

    # Big thanks to Sierra Macleod for this solution
    # https://medium.com/@cantsayihave/decorators-in-discord-py-e44ce3a1aae5
    return_func.__name__ = func_to_run.__name__
    sig = inspect.signature(func_to_run)
    return_func.__signature__ = sig.replace(parameters=tuple(sig.parameters.values())[1:])
    return return_func


@client.event
async def on_ready():
    print("Audio Engine online")


@client.command(pass_context=True, help="Leave the voice channel the bot is currently in")
@remove_message_post_func_and_inject_server
async def leave(server, ctx):
    await server.leave_voice_channel(ctx.guild.voice_client)


@client.command(pass_context=True, help="Use a URL for a youtube video to be added to the queue")
@remove_message_post_func_and_inject_server
async def play(server, ctx, url=None):
    voice_channel = ctx.message.author.voice.channel
    voice_clients = get(client.voice_clients, guild=ctx.guild)
    await server.play(voice_channel, voice_clients, ctx.guild, url)


@client.command(pass_context=True, help="Pause the current playback")
@remove_message_post_func_and_inject_server
async def pause(server, ctx):
    server.pause()


@client.command(pass_context=True, help="Resume if the audio is paused")
@remove_message_post_func_and_inject_server
async def resume(server, ctx):
    server.resume()


@client.command(pass_context=True, help="Stop playback, does not remove the current song from the queue")
@remove_message_post_func_and_inject_server
async def stop(server, ctx):
    server.stop()


@client.command(pass_context=True, help="Skips the current track and plays the next in the queue")
@remove_message_post_func_and_inject_server
async def skip(server, ctx):
    server.play_next()


@client.command(pass_context=True, help="Embeds the playback queue in a message")
@remove_message_post_func_and_inject_server
async def queue(server, ctx):
    await server.create_server_message(channel=ctx.channel)


@client.command(pass_context=True, help="Embeds the playback queue in a message")
@remove_message_post_func_and_inject_server
async def history(server, ctx, history_length):
    server.get_history(limit=history_length)


@client.command(pass_context=True, help="Clears all items in the playback queue")
@remove_message_post_func_and_inject_server
async def clear(server, ctx):
    server.clear_queue()


@client.command(pass_context=True, help="Remove an item at a specific index, see the index using 'queue'")
@remove_message_post_func_and_inject_server
async def remove(server, ctx, index):
    server.remove_from_queue_at_index(int(index))


@client.command(pass_context=True, help="Debug, WIP")
async def clear_messages(ctx, amount=1000):
    amount += 1
    if ctx.channel.name == "dwin_audio":
        await ctx.channel.purge(limit=amount)
    else:
        await ctx.reply("Cannot clear this channel, please create a text channel named 'dwin_audio'")


def get_server(ctx):
    if ctx.guild.id not in servers:
        servers[ctx.guild.id] = Server(
            mongo_db=db,
            server_id=ctx.guild.id,
            discord_client=client
        )
        db.add_server(ctx.guild.id)
    return servers[ctx.guild.id]


# async def send_queue_message(server, ctx):
#     old_queue_message_id = server.get_queue_message_id()
#     if old_queue_message_id is not None:
#         try:
#             old_queue_message = await ctx.channel.fetch_message(old_queue_message_id)
#             await old_queue_message.delete()
#         except NotFound:
#             print("Message not found, likely deleted by another bot or client")
#
#     embedded_message = server.get_embedded_queue_message()
#     queue_message = await ctx.channel.send(embed=embedded_message)
#     server.set_queue_message_id(queue_message.id)
#     server.set_server_message(queue_message)


client.run(config.DISCORD_TOKEN)
