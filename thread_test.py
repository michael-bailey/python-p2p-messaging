#!/usr/bin/env python3

import threading as th
from time import sleep

STOP = False

def Func():
    while not STOP:
        print("│  still going  │")
        print("├───────────────┤")
    print("│   stopping    │")
    print("├───────────────┤")

print("┌───────────────┐")
print("│starting thread│")
print("├───────────────┤")
t = th.Thread(target=Func, daemon=True).start()
print("│    waiting    │")
print("├───────────────┤")
sleep(5)
print("│    stopping   │")
print("├───────────────┤")
STOP = True
print("│waiting to join│")
print("├───────────────┤")
print("│   finished    │")
print("└───────────────┘")

sleep(5)

