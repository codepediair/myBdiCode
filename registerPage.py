import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# Register Page
class RegisterPage(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.resizable(False, False)

        # Create main frame
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True)

        # Create a Canvas to display the background image
        self.canvas = tk.Canvas(main_frame)
        self.canvas.pack(fill="both", expand=True)

        # Load the image
        self.image = Image.open("./img/login_pic.jpg")
        self.photo = ImageTk.PhotoImage(self.image)

        # Display the image on the canvas
        self.canvas.create_image(0, 0, image=self.photo, anchor="nw")

        # Bind the <Configure> event to the canvas to resize the image
        self.canvas.bind("<Configure>", self.resize_image)


        # Create right frame for the Singing form
        right_frame = ttk.Frame(self.canvas)
        self.canvas.create_window(400, 0, anchor="nw", window=right_frame, width=400, height=600)

        ttk.Label(right_frame, text="ثبت نام", font=("shabnam", 24)).pack(pady=20)

        ttk.Label(right_frame, text="نام کاربری", font=("shabnam", 18)).pack(pady=5)
        self.username_entry = ttk.Entry(right_frame, font=("shabnam", 14))
        self.username_entry.pack(pady=5)

        ttk.Label(right_frame, text="رمز عبور", font=("shabnam", 18)).pack(pady=5)
        self.password_entry = ttk.Entry(right_frame, show="*", font=("shabnam", 14))
        self.password_entry.pack(pady=5)

        ttk.Label(right_frame, text="تکرار رمز عبور", font=("shabnam", 18)).pack(pady=5)
        self.confirm_password_entry = ttk.Entry(right_frame, show="*", font=("shabnam", 14))
        self.confirm_password_entry.pack(pady=5)

        ttk.Button(right_frame, text="ثبت نام", command=self.register, width=15).pack(pady=10)
        ttk.Button(right_frame, text="بازگشت به ورود", command=self.master.show_login_page, width=15).pack()

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

    def resize_image(self, event):
        # Resize the image to fit the canvas
        new_width = event.width
        new_height = event.height
        resized_image = self.image.resize((new_width, new_height))
        self.photo = ImageTk.PhotoImage(resized_image)
        self.canvas.create_image(0, 0, image=self.photo, anchor="nw")