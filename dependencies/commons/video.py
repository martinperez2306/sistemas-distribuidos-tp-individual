from dependencies.commons.video_input import VideoInput


class Video:
    def __init__(self, id, title, category_id, trending_date, tags, view_count, likes, thumbnail_link, country):
        self.id = id
        self.title = title
        self.category_id = category_id
        self.trending_date = trending_date
        self.tags = tags
        self.view_count = view_count
        self.likes = likes
        self.thumbnail_link = thumbnail_link
        self.country = country

    def __str__(self):
        return "ID[{}] TITLE[{}] CATEGORY_ID [{}] TRENDING_DATE[{}] TAGS [{}] VIEW_COUNT [{}] LIKE[{}] THUMBNAIL_LINK[{}] COUNTRY[{}]"\
                    .format(self.id, self.title, self.category_id, 
                            self.trending_date, self.tags, str(self.view_count), str(self.likes), 
                            self.thumbnail_link, self.country)

    def __repr__(self):
       return self.__str__()

    def copy(self):
        return Video(self.id, self.title, self.category_id, self.trending_date,
                        self.tags, self.view_count, self.likes, self.thumbnail_link, 
                        self.country)

    @staticmethod
    def from_input(video_input: VideoInput):
        video = Video(video_input.id, video_input.title, video_input.category_id, video_input.trending_date,
                        video_input.tags, video_input.view_count, video_input.likes, video_input.thumbnail_link,
                        video_input.country)
        return video