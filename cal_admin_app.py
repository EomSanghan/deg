# admin_app.py
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from cal_userapp import cal_UserApp

class cal_AdminApp(cal_UserApp):
    def __init__(self, master,main_app, timetable):
        super().__init__(master, main_app, timetable)
        self.main_app = main_app
        self.timetable = timetable
        self.admin_frame = None  # admin_frame을 저장할 인스턴스 변수 추가

    def create_calendar(self):
        super().create_calendar()

    def show_timetable(self, day):
        super().show_timetable(day)

        if self.admin_frame is not None:
            self.admin_frame.destroy()

        # 새로운 admin_frame 생성 및 버튼 추가
        self.admin_frame = ttk.Frame(self)
        self.admin_frame.pack(side=tk.BOTTOM, pady=10)

        insert_btn = ttk.Button(self.admin_frame, text="Insert", command=lambda: self.insert_event(day))
        insert_btn.grid(row=0, column=0, padx=5, pady=5)

        delete_btn = ttk.Button(self.admin_frame, text="Delete", command=lambda: self.delete_event(day))
        delete_btn.grid(row=0, column=1, padx=5, pady=5)

        replace_btn = ttk.Button(self.admin_frame, text="Replace", command=lambda: self.replace_event(day))
        replace_btn.grid(row=0, column=2, padx=5, pady=5)

    def insert_event(self, day):
        start_time = simpledialog.askstring("Input", "Enter start time (HH:MM):")
        position = simpledialog.askinteger("Input", "Enter position:")
        name = simpledialog.askstring("Input", "Enter event name:")

        if start_time and name and position:
            self.timetable[day].insert_at_position(position, start_time, name)
            self.show_timetable(day)  # 새로고침하여 업데이트된 타임테이블 표시

    def delete_event(self, day):
        position = simpledialog.askinteger("Input", "Enter position to delete:")

        if position:
            self.timetable[day].delete_at_position(position)
            self.show_timetable(day)  # 새로고침하여 업데이트된 타임테이블 표시

    def replace_event(self, day):
        position = simpledialog.askinteger("Input", "Enter position to replace:")
        start_time = simpledialog.askstring("Input", "Enter start time (HH:MM):")
        name = simpledialog.askstring("Input", "Enter new event name:")

        if position and start_time and name:
            self.timetable[day].replace_at_position(position, start_time, name)
            self.show_timetable(day)  # 새로고침하여 업데이트된 타임테이블 표시
