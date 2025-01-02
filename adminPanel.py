import os
import tkinter as tk
from tkinter import ttk, messagebox
from dbHelper import Result, User  # Replace 'your_database_module' with the actual module name where Result is defined
import json
import pandas as pd
import bcrypt
import shutil


# admin panel
class AdminPanel(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.tab_control = ttk.Notebook(self)
        self.tab_control.pack(expand=1, fill="both")

        self.results_tab = ttk.Frame(self.tab_control)
        self.users_tab = ttk.Frame(self.tab_control)
        self.settings_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.results_tab, text="نتایج")
        self.tab_control.add(self.users_tab, text="کاربران")
        self.tab_control.add(self.settings_tab, text="تنظیمات")

        self.create_results_tab()
        self.create_users_tab()
        self.create_settings_tab()

    def create_results_tab(self):
        self.results_tree = ttk.Treeview(self.results_tab, columns=("user_id", "self_destruction_scale", "hope_scale", "mspss", "anxiety_scale", "depression_scale", "Fake_bad", "scales", "created_at"), show="headings")
        self.results_tree.heading("user_id", text="User ID")
        self.results_tree.heading("self_destruction_scale", text="Self Destruction Scale")
        self.results_tree.heading("hope_scale", text="Hope Scale")
        self.results_tree.heading("mspss", text="MSPSS")
        self.results_tree.heading("anxiety_scale", text="Anxiety Scale")
        self.results_tree.heading("depression_scale", text="Depression Scale")
        self.results_tree.heading("Fake_bad", text="Fake Bad")
        self.results_tree.heading("scales", text="Scales")
        self.results_tree.heading("created_at", text="Created At")
        self.results_tree.pack(expand=1, fill="both")

        self.results_scrollbar = ttk.Scrollbar(self.results_tab, orient="vertical", command=self.results_tree.yview)
        self.results_tree.configure(yscroll=self.results_scrollbar.set)
        self.results_scrollbar.pack(side="right", fill="y")

        self.load_results()

    def load_results(self):
        # for row in self.master.db.session.query(Result).all():
        for result, user in self.master.db.session.query(Result, User).join(User, Result.user_id == User.id).all():
            # self.results_tree.insert("", "end", values=(self.master.db.show_full_name(user), result.self_destruction_scale, result.hope_scale, result.mspss, result.anxiety_scale, result.depression_scale, result.Fake_bad, result.scales, result.created_at))
            self.results_tree.insert("", "end", values=(self.master.db.show_full_name(user), "result.self_destruction_scale", result.hope_scale, result.mspss, result.anxiety_scale, result.depression_scale, result.Fake_bad, result.scales, result.created_at))
            # print(result.User.username)

    def create_users_tab(self):
        self.users_tree = ttk.Treeview(self.users_tab, columns=("id", "username", "first_name", "last_name", "is_admin"), show="headings")
        self.users_tree.heading("id", text="ID")
        self.users_tree.heading("username", text="Username")
        self.users_tree.heading("first_name", text="First Name")
        self.users_tree.heading("last_name", text="Last Name")
        self.users_tree.heading("is_admin", text="Is Admin")
        self.users_tree.pack(expand=1, fill="both")

        self.load_users()
        self.user_form_frame = ttk.Frame(self.users_tab)
        self.user_form_frame.pack(pady=10)

        ttk.Label(self.user_form_frame, text="نام کاربری:", font=("shabnam", 12)).grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = ttk.Entry(self.user_form_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.user_form_frame, text="رمز ورود:", font=("shabnam", 12)).grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = ttk.Entry(self.user_form_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.user_form_frame, text="نام:", font=("shabnam", 12)).grid(row=2, column=0, padx=5, pady=5)
        self.first_name_entry = ttk.Entry(self.user_form_frame)
        self.first_name_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.user_form_frame, text="نام خانوادگی:", font=("shabnam", 12)).grid(row=3, column=0, padx=5, pady=5)
        self.last_name_entry = ttk.Entry(self.user_form_frame)
        self.last_name_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.user_form_frame, text="دسترسی ادمین:", font=("shabnam", 12)).grid(row=4, column=0, padx=5, pady=5)
        self.is_admin_var = tk.IntVar()
        self.is_admin_check = ttk.Checkbutton(self.user_form_frame, variable=self.is_admin_var)
        self.is_admin_check.grid(row=4, column=1, padx=5, pady=5)

        self.create_button = ttk.Button(self.user_form_frame, text="ایجاد", command=self.create_user)
        self.create_button.grid(row=5, column=0, padx=5, pady=5)

        self.update_button = ttk.Button(self.user_form_frame, text="ویرایش", command=self.update_user)
        self.update_button.grid(row=5, column=1, padx=5, pady=5)

        self.delete_button = ttk.Button(self.user_form_frame, text="حذف", command=self.delete_user)
        self.delete_button.grid(row=5, column=2, padx=5, pady=5)

        self.users_tree.bind("<ButtonRelease-1>", self.on_user_select)

    def create_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        is_admin = self.is_admin_var.get()

        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        new_user = User(username=username, password=hashed_password, first_name=first_name, last_name=last_name, is_admin=is_admin)
        self.master.db.session.add(new_user)
        self.master.db.session.commit()
        self.load_users()

    def update_user(self):
        selected_item = self.users_tree.selection()[0]
        user_id = self.users_tree.item(selected_item, "values")[0]

        user = self.master.db.session.query(User).filter_by(id=user_id).first()
        user.username = self.username_entry.get()
        user.password = bcrypt.hashpw(self.password_entry.get().encode(), bcrypt.gensalt())
        user.first_name = self.first_name_entry.get()
        user.last_name = self.last_name_entry.get()
        user.is_admin = self.is_admin_var.get()

        self.master.db.session.commit()
        self.load_users()

    def delete_user(self):
        selected_item = self.users_tree.selection()[0]
        user_id = self.users_tree.item(selected_item, "values")[0]

        user = self.master.db.session.query(User).filter_by(id=user_id).first()
        self.master.db.session.delete(user)
        self.master.db.session.commit()
        self.load_users()

    def on_user_select(self, event):
        selected_item = self.users_tree.selection()[0]
        user_id, username, first_name, last_name, is_admin = self.users_tree.item(selected_item, "values")

        self.username_entry.delete(0, tk.END)
        self.username_entry.insert(0, username)

        self.password_entry.delete(0, tk.END)

        self.first_name_entry.delete(0, tk.END) 
        self.first_name_entry.insert(0, first_name)

        self.last_name_entry.delete(0, tk.END)
        self.last_name_entry.insert(0, last_name)

        self.is_admin_var.set(is_admin)


    def load_users(self):
        # Clean tree view
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)

        for row in self.master.db.session.query(User).all():
            self.users_tree.insert("", "end", values=(row.id, row.username, row.first_name, row.last_name, row.is_admin))

    def create_settings_tab(self):
        ttk.Label(self.settings_tab, text="مد برنامه" , font=("shabnam", 16)).pack(pady=20)
        with open("settings.json", "r") as f:
            self.settings = json.load(f)

        self.settings_frame = ttk.Frame(self.settings_tab)
        self.settings_frame.pack(pady=10)


        mode = tk.StringVar() 
        mode_combo = ttk.Combobox(self.settings_frame, width = 27, textvariable = mode, font=("shabnam", 12)) 
        
        # Adding combobox drop down list 
        mode_combo['values'] = (
            "کامل",
            "سریع"
        ) 

        mode_combo.bind("<<ComboboxSelected>>", self.change_mode)

        mode_combo.pack(pady=10)
        mode_combo.current(1)
        print(mode.get())

        
        ttk.Button(self.settings_frame, text="بازگشت به ورود", command=self.back_to_login).pack(pady=20)
        ttk.Button(self.settings_frame, text="خروجی گرفتن اکسل", command=self.export_to_excel).pack(pady=10)
        ttk.Button(self.settings_frame, text="پشتیبان گیری از پایگاه داده", command=self.backup_database).pack(pady=10)

    def change_mode(self, event):
        self.settings["mode"] = event.widget.get()
        with open("settings.json", "w") as f:
            json.dump(self.settings, f)
        messagebox.showinfo("تغییر مد", "مد برنامه با موفقیت تغییر یافت")
        # if event.widget.get() == "کامل":
        #     # self.master.style.theme_use("forest-dark")
        #     print(event.widget.get())
        # # print(self.settings["mode"])

    def export_to_excel(self):
        results = self.master.db.get_results_with_username()
        data = []
        for result, user in results:
            data.append({
                "Username": user,
                "Self Destruction Scale": result.self_destruction_scale,
                "Hope Scale": result.hope_scale,
                "MSPSS": result.mspss,
                "Anxiety Scale": result.anxiety_scale,
                "Depression Scale": result.depression_scale,
                "Fake Bad": result.Fake_bad,
                "Scales": result.scales,
                "Created At": result.created_at
            })
        df = pd.DataFrame(data)
        df.to_excel("results.xlsx", index=False)
        messagebox.showinfo("خروجی گرفتن اکسل", "خروجی اکسل با موفقیت ایجاد شد")

    def backup_database(self):
        backup_path = "backup/quiz_app_backup.db"
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        shutil.copy("quiz_app.db", backup_path)
        messagebox.showinfo("پشتیبان گیری از پایگاه داده", "پشتیبان گیری با موفقیت انجام شد")


    def open_file_location(self):
        os.system("start .")

    def back_to_login(self):
        self.master.show_login_page()