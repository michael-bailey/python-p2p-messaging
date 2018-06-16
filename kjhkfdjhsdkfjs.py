import json as js

f = open("./contacts.json","r")
contacts = js.load(f)

print(contacts)

print(contacts["1"]["name"])