import json


class Thumbnail:
    def __init__(self, filename, base64):
        self.filename = filename
        self.base64 = base64

    @staticmethod
    def from_json(json_str: str):
         parsed = json.loads(json_str)
         return Thumbnail(parsed["filename"], parsed["base64"])