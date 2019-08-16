from program.NotificationCenter import NotificationCenter
from program.Preferences import Preferences


class hj(object):
    def test_func(self, notification_name, info=None):
        print(self)
        print(notification_name)
        print(info)

def main():
    a = Preferences()
    print(a)
    a.setPreference("colour", "blue")
    print(a.getPreference("colour"))
    b = Preferences()
    print(b)
    print(b.getPreference("colour"))

    bob = hj()
    alice = hj()
    c = NotificationCenter()
    print(c)

    c.addObserver(bob, bob.test_func, "call")
    c.postNotification("call", "boop")

    d = NotificationCenter()
    print(d)
    d.postNotification("call", "boop")

if __name__ == "__main__":
    main()