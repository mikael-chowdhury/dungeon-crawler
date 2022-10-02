import os


class ResourceLocation(str):
    def __init__(self, path):
        self.path = path

    def __str__(self) -> str:
        return os.path.join(os.path.dirname(__file__), "..", self.path)