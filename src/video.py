import os
from googleapiclient.discovery import build


class Video:
    """Класс для видео на ютуб-канале"""

    def __init__(self, video_id):
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""
        self._video_id = video_id

    def __str__(self):
        return self.title

    @staticmethod
    def get_service():
        """Возвращает объект для работы с API"""
        return build('youtube', 'v3', developerKey=os.getenv('YT_API_KEY'))

    def get_data(self):
        """Возвращает данные о видео в виде словаря"""
        video_response = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                          id=self._video_id
                                                          ).execute()
        return video_response

    @property
    def video_id(self):
        return self._video_id

    @property
    def title(self):
        """Возвращает название видео"""
        title = self.get_data()['items'][0]['snippet']['title']
        return title

    @property
    def url(self):
        """Возвращает ссылку на видео"""
        url = 'https://www.youtube.com/watch?v=' + self._video_id
        return url

    @property
    def view_count(self):
        """Возвращает количество просмотров на видео"""
        view_count = self.get_data()['items'][0]['statistics']['viewCount']
        return view_count

    @property
    def like_count(self):
        """Возвращает количество просмотров на видео"""
        like_count = self.get_data()['items'][0]['statistics']['likeCount']
        return like_count


class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""
        super().__init__(video_id)
        self._playlist_id = playlist_id

    def get_playlist_data(self):
        """Возвращает данные о видео в виде словаря"""
        playlists = self.get_service().playlists().list(id=self._playlist_id,
                                                        part='contentDetails,snippet',
                                                        maxResults=50,
                                                        ).execute()

        return playlists

    @property
    def playlist_id(self):
        return self._playlist_id
