from discord import FFmpegPCMAudio


def get_ffmpeg_object(url):
    ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                      'options': '-vn'}

    return FFmpegPCMAudio(url, **ffmpeg_options)


class AudioEngine:
    def __init__(self):
        self.audio_interface = None

    def is_engine_playing(self):
        return self.audio_interface.is_playing()

    def is_audio_interface_set(self):
        if self.audio_interface is not None:
            return True

        return False

    def set_audio_interface(self, passed_audio_interface):
        self.audio_interface = passed_audio_interface

    def clear_audio_interface(self):
        self.audio_interface = None

    def play_item(self, url, song_finished_callback):
        self.audio_interface.play(get_ffmpeg_object(url), after=lambda e: song_finished_callback)

        self.audio_interface.is_playing()

    def pause(self):
        self.audio_interface.pause()

    def resume(self):
        self.audio_interface.resume()

    def stop(self):
        self.audio_interface.stop()
