from dependencies.commons.video import Video

class ResultRepository:
    def __init__(self):
        self.filtered_videos = dict()

    def save_filtered_video(self, request_id: int, video: Video):
        if self.filtered_videos.get(request_id):
            req_videos: list = self.filtered_videos.get(request_id)
            req_videos.append(video)
            self.filtered_videos[request_id] = req_videos
        else:
            req_videos: list = list()
            req_videos.append(video)
            self.filtered_videos[request_id] = req_videos
        