from tkinter import ttk, messagebox

# Login Page
class LoginPage(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        ttk.Label(self, text="ورود", font=("shabnam", 24)).pack(pady=40, anchor="center")

        ttk.Label(self, text="نام کاربری" , font=("shabnam", 18)).pack(pady=5)
        self.username_entry = ttk.Entry(self, font=("shabnam", 12), width=20)
        self.username_entry.pack(pady=5)

        ttk.Label(self, text="رمزورود", font=("shabnam", 18)).pack(pady=5)
        self.password_entry = ttk.Entry(self, show="*", font=("shabnam", 12))
        self.password_entry.pack(pady=5)

        ttk.Button(self, text="ورود" ,command=self.login).pack(pady=10)
        ttk.Button(self, text="ثبت نام", command=self.master.show_register_page).pack()



    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("خطا", "لطفا هر دو مقدار را وارد کنید")
            return

        user = self.master.db.validate_user(username, password)
        if user:
            self.master.current_user = user
            if user.is_admin:  # is_admin
                self.master.show_admin_panel()
                # self.master.show_quiz_page(user)
            else:
                self.master.show_quiz_page(user)
                # self.master.show_user_profile_page(user)
                # print("user login")
        else:
            messagebox.showerror("خطا", "نام کاربری یا رمز عبور اشتباه است")