import json
from program import NotificationCenter


class Preferences(object):
    __instance = None
    __fileName = "preferences.pref"

    def __new__(cls):
        # does the single instance not exist
        if Preferences.__instance is None:
            Preferences.__instance = object.__new__(cls)
            tmp = Preferences.__instance
            try:
                tmp.__file = open(Preferences.__fileName, "r+")
                tmp.__preferences = json.load(tmp.__file)
                tmp.__file.close()

            except FileNotFoundError:
                tmp.__file = open(Preferences.__fileName, "w+")
                tmp.__preferences = {}
                json.dump(tmp.__preferences, tmp.__file)
                tmp.__file.close()

            except json.JSONDecodeError:
                tmp.__file.close()
                tmp.__file = open(Preferences.__fileName, "w+")
                tmp.__preferences = {}
                json.dump(tmp.__preferences, tmp.__file)
                tmp.__file.close()

            tmp.center = NotificationCenter()
            return tmp

        else:
            return Preferences.__instance

    def setPreference(self, name, value):
        self.__preferences[name] = value
        self.update()

    def getPreference(self, name):
        return self.__preferences[name]

    def update(self):
        self.__file = open(Preferences.__fileName, "w+")
        json.dump(self.__preferences, self.__file)
        self.__file.close()
