# cal_userapp.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from position_list import PositionList

class cal_UserApp(tk.Toplevel):
    def __init__(self, master, main_app, timetable):
        super().__init__(master)
        self.main_app = main_app
        self.timetable = timetable
        self.create_calendar()

    def create_calendar(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.title("Calendar Schedule")
        self.geometry("800x600")

        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 14), padding=10)
        style.configure('TLabel', font=('Helvetica', 14))
        style.configure('Treeview.Heading', font=('Helvetica', 16, 'bold'))
        style.configure('Treeview', rowheight=25)

        title_label = ttk.Label(self, text="콘서트 일정표", font=('Helvetica', 22, 'bold'))
        title_label.pack(pady=20)

        days = ["일요일", "월요일", "화요일", "수요일", "목요일", "금요일", "토요일"]
        day_frame = ttk.Frame(self)
        day_frame.pack()

        for i, day in enumerate(days):
            label = ttk.Label(day_frame, text=day, borderwidth=1, relief="solid", width=15, anchor='center', font=('Helvetica', 14, 'bold'))
            label.grid(row=0, column=i)

        cal_frame = ttk.Frame(self)
        cal_frame.pack()

        for day in range(1, 32):
            btn = tk.Button(cal_frame, text=str(day), width=10, height=5)
            btn.grid(row=(day + 6) // 7, column=(day + 6) % 7, padx=5, pady=5, sticky="nsew")
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="lightgray"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="SystemButtonFace"))
            btn.config(command=lambda d=day: self.show_timetable(d))

        back_button = ttk.Button(self, text="뒤로 가기", command=self.main_app.show_user_buttons)
        back_button.pack(pady=10)

    def show_timetable(self, day):
        for widget in self.winfo_children():
            widget.destroy()

        back_btn = ttk.Button(self, text="뒤로 가기", command=self.create_calendar)
        back_btn.pack(pady=10)

        tree = ttk.Treeview(self, columns=("Time", "Name"), show="headings")
        tree.heading("Time", text="시간")
        tree.heading("Name", text="이름")

        tree_style = ttk.Style()
        tree_style.configure('Treeview', font=('Helvetica', 15))

        for node in self.timetable[day]:
            tree.insert("", "end", values=(node.time, node.name))

        tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
