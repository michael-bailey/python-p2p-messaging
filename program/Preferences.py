import json



class Preferences(object):
    __instance = None

    def __init__(self):
        if Preferences.__instance != None:
            self = Preferences.__instance
        else:
            try:
                self.__file = open("preferences.pref", "r+")
                self.__preferences = json.load(self.__file)
            except FileNotFoundError:
                self.__file = open("preferences.pref", "w+")
                self.__preferences = {}
            
    
    def getPreference(self, preferenceName):
        if preferenceName in self.__preferences.keys():
            return self.__preferences[preferenceName]
        else:
            return ""

    def setPreference(self, preferenceName, value):
        self.__preferences[preferenceName] = value
        self.update()

    def update(self):
        json.dump(self.__preferences, self.__file)
        self.__file.flush()
