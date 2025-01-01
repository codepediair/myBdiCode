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
            if user.is_admin:  # is_admin
                self.master.show_admin_panel()
            else:
                self.master.show_quiz_page(user)
        else:
            messagebox.showerror("خطا", "نام کاربری یا رمز عبور اشتباه است")