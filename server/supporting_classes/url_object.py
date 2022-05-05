import datetime

from youtube_dl import YoutubeDL


def get_url_object_s(url):
    youtube_dl_args = {'format': 'bestaudio', 'playlistend': 30}
    with YoutubeDL(youtube_dl_args) as youtube_dl:
        youtube_json = youtube_dl.extract_info(url, download=False)

    if '_type' not in youtube_json:
        return [
            UrlObject(youtube_json)
        ]

    # likely playlist but maybe check also
    if youtube_json['_type'] == "playlist":
        return_list = []
        for single_youtube_video in youtube_json['entries']:
            return_list.append(
                UrlObject(single_youtube_video)
            )
        return return_list

    return None


class UrlObject:
    def __init__(self, youtube_json):
        self.video_id = youtube_json['id']
        self.url = youtube_json['formats'][0]['url']
        self.title = youtube_json['title']
        self.thumbnail_link = youtube_json['thumbnail']
        self.webpage_url = youtube_json['webpage_url']
        self.duration = youtube_json['duration']
        self.duration_string = str(datetime.timedelta(seconds=self.duration))

    def get_id(self):
        return self.video_id

    def get_url(self):
        return self.url

    def get_title(self):
        return self.title

    def get_thumbnail_link(self):
        return self.thumbnail_link

    def get_webpage_url(self):
        return self.webpage_url

    def get_dict(self):
        return {
            "video_id": self.video_id,
            "url": self.url,
            "title": self.title,
            "thumbnail_link": self.thumbnail_link,
            "webpage_url": self.webpage_url,
            "duration": self.duration,
            "duration_string": self.duration_string
        }
