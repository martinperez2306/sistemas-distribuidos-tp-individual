class Video:
    def __init__(self, video_str: str):
        matches = video_str.strip('][').split(', ')
        self.id = matches[0].strip("''")
        self.title = matches[1].strip("''")
        self.published_at = matches[2].strip("''")
        self.channel_id = matches[3].strip("''")
        self.channel_title = matches[4].strip("''")
        self.category_id = matches[5].strip("''")
        self.trending_date = matches[6].strip("''")
        self.tags = matches[7].strip("''")
        try:
            self.view_count = int(matches[8].strip("''"))
        except ValueError:
            self.view_count = 0
        try:
            self.likes = int(matches[9].strip("''"))
        except ValueError:
            self.likes = 0
        try:
            self.dislikes = int(matches[10].strip("''"))
        except ValueError:
            self.dislikes = 0
        try:
            self.comment_count = int(matches[11].strip("''"))
        except ValueError:
            self.comment_count = 0
        self.thumbnail_link = matches[12].strip("''")
        self.comments_disabled = matches[13].strip("''")
        self.ratings_disabled = matches[14].strip("''")
        self.description = matches[15].strip("''")

    def __str__(self):
        return "ID[{}] TITLE[{}] PUBLISHED_AT[{}] CHANNEL_ID[{}] CHANNEL_TITLE[{}] CATEGORY_ID [{}] TRENDING_DATE[{}] TAGS [{}] VIEW_COUNT [{}] LIKE[{}] DISLIKES[{}] COMMENT_COUNT[{}] THUMBNAIL_LINK[{}] COMMNETS_DISABLED[{}] RATINGS_DISABLED[{}] DESCRIPTION[{}]"\
                    .format(self.id, self.title, self.published_at, self.channel_id, self.channel_title, self.category_id, \
                        self.trending_date, self.tags, str(self.view_count), str(self.likes), str(self.dislikes), str(self.comment_count), \
                            self.thumbnail_link, self.comments_disabled, self.ratings_disabled, self.description)

    def __repr__(self):
       return self.__str__()