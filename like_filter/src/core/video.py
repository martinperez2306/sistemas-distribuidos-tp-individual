import re

VIDEO_FIELD_PATTERN = r'\"(.+?)\"'

class Video:
    def __init__(self, video_str: str):
        matches = re.findall(VIDEO_FIELD_PATTERN, video_str)
        self.id = matches[0]
        self.title = matches[1]
        self.published_at = matches[2]
        self.channel_id = matches[3]
        self.channel_title = matches[4]
        self.category_id = matches[5]
        self.trending_date = matches[6]
        self.tags = matches[7]
        self.view_count = matches[8]
        self.likes = matches[9]
        self.dislikes = matches[10]
        self.comment_count = matches[11]
        self.thumbnail_link = matches[12]
        self.comments_disabled = matches[13]
        self.ratings_disabled = matches[14]
        self.description = matches[15]

    def __str__(self):
        return "ID[{}] TITLE[{}] PUBLISHED_AT[{}] CHANNEL_ID[{}] CHANNEL_TITLE[{}] CATEGORY_ID [{}] TRENDING_DATE[{}] TAGS [{}] VIEW_COUNT [{}] \
                LIKE[{}] DISLIKES[{}] COMMENT_COUNT[{}] THUMBNAIL_LINK[{}] COMMNETS_DISABLED[{}] RATINGS_DISABLED[{}] DESCRIPTION[{}]"\
                    .format(self.id, self.title, self.published_at, self.channel_id, self.channel_title, self.category_id, \
                        self.trending_date, self.tags, self.view_count, self.likes, self.dislikes, self.comment_count, \
                            self.thumbnail_link, self.comments_disabled, self.ratings_disabled, self.description)
