from .audio_engine import AudioEngine


class VoiceChannel:
    def __init__(self, voice_channel=None):
        self.voice_channel = voice_channel
        self.audio_engine = AudioEngine()

    def set_voice_channel(self, voice_channel):
        self.voice_channel = voice_channel

    async def join_voice_channel(self, voice_channel):
        if self.voice_channel is not None:
            try:
                await self.voice_channel.disconnect()
            except:
                print("VoiceChannel wasn't connected")

        # for voice channel
        # ctx.message.author.voice.channel
        self.voice_channel = voice_channel
        await self.voice_channel.connect()
        # for audio engine
        # get(self.discord_client.voice_clients, guild=ctx.guild)
        # Set the audio interface in the engine
        # print(voice_channel, voice_clients)
        # self.audio_engine.set(voice_clients)

    def set_engine_interface(self, interface):
        self.audio_engine.set(interface)

    async def leave_voice_channel(self, voice_client):
        if self.voice_channel is not None:
            await voice_client.disconnect()
            self.voice_channel = None
            self.audio_engine.clear()
        #await self.voice_channel.disconnect()
        # Clear the audio interface in the engine
        #self.audio_engine.clear()

    '''
    Pure Engine funcs
    '''

    def is_engine_playing(self):
        return self.audio_engine.is_playing()

    def play_url(self, url, url_finished_callback):
        self.audio_engine.play_url(url, url_finished_callback)

    def play(self):
        self.audio_engine.play()

    def pause(self):
        self.audio_engine.pause()

    def resume(self):
        self.audio_engine.resume()

    def stop(self):
        self.audio_engine.stop()
