from dependencies.commons.video import Video

class Results:
    def __init__(self, filtered_videos, most_viewed_day: str):
        self.filtered_videos = filtered_videos
        self.most_viewed_day = most_viewed_day

    def __str__(self):
        videos_str = str(self.filtered_videos)
        most_viewed_day_str = str(self.most_viewed_day)
        return "FILTERED_VIDEOS[{}]MOST_VIEWED_DAY[{}]"\
            .format(videos_str, most_viewed_day_str)

    def __repr__(self):
       return self.__str__()