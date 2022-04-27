import config
from discord import Embed
from discord.ext import commands
from auxillary.server_class import ServerHandler
from functools import wraps

client = commands.Bot(command_prefix='_')

servers = {}


# Decorator to remove a command message after running relevant command
def remove_message_post_func(func_to_run):
    @wraps(func_to_run)
    async def return_async_func(*args):
        await func_to_run(*args)
        await args[0].message.delete()

    return return_async_func


@client.event
async def on_ready():
    print("Audio Engine online")


@client.command(pass_context=True, help="Leave the voice channel the bot is currently in")
@remove_message_post_func
async def leave(ctx):
    await get_server(ctx).leave_voice_channel(ctx)


@client.command(pass_context=True, help="Use a URL for a youtube video to be added to the queue")
@remove_message_post_func
async def play(ctx, url=None):
    if url is None:
        if get_server(ctx).is_queue_empty():
            await ctx.channel.send("Play queue is empty")
            return
        await get_server(ctx).play_next_url_in_queue()
    else:
        await get_server(ctx).add_url(ctx, url)


@client.command(pass_context=True, help="Pause the current playback")
@remove_message_post_func
async def pause(ctx):
    get_server(ctx).pause()


@client.command(pass_context=True, help="Resume if the audio is paused")
@remove_message_post_func
async def resume(ctx):
    get_server(ctx).resume()


@client.command(pass_context=True, help="Stop playback, does not remove the current song from the queue")
@remove_message_post_func
async def stop(ctx):
    get_server(ctx).stop()


@client.command(pass_context=True, help="Skips the current track and plays the next in the queue")
@remove_message_post_func
async def skip(ctx):
    get_server(ctx).skip()


@client.command(pass_context=True, help="Embeds the playback queue in a message")
@remove_message_post_func
async def queue(ctx):
    embedded_message = get_server(ctx).get_embedded_queue_message()
    await ctx.channel.send(embed=embedded_message)


@client.command(pass_context=True, help="Clears all items in the playback queue")
@remove_message_post_func
async def clear(ctx):
    get_server(ctx).clear_queue()


@client.command(pass_context=True, help="Remove an item at a specific index, see the index using 'queue'")
@remove_message_post_func
async def remove(ctx, index):
    get_server(ctx).remove_from_queue_at_index(int(index))


@client.command(pass_context=True, help="Debug, WIP")
async def clear_messages(ctx, amount=1000):
    amount += 1
    if ctx.channel.name == "dwin_audio":
        await ctx.channel.purge(limit=amount)
    else:
        await ctx.reply("Cannot clear this channel, please create a text channel named 'dwin_audio'")


def get_server(ctx):
    if ctx.guild.id not in servers:
        servers[ctx.guild.id] = ServerHandler(ctx.guild.id, client)
    return servers[ctx.guild.id]


client.run(config.DISCORD_TOKEN)
