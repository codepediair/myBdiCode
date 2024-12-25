from tkinter import ttk, messagebox

# Register Page
class RegisterPage(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        ttk.Label(self, text="ثبت نام", font=("shabnam", 24)).pack(pady=20)

        ttk.Label(self, text="نام کاربری", font=("shabnam", 18)).pack(pady=5)
        self.username_entry = ttk.Entry(self, font=("shabnam", 14))
        self.username_entry.pack(pady=5)

        ttk.Label(self, text="رمز عبور", font=("shabnam", 18)).pack(pady=5)
        self.password_entry = ttk.Entry(self, show="*", font=("shabnam", 14))
        self.password_entry.pack(pady=5)

        ttk.Label(self, text="تکرار رمز عبور", font=("shabnam", 18)).pack(pady=5)
        self.confirm_password_entry = ttk.Entry(self, show="*", font=("shabnam", 14))
        self.confirm_password_entry.pack(pady=5)

        ttk.Button(self, text="ثبت نام", command=self.register).pack(pady=10)
        ttk.Button(self, text="بازگشت به ورود", command=self.master.show_login_page).pack()

    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()

        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "Please enter all fields.")
            return

        if password!= confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        if self.master.db.register_user(username, password):
            messagebox.showinfo("Success", "Registration successful!")
            self.master.show_login_page()
        else:
            messagebox.showerror("Error", "Username already exists.")