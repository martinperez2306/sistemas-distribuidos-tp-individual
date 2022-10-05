from dependencies.commons.utils import unique
from dependencies.commons.video import Video

class ResultRepository:
    def __init__(self):
        self.filtered_videos = dict()
        self.most_viewed_day = None

    def save_filtered_video(self, request_id: int, video: Video):
        if self.filtered_videos.get(str(request_id)):
            req_videos: list = self.filtered_videos.get(request_id)
            req_videos.append(video)
            self.filtered_videos[str(request_id)] = req_videos
        else:
            req_videos: list = list()
            req_videos.append(video)
            self.filtered_videos[str(request_id)] = req_videos

    def get_filtered_videos(self, request_id: int) -> 'list[Video]':
        return self.__get_unique_result_videos(self.filtered_videos.get(str(request_id)))

    def __get_unique_result_videos(self, result_videos: 'list[Video]') -> 'list[Video]':
        return unique(result_videos)

    def save_most_viewed_day(self, most_viewed_day):
        self.most_viewed_day = most_viewed_day

    def get_most_viewed_day(self) -> str:
        return self.most_viewed_day
        