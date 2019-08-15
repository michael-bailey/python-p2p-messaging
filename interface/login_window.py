#Date: 11/08/2019
#Time: 20:00

#Imports
import tkinter
import tkinter as tk
from tkinter import ttk

class Login_Frame(tk.Tk):
    def __init__(self, *args, **kwargs):
        super.__init__(self, *args, **kwargs)
        self.iconbitmap(self, default="")
        self.wm_title(self, "Login")
        #tk.Tk.overrideredirect(self,True)
        width = 300                                #tk.Tk.winfo_screenwidth(self)
        height = 200           
                            #tk.Tk.winfo_screenheight(self)
        res = str(width)+"x"+str(height)
        tk.Tk.geometry(self,res)

        container = tk.Frame(self)
        container.pack(side="top", fill="both",expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.large_font = ("Verdana", 12)
        self.frames = {}
        for F in (Login_Display, CreateAccount_Display):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(Login_Display)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def get_large_font(self):
        return self.large_font

class Login_Display(tk.Frame, Login_Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Login", font=self.get_large_font)
        label.grid(row=2, column=3)

        usernameL = ttk.Label(self, text="Username", font=self.get_large_font)
        usernameL.grid(row=3, column=2)
        usernameE = ttk.Entry(self)
        usernameE.grid(row=3, column=3)

        passwordL = ttk.Label(self, text="Password", font=self.get_large_font)
        passwordL.grid(row=4, column=2)
        passwordE = ttk.Entry(self, show="*")
        passwordE.grid(row=4, column=3)

        button1 = ttk.Button(self, text="Continue",
                             command=lambda: controller.login_to_account(usernameE, passwordE))
        button1.grid(row=5, column=3)
        button2 = ttk.Button(self, text="Create Account",
                             command=lambda: controller.show_frame(CreateAccount_Display))
        button2.grid(row=5, column=2)

        # Centers the login menu
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(6, weight=1)
        self.grid_columnconfigure(4, weight=1)

class CreateAccount_Display(tk.Frame, Login_Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Create Account",font=self.get_large_font)
        label.grid(row=2,column=3)

        usernameL = ttk.Label(self, text="Username", font=self.get_large_font)
        usernameL.grid(row=3, column=2)
        usernameE = ttk.Entry(self)
        usernameE.grid(row=3, column=3)

        passwordL = ttk.Label(self, text="Password", font=self.get_large_font)
        passwordL.grid(row=4, column=2)
        passwordE = ttk.Entry(self, show="*")
        passwordE.grid(row=4, column=3)

        firstnameL = ttk.Label(self, text="First Name", font=self.get_large_font)
        firstnameL.grid(row=5, column=2)
        firstnameE = ttk.Entry(self)
        firstnameE.grid(row=5, column=3)

        surnameL = ttk.Label(self, text="Surname", font=self.get_large_font)
        surnameL.grid(row=6, column=2)
        surnameE = ttk.Entry(self)
        surnameE.grid(row=6, column=3)

        button1 = ttk.Button(self, text="Confirm",
                             command=lambda: controller.send_to_database(usernameE,passwordE,firstnameE,surnameE))
        button1.grid(row=7, column=3)
        button2 = ttk.Button(self, text="Return",
                             command=lambda: controller.show_frame(Login_Display))
        button2.grid(row=7, column=2)

        #Centers the login menu
        self.grid_rowconfigure(1,weight=1)
        self.grid_columnconfigure(1,weight=1)
        self.grid_rowconfigure(12,weight=1)
        self.grid_columnconfigure(8,weight=1)


program = Login_Frame()
program.mainloop()