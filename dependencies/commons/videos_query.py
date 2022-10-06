import json


class VideosQuery:
    def __init__(self, categories, total_countries):
        self.categories = categories
        self.total_countries = total_countries

    @staticmethod
    def from_json(json_str: str):
         parsed = json.loads(json_str)
         return VideosQuery(parsed["categories"], parsed["total_countries"])