import tkinter as tk
import socket as s
import json as json
import xml.dom.minidom as x
class app:
    
    def __init__(self):
        window = tk.Tk()
        window.title = "IP messaging"
        window.res

        top_frame = tk.PanedWindow(orient=tk.HORIZONTAL)

        contact_pane = tk.Listbox()
        top_frame.add(contact_pane)

        rcanvas = tk.Canvas()
        top_frame.add(rcanvas)

        top_frame.pack(fill=tk.BOTH, expand=1)
        
        tk.mainloop()

app1 = app()