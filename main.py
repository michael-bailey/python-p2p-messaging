from program.Preferences import Preferences
from program.NotificationCenter import NotificationCenter

def test_func(sender, notification_name, info):
    print(sender)
    print(notification_name)
    print(info)

def main():
    a = Preferences()

    a.setPreference("colour", "blue")
    print(a.getPreference("colour"))
    b = Preferences()
    print(b.getPreference("colour"))

    c = NotificationCenter()

    c.add_observer(test_func, "call")
    c.post_notification(object(), "call", [1,2,3,4,5,6])

    d = NotificationCenter()
    d.post_notification(object(), "call", [1,2,3,4,5,6])


if __name__ == "__main__":
    main()