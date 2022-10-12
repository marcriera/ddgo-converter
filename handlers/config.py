import json

class ConfigHandler:
    def __init__(self, path):
        super().__init__()

        self._path = path
        self._config = []
        self.load()

    def load(self):
        try:
            with open(self._path, 'r') as f:
                self._config = json.load(f)
        except Exception:
            pass

    def save(self):
        with open(self._path, 'w') as f:
            json.dump(self._config, f, indent = 4)

    def get_config(self, hash):
        return None

    def set_config(self, hash, data):
        return
    
