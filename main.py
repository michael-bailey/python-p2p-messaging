from program.Preferences import Preferences

def main():
    a = Preferences()

    a.setPreference("colour", "blue")
    print(a.getPreference("colour"))
    b = Preferences()
    print(b.getPreference("colour"))

if __name__ == "__main__":
    main()