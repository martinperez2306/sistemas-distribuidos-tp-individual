import json


class VideoInput:
    def __init__(self, id, title, published_at, channel_id, channel_title, category_id, trending_date, tags, view_count, likes, dislikes, comment_count, thumbnail_link, comments_disabled, ratings_disabled, description, country):
        self.id = id
        self.title = title
        self.published_at = published_at
        self.channel_id = channel_id
        self.channel_title = channel_title
        self.category_id = category_id
        self.trending_date = trending_date
        self.tags = tags
        self.view_count = view_count
        self.likes = likes
        self.dislikes = dislikes
        self.comment_count = comment_count
        self.thumbnail_link = thumbnail_link
        self.comments_disabled = comments_disabled
        self.ratings_disabled = ratings_disabled
        self.description = description
        self.country = country

    @staticmethod
    def from_json(json_str: str):
        parsed = json.loads(json_str)
        video = VideoInput(parsed["id"], parsed["title"], parsed["published_at"], parsed["channel_id"], parsed["channel_title"], parsed["category_id"], 
                    parsed["trending_date"], parsed["tags"], parsed["view_count"], parsed["likes"], parsed["dislikes"], parsed["comment_count"], 
                    parsed["thumbnail_link"], parsed["comments_disabled"], parsed["ratings_disabled"], parsed["description"], parsed["country"])
        return video

    def __str__(self):
        return "ID[{}] TITLE[{}] PUBLISHED_AT[{}] CHANNEL_ID[{}] CHANNEL_TITLE[{}] CATEGORY_ID [{}] TRENDING_DATE[{}] TAGS [{}] VIEW_COUNT [{}] LIKE[{}] DISLIKES[{}] COMMENT_COUNT[{}] THUMBNAIL_LINK[{}] COMMNETS_DISABLED[{}] RATINGS_DISABLED[{}] DESCRIPTION[{}] COUNTRY[{}]"\
                    .format(self.id, self.title, self.published_at, self.channel_id, self.channel_title, self.category_id, \
                        self.trending_date, self.tags, str(self.view_count), str(self.likes), str(self.dislikes), str(self.comment_count), \
                            self.thumbnail_link, self.comments_disabled, self.ratings_disabled, self.description, self.country)

    def __repr__(self):
       return self.__str__()

    def copy(self):
        return VideoInput(self.id, self.title, self.published_at, self.channel_id, self.channel_title, self.category_id, self.trending_date,
                        self.tags, self.view_count, self.likes, self.dislikes, self.comment_count, self.thumbnail_link, self.comments_disabled,
                        self.ratings_disabled, self.description, self.country)