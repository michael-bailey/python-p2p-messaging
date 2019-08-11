import json

class Preferences(object):

    def __init__(self):
        if not hasattr(self, 'preferences'):
            with open("preferences.json", "r+") as file:
                self.preferences = json.load(file)
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance
    
    def getPreference(self, preferenceName):
        if preferenceName in self.preferences.keys():
            return self.preferences[preferenceName]
        else:
            return ""

    def setPreference(self, preferenceName, value):
        self.preferences[preferenceName] = value
        self.update()

    def update(self):
        with open("preferences.json", "w") as file:
            json.dump(self, file)
