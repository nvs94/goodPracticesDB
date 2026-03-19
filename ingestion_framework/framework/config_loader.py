import json

class ConfigLoader:
    """
    Loads pipeline configuration from JSON.
    """

    @staticmethod
    def load(path):
        with open(path, "r") as f:
            return json.load(f)
