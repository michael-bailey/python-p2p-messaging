import tkinter as tk

class entryBox(tk.Frame):

    value = ""

    def __init__(self, master, command):
        tk.Frame.__init__(self, master)

        self.enterButton = tk.Button(self, text="enter", command=self.update)
        self.entryBox = tk.Entry(self)

        self.enterButton.pack(side="right")
        self.entryBox.pack(side="left")

    def update(self):
        self.value = self.entryBox.get()


app = tk.Tk()

a = entryBox(app)
a.pack()
l = tk.Label(app)
tk.mainloop()
