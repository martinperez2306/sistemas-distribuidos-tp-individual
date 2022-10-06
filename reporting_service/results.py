from dependencies.commons.video import Video

class Results:
    def __init__(self, popular_and_funny_videos, most_viewed_day: str):
        self.popular_and_funny_videos = popular_and_funny_videos
        self.most_viewed_day = most_viewed_day

    def __str__(self):
        videos_str = str(self.popular_and_funny_videos)
        most_viewed_day_str = str(self.most_viewed_day)
        return "FILTERED_VIDEOS[{}]MOST_VIEWED_DAY[{}]"\
            .format(videos_str, most_viewed_day_str)

    def __repr__(self):
       return self.__str__()