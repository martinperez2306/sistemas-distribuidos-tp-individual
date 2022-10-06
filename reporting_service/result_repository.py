from dependencies.commons.utils import unique
from dependencies.commons.video import Video

class ResultRepository:
    def __init__(self):
        self.popular_and_funny_videos = dict()
        self.trending_videos = dict()
        self.most_viewed_day = None

    def save_popular_and_funny_video(self, request_id: int, video: Video):
        if self.popular_and_funny_videos.get(str(request_id)):
            req_videos: list = self.popular_and_funny_videos.get(request_id)
            req_videos.append(video)
            self.popular_and_funny_videos[str(request_id)] = req_videos
        else:
            req_videos: list = list()
            req_videos.append(video)
            self.popular_and_funny_videos[str(request_id)] = req_videos

    def get_filtered_videos(self, request_id: int) -> 'list[Video]':
        return self.__get_unique_result_videos(self.popular_and_funny_videos.get(str(request_id)))

    def __get_unique_result_videos(self, result_videos: 'list[Video]') -> 'list[Video]':
        return unique(result_videos)

    def save_trending_video(self, request_id: int, video: Video):
        if self.trending_videos.get(str(request_id)):
            req_videos: list = self.trending_videos.get(request_id)
            req_videos.append(video)
            self.trending_videos[str(request_id)] = req_videos
        else:
            req_videos: list = list()
            req_videos.append(video)
            self.trending_videos[str(request_id)] = req_videos

    def get_trending_videos(self, request_id: int) -> 'list[Video]':
        return self.trending_videos.get(str(request_id))

    def save_most_viewed_day(self, most_viewed_day):
        self.most_viewed_day = most_viewed_day

    def get_most_viewed_day(self) -> str:
        return self.most_viewed_day
        