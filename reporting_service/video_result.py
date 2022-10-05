class VideoResult:
    def __init__(self, id, title, category):
        self.id = id
        self.title = title
        self.category = category

    def __str__(self):
        return "ID[{}] TITLE [{}] CATEGORY[{}]"\
            .format(self.id, self.title, self.category)

    def __repr__(self):
       return self.__str__()