import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class LoginPage(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.resizable(False, False)

        # Create main frame
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True)

        # Create a canvas to display the background image
        self.canvas = tk.Canvas(main_frame)
        self.canvas.pack(fill="both", expand=True)

        # Load the image
        self.image = Image.open("./img/login_pic.jpg")
        self.photo = ImageTk.PhotoImage(self.image)

        # Display the image on the canvas
        self.canvas.create_image(0, 0, image=self.photo, anchor="nw")

        # Bind the <Configure> event to the canvas to resize the image
        self.canvas.bind("<Configure>", self.resize_image)

        # Create right frame for the login form
        right_frame = ttk.Frame(self.canvas)
        self.canvas.create_window(400, 0, anchor="nw", window=right_frame, width=400, height=600)

        ttk.Label(right_frame, text="ورود", font=("shabnam", 24)).pack(pady=40, anchor="center")

        ttk.Label(right_frame, text="نام کاربری", font=("shabnam", 18)).pack(pady=5)
        self.username_entry = ttk.Entry(right_frame, font=("shabnam", 12), width=20)
        self.username_entry.pack(pady=5)

        ttk.Label(right_frame, text="رمزورود", font=("shabnam", 18)).pack(pady=5)
        self.password_entry = ttk.Entry(right_frame, show="*", font=("shabnam", 12))
        self.password_entry.pack(pady=5)

        ttk.Button(right_frame, text="ورود", command=self.login).pack(pady=10)
        ttk.Button(right_frame, text="ثبت نام", command=self.master.show_register_page).pack()

        # Bind Enter key to login
        self.master.bind('<Return>', self.login)

    def resize_image(self, event):
        # Resize the image to fit the canvas
        new_width = event.width
        new_height = event.height
        resized_image = self.image.resize((new_width, new_height))
        self.photo = ImageTk.PhotoImage(resized_image)
        self.canvas.create_image(0, 0, image=self.photo, anchor="nw")

    def login(self, event=None):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("خطا", "لطفا هر دو مقدار را وارد کنید")
            return

        user = self.master.db.validate_user(username, password)
        if user:
            self.master.current_user = user
            if self.master.db.is_profile_empty(user.id):
                self.show_profile_form(user)
            elif user.is_admin:  # is_admin
                self.master.show_admin_panel()
            else:
                self.master.show_quiz_page(user)
        else:
            messagebox.showerror("خطا", "نام کاربری یا رمز عبور اشتباه است")

    def show_profile_form(self, user):
        profile_form = tk.Toplevel(self)
        profile_form.title("فرم پروفایل")
        profile_form.geometry("400x300")

        ttk.Label(profile_form, text="لطفا پروفایل خود را تکمیل کنید", font=("shabnam", 18)).pack(pady=20)

        ttk.Label(profile_form, text="سن", font=("shabnam", 12)).pack(pady=5)
        age_entry = ttk.Entry(profile_form, font=("shabnam", 12), width=30)
        age_entry.pack(pady=5)

        ttk.Label(profile_form, text="تحصیلات", font=("shabnam", 12)).pack(pady=5)
        education_entry = ttk.Entry(profile_form, font=("shabnam", 12), width=30)
        education_entry.pack(pady=5)

        ttk.Label(profile_form, text="وضعیت تاهل", font=("shabnam", 12)).pack(pady=5)
        marige_entry = ttk.Entry(profile_form, font=("shabnam", 12), width=30)
        marige_entry.pack(pady=5)

        ttk.Label(profile_form, text="وضعیت خدمت سربازی", font=("shabnam", 12)).pack(pady=5)
        military_entry = ttk.Entry(profile_form, font=("shabnam", 12), width=30)
        military_entry.pack(pady=5)

        ttk.Label(profile_form, text="تعداد فرزند", font=("shabnam", 12)).pack(pady=5)
        childe_entry = ttk.Entry(profile_form, font=("shabnam", 12), width=30)
        childe_entry.pack(pady=5)

        ttk.Label(profile_form, text="وضعیت شغلی", font=("shabnam", 12)).pack(pady=5)
        job_entry = ttk.Entry(profile_form, font=("shabnam", 12), width=30)
        job_entry.pack(pady=5)

        ttk.Label(profile_form, text="تعداد نفرات خانواده", font=("shabnam", 12)).pack(pady=5)
        family_entry = ttk.Entry(profile_form, font=("shabnam", 12), width=30)
        family_entry.pack(pady=5)

        ttk.Label(profile_form, text="خانه یا ماشین دارید؟", font=("shabnam", 12)).pack(pady=5)
        prop_entry = ttk.Entry(profile_form, font=("shabnam", 12), width=30)
        prop_entry.pack(pady=5)

        ttk.Label(profile_form, text="دین", font=("shabnam", 12)).pack(pady=5)
        religion_entry = ttk.Entry(profile_form, font=("shabnam", 12), width=30)
        religion_entry.pack(pady=5)

        ttk.Label(profile_form, text="سابقه روانپزشکی", font=("shabnam", 12)).pack(pady=5)
        psycho_entry = ttk.Entry(profile_form, font=("shabnam", 12), width=30)
        psycho_entry.pack(pady=5)

        ttk.Label(profile_form, text="سابقه خودکشی", font=("shabnam", 12)).pack(pady=5)
        suicide_entry = ttk.Entry(profile_form, font=("shabnam", 12), width=30)
        suicide_entry.pack(pady=5)

        ttk.Label(profile_form, text="سابقه بیماری", font=("shabnam", 12)).pack(pady=5)
        sickness_entry = ttk.Entry(profile_form, font=("shabnam", 12), width=30)
        sickness_entry.pack(pady=5)

        ttk.Label(profile_form, text="سابقه بیمه", font=("shabnam", 12)).pack(pady=5)
        insurance_entry = ttk.Entry(profile_form, font=("shabnam", 12), width=30)
        insurance_entry.pack(pady=5)


        def save_profile():
            age = age_entry.get().strip()
            education = education_entry.get().strip()
            marige = marige_entry.get().strip()
            military = military_entry.get().strip()
            childe = childe_entry.get().strip()
            job = job_entry.get().strip()
            family = family_entry.get().strip()
            prop = prop_entry.get().strip()
            religion = religion_entry.get().strip()
            psycho = psycho_entry.get().strip()
            suicide = suicide_entry.get().strip()
            sickness = sickness_entry.get().strip()
            insurance = insurance_entry.get().strip()
            self.master.db.create_profile(user.id, age, education, marige, military, childe, job, family, prop, religion, psycho, suicide, sickness, insurance)
            profile_form.destroy()
            if user.is_admin:
                self.master.show_admin_panel()
            else:
                self.master.show_quiz_page(user)

        ttk.Button(profile_form, text="ذخیره پروفایل", command=save_profile).pack(pady=20)