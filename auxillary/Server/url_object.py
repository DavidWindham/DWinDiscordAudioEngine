import datetime

from youtube_dl import YoutubeDL


class UrlObject:
    def __init__(self, url_to_scrape):
        youtube_dl_args = {'format': 'bestaudio', 'noplaylist': 'True'}
        with YoutubeDL(youtube_dl_args) as youtube_dl:
            youtube_json = youtube_dl.extract_info(url_to_scrape, download=False)

        self.video_id = youtube_json['id']
        self.url = youtube_json['formats'][0]['url']
        self.title = youtube_json['title']
        self.thumbnail_link = youtube_json['thumbnail']
        self.webpage_url = youtube_json['webpage_url']
        self.duration = youtube_json['duration']
        self.duration_string = str(datetime.timedelta(seconds=self.duration))
        print(self.title, self.url)

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
