class Video:
    def __init__(self, id, title, published_at, channel_id, channel_title, category_id, trending_date, tags, view_count, likes, dislikes, comment_count, thumbnail_link, comments_disabled, ratings_disabled, description):
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

    def __str__(self):
        return "ID[{}] TITLE[{}] PUBLISHED_AT[{}] CHANNEL_ID[{}] CHANNEL_TITLE[{}] CATEGORY_ID [{}] TRENDING_DATE[{}] TAGS [{}] VIEW_COUNT [{}] LIKE[{}] DISLIKES[{}] COMMENT_COUNT[{}] THUMBNAIL_LINK[{}] COMMNETS_DISABLED[{}] RATINGS_DISABLED[{}] DESCRIPTION[{}]"\
                    .format(self.id, self.title, self.published_at, self.channel_id, self.channel_title, self.category_id, \
                        self.trending_date, self.tags, str(self.view_count), str(self.likes), str(self.dislikes), str(self.comment_count), \
                            self.thumbnail_link, self.comments_disabled, self.ratings_disabled, self.description)

    def __repr__(self):
       return self.__str__()