import tkinter as tk
from tkinter import ttk
# 문재민
from inquiry_GUI import InquiryUserGUI, InquiryAdminGUI
from inquiry_system import InquirySystem
# 안기섭
from ticketing_admin import ConcertReservationSystemGUI
# 엄상한
from position_list import PositionList
from cal_userapp import cal_UserApp
from cal_admin_app import cal_AdminApp
# 방보현
from facility_guide import Tree
from tree_usergui import tree_UserApp
from tree_admingui import tree_AdminApp
# 김대겸
from ticketing_user import ticketing_user_gui  

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MainApp")
        self.geometry("400x400")  # 창의 크기를 키움
        
        self.system = InquirySystem()
        self.timetable = {day: PositionList() for day in range(1, 32)}
        self.tree = self.create_tree()
        
        self.user_buttons = [("Calendar", cal_UserApp), ("Inquiry", InquiryUserGUI), ("Facility", tree_UserApp), ("Ticketing", ticketing_user_gui)]
        self.admin_buttons = [("ConcertReservation", ConcertReservationSystemGUI), ("InquiryAdmin", InquiryAdminGUI), ("Calendar", cal_AdminApp), ("Facility", tree_AdminApp)]
        
        self.create_main_buttons()


    def create_main_buttons(self):
        user_button = ttk.Button(self, text="User", command=self.show_user_buttons)
        user_button.pack(pady=10)

        admin_button = ttk.Button(self, text="Admin", command=self.show_admin_buttons)
        admin_button.pack(pady=10)

    def show_user_buttons(self):
        self.clear_frame()
        for text, app_class in self.user_buttons:
            button = ttk.Button(self, text=text, command=lambda app_class=app_class: self.open_app(app_class, "user"))
            button.pack(pady=5)

    def show_admin_buttons(self):
        self.clear_frame()
        for text, app_class in self.admin_buttons:
            button = ttk.Button(self, text=text, command=lambda app_class=app_class: self.open_app(app_class, "admin"))
            button.pack(pady=5)

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.create_main_buttons()

    def open_app(self, app_class, user_type):
        if user_type == "user" and app_class == InquiryUserGUI:
            app_class(self, self.system)
        elif user_type == "admin" and app_class == InquiryAdminGUI:
            app_class(self, self.system)
        else:
            app_class(self)

            

    def open_app(self, app_class, user_type):
        if user_type == "user" and app_class == InquiryUserGUI:
            app_class(self, self.system)
        elif user_type == "admin" and app_class == InquiryAdminGUI:
            app_class(self, self.system)
        elif user_type == "user" and app_class == cal_UserApp:
            app_class(self, self, self.timetable)
        elif user_type == "admin" and app_class == cal_AdminApp:
            app_class(self, self, self.timetable)
        elif user_type == "user" and app_class == tree_UserApp:
            app_class(self, self.tree)
        elif user_type == "admin" and app_class == tree_AdminApp:
            app_class(self, self.tree)
        elif user_type == "user" and app_class == ticketing_user_gui:
            app_class(self)
            self.show_ticketing_gui()
        else:
            app_class(self)

    def create_tree(self):
        tree = Tree("Concert Hall")
        tree.add_node("Concert Hall", "Entrance")
        tree.add_node("Concert Hall", "Seats")
        tree.add_node("Concert Hall", "Restroom")
        tree.add_node("Concert Hall", "Snack Bar")

        tree.add_node("Entrance", "Entrance 1")
        tree.add_node("Entrance", "Entrance 2")

        tree.add_node("Seats", "VIP Seats")
        tree.add_node("Seats", "Regular Seats")

        tree.add_node("Restroom", "Men's Restroom")
        tree.add_node("Restroom", "Women's Restroom")

        tree.add_node("Snack Bar", "Beverage Bar")
        tree.add_node("Snack Bar", "Food Bar")
        tree.add_node("Snack Bar", "Souvenir Shop")
        return tree
    

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
