import tkinter as tk
from tkinter import ttk, messagebox
import json

class CompQuizPage(ttk.Frame):
    def __init__(self, master, user):
        super().__init__(master)
        self.master = master
        self.user = user
        self.current_question = 0
        self.score = 0
        self.questions_list_index = 0

        ttk.Label(self, text=f"آزمون را با ارامش و با توجه به شرایط هفته گذشته جواب بدهید", font=("shabnam", 12)).pack(pady=40, anchor="center")

        self.load_questions()
        self.create_ui()
    
    def load_questions(self):
        with open("questions/fast_quiz.json", "r", encoding="utf-8") as f:
            self.questions = json.load(f)

    def create_ui(self):
        self.create_question_label()
        self.create_radio_buttons()
        self.create_buttons()

    
    def create_question_label(self):
        self.question_label = ttk.Label(self, text=self.questions[self.current_question]["question"], font=("shabnam", 14))
        self.question_label.pack(pady=10)

    def create_radio_buttons(self):
        self.var = tk.IntVar()
        self.radio_frame = ttk.Frame(self)
        self.radio_frame.pack(pady=10, anchor='center')
        for opt in (self.questions[self.current_question]["answers"]): 
            ttk.Radiobutton(self.radio_frame, text=opt['text'], variable=self.var, value=opt['score']).pack(pady=5, anchor='w')


    def create_buttons(self):
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(pady=10)

        self.back_button = ttk.Button(self.button_frame, text="قبلی", command=self.back_to_previous_question)
        self.back_button.pack(side="left", padx=10)

        self.next_button = ttk.Button(self.button_frame, text="بعدی", command=self.next_question)
        self.next_button.pack(side="left", padx=10)


    def next_question(self):
        self.update_score()
        self.current_question += 1
        if self.current_question < len(self.questions):
            if self.current_question == 5 and self.var.get() < 2:
                self.start_check()
            else:
                self.update_ui()
        else:
            self.submit_quiz()

    def back_to_previous_question(self):
        if self.current_question > 0:
            self.decrease_score()
            self.current_question -= 1
            self.update_ui()


    def update_ui(self):
        self.question_label.config(text=self.questions[self.current_question]["question"])
        self.radio_frame.destroy()
        self.button_frame.destroy()
        self.create_radio_buttons()
        self.create_buttons()

    def update_score(self):
        score = self.var.get()
        self.score += score

    def decrease_score(self):
        score = self.var.get()
        self.score -= score
        print(self.score)

    def submit_quiz(self):
        self.master.db.insert_score(self.user.id, compactmode=self.score)
        self.master.show_login_page()

    def start_check(self):
        if self.score < 5:
            messagebox.showinfo("نتیجه", "پابان آزمون موفق و بهروز باشید")
            self.master.show_login_page()
        else:
            self.update_ui()