# not my code credit to https://pypi.org/user/ti250/


class NotificationCenter(object):
    __instance = None

    def __new__(cls):
        if NotificationCenter.__instance == None:
            NotificationCenter.__instance = object.__new__(cls)
            tmp = NotificationCenter.__instance

            # instantiation
            tmp.notifications = {}
            tmp.observerKeys = {}

            return tmp

        else:
            return NotificationCenter.__instance

    def addObserver(self, observer, method, notificationName, observedObject=None):

        if notificationName not in self.notifications.keys():
            self.notifications[notificationName] = {}

        notificationDict = self.notifications[notificationName]

        if observedObject not in notificationDict.keys():
            notificationDict[observedObject] = {}

        notificationDict[observedObject][observer] = method

        if observer not in self.observerKeys.keys():
            self.observerKeys[observer] = []

        self.observerKeys[observer].append((notificationName, observedObject))

    def removeObserver(self, observer, notificationName=None, observedObject=None):
        try:
            observerKeys = self.observerKeys.pop(observer)
        except KeyError:
            return
        for observerKey in observerKeys:
            if notificationName and observerKey[0] != notificationName:
                continue
            if observedObject and observerKey[1] != observedObject:
                continue
            try:
                self.notifications[observerKey[0]][observerKey[1]].pop(observer)
            except KeyError:
                return
            if len(self.notifications[observerKey[0]][observerKey[1]]) == 0:
                self.notifications[observerKey[0]].pop(observerKey[1])
                if len(self.notifications[observerKey[0]]) == 0:
                    self.notifications.pop(observerKey[0])

    def postNotification(self, notificationName, notifyingObject, userInfo=None):
        try:
            notificationDict = self.notifications[notificationName]
        except KeyError:
            return
        for key in (notifyingObject, None):
            try:
                methodsDict = notificationDict[key]
            except KeyError:
                continue
            for observer in methodsDict:
                if not userInfo:
                    methodsDict[observer](notifyingObject)
                else:
                    methodsDict[observer](notifyingObject, userInfo)
