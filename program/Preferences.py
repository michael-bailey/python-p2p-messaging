import json
import os

class Singleton(object):
    __instance = None
    def __new__(cls, val):
        # does the single instace not exist
        if Singleton.__instance is None:
            Singleton.__instance = object.__new__(cls)
            tmp = Singleton.__instance
            try:
                with open("preferences.pref", "r+") as file:

            

        return Singleton.__instance