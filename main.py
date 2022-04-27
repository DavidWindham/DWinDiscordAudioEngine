import config
from discord.ext import commands
from classes.server_class import ServerHandler
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


@client.command(pass_context=True)
@remove_message_post_func
async def join(ctx):
    await get_server(ctx).join_voice_channel(ctx)


@client.command(pass_context=True)
@remove_message_post_func
async def leave(ctx):
    await get_server(ctx).leave_voice_channel(ctx)


@client.command(pass_context=True)
@remove_message_post_func
async def play(ctx, url):
    await get_server(ctx).add_url(ctx, url)


def get_server(ctx):
    if ctx.guild.id not in servers:
        servers[ctx.guild.id] = ServerHandler(ctx.guild.id, client)
    return servers[ctx.guild.id]


client.run(config.DISCORD_TOKEN)
