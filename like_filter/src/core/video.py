VIDEO_FIELD_PATTERN = r','

class Video:
    def __init__(self, video_str: str):
        split = video_str.split(VIDEO_FIELD_PATTERN)
        self.id = split[0]
        self.title = split[1]
        self.published_at = split[2]
        self.channel_id = split[3]
        self.channel_title = split[4]
        self.category_id = split[5]
        self.trending_date = split[6]
        self.tags = split[7]
        self.view_count = split[8]
        self.likes = split[9]
        self.dislikes = split[10]
        self.comment_count = split[11]
        self.thumbnail_link = split[12]
        self.comments_disabled = split[13]
        self.ratings_disabled = split[14]
        self.description = split[15]

    def __str__(self):
        return "ID[{}] TITLE[{}] PUBLISHED_AT[{}] CHANNEL_ID[{}] CHANNEL_TITLE[{}] CATEGORY_ID [{}] TRENDING_DATE[{}] TAGS [{}] VIEW_COUNT [{}] \
                LIKE[{}] DISLIKES[{}] COMMENT_COUNT[{}] THUMBNAIL_LINK[{}] COMMNETS_DISABLED[{}] RATINGS_DISABLED[{}] DESCRIPTION[{}]"\
                    .format(self.id, self.title, self.published_at, self.channel_id, self.channel_title, self.category_id, \
                        self.trending_date, self.tags, self.view_count, self.likes, self.dislikes, self.comment_count, \
                            self.thumbnail_link, self.comments_disabled, self.ratings_disabled, self.description)
