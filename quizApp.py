import tkinter as tk
from tkinter import ttk
from loginPage import LoginPage
from quizPages import QuizPage
from dbHelper import DBHelper
from adminPanel import AdminPanel
from registerPage import RegisterPage
from quizPage_fast import CompQuizPage
import json

class QuizApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.db = DBHelper()
        self.title("Quiz Application")
        self.geometry("800x600")
        self.current_user = None

        # Tkinter styles
        self.style = ttk.Style(self)
        self.style.tk.call("source", "./theme/forest-light.tcl")
        self.style.tk.call("source", "./theme/forest-dark.tcl")
        self.style.theme_use("forest-dark")

        self.style.configure("TLabel", font=("shabnam", 12))
        self.style.configure("TButton", font=("shabnam", 12))
        self.style.configure("TCheckbutton", font=("shabnam", 12))
        self.style.configure("TNotebook.Tab", font=("shabnam", 12))
        self.style.configure("Treeview", font=("shabnam", 12))
        self.style.configure("Treeview.Heading", font=("shabnam", 12))
        self.style.configure("TRadiobutton", font=("shabnam", 12))

        with open("settings.json", "r") as f:
            self.settings = json.load(f)

        self.show_login_page()

        # print(self.db.fetch_users())
    
    def show_login_page(self):
        for widget in self.winfo_children():
            widget.destroy()
        LoginPage(self).pack(fill=tk.BOTH, expand=True)

    def show_register_page(self):
        for widget in self.winfo_children():
            widget.destroy()
        RegisterPage(self).pack(fill="both", expand=True)

    def show_quiz_page(self, user):
        for widget in self.winfo_children():
            widget.destroy()
        if self.settings["mode"] == "کامل":
            QuizPage(self, user).pack(fill="both", expand=True)
        else:
            CompQuizPage(self, user).pack(fill="both", expand=True)

    def show_admin_panel(self):
        for widget in self.winfo_children():
            widget.destroy()
        AdminPanel(self).pack(fill="both", expand=True)