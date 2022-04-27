from discord.utils import get
from ..audio_class import AudioEngine


class ServerCore:
    def __init__(self, discord_client):
        self.discord_client = discord_client
        self.audio_engine = AudioEngine()
        self.voice_channel = None

    async def join_voice_channel(self, ctx):
        if self.voice_channel is not None:
            await self.leave_voice_channel(ctx)

        self.voice_channel = ctx.message.author.voice.channel
        await self.voice_channel.connect()

    async def leave_voice_channel(self, ctx):
        if self.voice_channel is not None:
            await ctx.guild.voice_client.disconnect()
            self.voice_channel = None
            self.clear_audio_engine_interface()

    def set_audio_engine_interface(self, ctx):
        self.audio_engine.set_audio_interface(
            get(self.discord_client.voice_clients, guild=ctx.guild)
        )

    def clear_audio_engine_interface(self):
        self.audio_engine.clear_audio_interface()
