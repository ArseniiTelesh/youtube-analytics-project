import os
from googleapiclient.discovery import build
import isodate
import datetime


class PlayList:

    def __init__(self, playlist_id):
        """Экземпляр инициализируется id плейлиста. Дальше все данные будут подтягиваться по API."""
        self.playlist_id = playlist_id

    @staticmethod
    def get_service():
        """Возвращает объект для работы с API"""
        return build('youtube', 'v3', developerKey=os.getenv('YT_API_KEY'))

    def get_data(self):
        """Возвращает данные о видео в виде словаря"""
        playlist_videos = self.get_service().playlistItems().list(playlistId=self.playlist_id,
                                                                  part='contentDetails, snippet',
                                                                  maxResults=50,
                                                                  ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        return video_ids

    @property
    def total_duration(self):
        video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                          id=','.join(self.get_data())
                                                          ).execute()
        total_duration = datetime.timedelta(hours=0)
        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration

    def show_best_video(self):
        videos_stats = self.get_service().videos().list(part='statistics,contentDetails,topicDetails',
                                                        id=self.get_data()
                                                        ).execute()

        max_likes = 0
        information = None
        for video in videos_stats['items']:
            if int(video['statistics']['likeCount']) >= max_likes:
                max_likes = int(video['statistics']['likeCount'])
                information = video

        return f"https://youtu.be/{information['id']}"

    @property
    def title(self):
        playlist_videos = self.get_service().playlistItems().list(playlistId=self.playlist_id,
                                                                  part='snippet',
                                                                  maxResults=50,
                                                                  ).execute()

        playlists = self.get_service().playlists().list(channelId=playlist_videos['items'][0]['snippet']['channelId'],
                                                        part='contentDetails,snippet',
                                                        maxResults=50,
                                                        ).execute()
        right_name = None
        for playlist in playlists['items']:
            if playlist['snippet']['title'] == 'Moscow Python Meetup №81':
                right_name = playlist['snippet']['title']

        return right_name

    @property
    def url(self):
        return f'https://www.youtube.com/playlist?list={self.playlist_id}'
