import inspect
from functools import wraps


# Decorator to inject server obj and remove a command message after running relevant command
def inject_server_and_remove_message_factory(server_handler):
    def wrapper(func_to_run):
        @wraps(func_to_run)
        async def return_func(ctx, *args, **kwargs):
            server = server_handler.get_server(ctx)
            await func_to_run(server, ctx, *args, **kwargs)
            await ctx.message.delete()
            await server.handle_server_message(ctx.channel)

        # Big thanks to Sierra Macleod for this solution
        # https://medium.com/@cantsayihave/decorators-in-discord-py-e44ce3a1aae5
        return_func.__name__ = func_to_run.__name__
        sig = inspect.signature(func_to_run)
        return_func.__signature__ = sig.replace(parameters=tuple(sig.parameters.values())[1:])
        return return_func

    return wrapper
