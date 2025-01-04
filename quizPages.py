import tkinter as tk
from tkinter import ttk, messagebox
import json

class QuizPage(ttk.Frame):
    def __init__(self, master, user):
        super().__init__(master)
        self.master = master
        self.user = user
        self.current_question = 0
        self.score = {}
        self.questions_list_index = 0
        self.questions_list = ['self_destruction_scale', 'mspss', 'depression_scale',  'anxiety_scale', 'depression_scale' , 'scales', 'Fake_bad']

        ttk.Label(self, text=f"آزمون را با ارامش و با توجه به شرایط هفته گذشته جواب بدهید", font=("shabnam", 12)).pack(pady=40, anchor="center")


        self.load_questions(self.questions_list_index)
        self.create_ui()
    
    def load_questions(self, i):
        print(self.questions_list_index, i)
        self.score[self.questions_list[i]] = 0
        with open(f"questions/{self.questions_list[i]}.json", "r", encoding="utf-8") as f:
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
            tk.Radiobutton(self.radio_frame, indicator=0, text=opt['text'], variable=self.var, value=opt['score'], font=("shabnam", 12), width=30, relief="flat", selectcolor="black", activebackground="white").pack(pady=5, anchor='e')


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
        print(self.current_question)
        if self.current_question < len(self.questions):
            self.update_ui()
        else:
            self.current_question = 0
            self.questions_list_index += 1
            if self.questions_list_index < len(self.questions_list):
                self.load_questions(self.questions_list_index)
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
        self.score[self.questions_list[self.questions_list_index]] += score
        print(self.score)

    def decrease_score(self):
        score = self.var.get()
        self.score[self.questions_list[self.questions_list_index]] -= score
        print(self.score)

    def submit_quiz(self):
        self.master.db.insert_score(self.user.id, self_destruction_scale=self.score['self_destruction_scale'], hope_scale=self.score['hope_scale'], mspss=self.score['mspss'], anxiety_scale=self.score['anxiety_scale'], depression_scale=self.score['depression_scale'], Fake_bad=self.score['Fake_bad'], scales=self.score['scales'])
        self.master.show_login_page()
        # pass

    def start_check(self):
        if self.score['self_destruction_scale'] < 5:
            messagebox.showinfo("نتیجه", "پابان آزمون موفق و بهروز باشید")
            self.master.show_login_page()
        else:
            self.update_ui()
