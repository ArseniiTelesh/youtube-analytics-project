import json
import os
from googleapiclient.discovery import build

YT_API_KEY = 'AIzaSyD8HPnvS0S1GG_Fxs0djyR8zFkWcg4ZR9M'


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""

        api_key: str = os.getenv('YT_API_KEY')
        # создать специальный объект для работы с API
        youtube = build('youtube', 'v3', developerKey=api_key)

        def printj(dict_to_print: dict) -> None:
            """Выводит словарь в json-подобном удобном формате с отступами"""
            print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))

        channel_id = 'UC-OVMPlMA3-YCIeg4z5z23A'  # MoscowPython
        channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        printj(channel)

    @staticmethod
    def get_service():
        """Возвращает объект для работы с API"""
        return build('youtube', 'v3', developerKey=os.getenv('YT_API_KEY'))

    def get_data(self, channel_id='UC-OVMPlMA3-YCIeg4z5z23A'):
        channel = self.get_service().channels().list(id=channel_id, part='snippet,statistics').execute()
        return channel

    @property
    def title(self):
        """Возвращает название канала"""
        title = self.get_data()['items'][0]['snippet']['title']
        return title

    @property
    def description(self):
        """Возвращает описание канала"""
        description = self.get_data()['items'][0]['snippet']['description']
        return description

    @property
    def url(self):
        """Возвращает ссылку на канал"""
        url = 'https://www.youtube.com/channel/' + self.channel_id
        return url

    @property
    def subscriber_count(self):
        """Возвращает количество подписчиков канала"""
        subscriber_count = self.get_data()['items'][0]['statistics']['subscriberCount']
        return subscriber_count

    @property
    def video_count(self):
        """Возвращает общее количество видео на канале"""
        video_count = self.get_data()['items'][0]['statistics']['videoCount']
        return video_count

    @property
    def view_count(self):
        """Возвращает общее количество просмотров видео на канале"""
        view_count = self.get_data()['items'][0]['statistics']['viewCount']
        return view_count

    def to_json(self, name_of_file):
        data = {
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count
                }

        with open(name_of_file, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
