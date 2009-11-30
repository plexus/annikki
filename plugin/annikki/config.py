class Config:
    def __init__(self, anki_config):
        self.__dict__['anki_config'] = anki_config

    def __getattr__(self, name):
        key = "annikki.%s" % name
        if self.anki_config.has_key(key):
            return self.anki_config[key]
        else:
            return None

    def __setattr__(self, name, value):
        key = "annikki.%s" % name
        self.anki_config[key] = value

    def save(self):
        self.anki_config.save()
