#inquiry_GUI.py
import tkinter as tk
from inquiry_system import InquirySystem

class InquiryUserGUI:
    def __init__(self, master, system):
        self.system = system
        self.window = tk.Toplevel(master)
        self.window.title("Customer Service - User")

        # 기본 텍스트 레이블 추가
        self.intro_label = tk.Label(self.window, text="""What kind of inquiry do you have?
1. Emergency
2. Incident/Crime Report
3. Facility Malfunction
4. Seating Issue
5. Reservation Confirmation
6. Lost Item Report
7. Others"""
)
        self.intro_label.grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(self.window, text="Category:").grid(row=1, column=0)
        self.category_entry = tk.Entry(self.window)
        self.category_entry.grid(row=1, column=1)

        tk.Label(self.window, text="Customer ID:").grid(row=2, column=0)
        self.customer_id_entry = tk.Entry(self.window)
        self.customer_id_entry.grid(row=2, column=1)

        tk.Label(self.window, text="Content:").grid(row=3, column=0)
        self.content_entry = tk.Text(self.window, height=5, width=40)
        self.content_entry.grid(row=3, column=1)

        submit_button = tk.Button(self.window, text="Submit Inquiry", command=self.write_inquiry)
        submit_button.grid(row=4, column=0, columnspan=2)

        tk.Label(self.window, text="Customer ID for answered inquiries:").grid(row=5, column=0)
        self.customer_id_answer_entry = tk.Entry(self.window)
        self.customer_id_answer_entry.grid(row=5, column=1)

        view_answered_button = tk.Button(self.window, text="View Answered Inquiries", command=self.view_answered_inquiries)
        view_answered_button.grid(row=6, column=0, columnspan=2)

        self.result_label = tk.Label(self.window, text="", wraplength=300)
        self.result_label.grid(row=7, column=0, columnspan=2)

    def write_inquiry(self):
        category = int(self.category_entry.get())
        customer_id = int(self.customer_id_entry.get())
        content = self.content_entry.get("1.0", tk.END).strip()
        self.system.write_inquiry(category, customer_id, content)
        self.result_label.config(text="Inquiry submitted.")
        self.category_entry.delete(0, tk.END)
        self.customer_id_entry.delete(0, tk.END)
        self.content_entry.delete("1.0", tk.END)

    def view_answered_inquiries(self):
        customer_id = int(self.customer_id_answer_entry.get())
        answered = self.system.view_answered_inquiries(customer_id)
        if not answered:
            self.result_label.config(text="No answered inquiries for this customer.")
        else:
            result_text = "\n".join([f"Category: {cat}, Content: {content}, Answer: {ans}" 
                                    for cat, content, ans in answered])
            self.result_label.config(text=result_text)
        self.customer_id_answer_entry.delete(0, tk.END)


class InquiryAdminGUI:
    def __init__(self, master, system):
        self.system = system
        self.window = tk.Toplevel(master)
        self.window.title("Customer Service - Admin")

        answer_label = tk.Label(self.window, text="Answer Content:")
        answer_label.grid(row=0, column=0)
        self.answer_entry = tk.Text(self.window, height=5, width=40)
        self.answer_entry.grid(row=0, column=1)

        answer_button = tk.Button(self.window, text="Answer Inquiry", command=self.answer_inquiry)
        answer_button.grid(row=1, column=0, columnspan=2)

        view_button = tk.Button(self.window, text="View Inquiries", command=self.view_inquiries)
        view_button.grid(row=2, column=0, columnspan=2)

        self.result_label = tk.Label(self.window, text="", wraplength=300)
        self.result_label.grid(row=3, column=0, columnspan=2)

    def answer_inquiry(self):
        answer_content = self.answer_entry.get("1.0", tk.END).strip()
        self.system.answer_inquiry(answer_content)
        self.answer_entry.delete("1.0", tk.END)
        self.result_label.config(text="Inquiry answered.")

    def view_inquiries(self):
        inquiries = self.system.view_inquiries()
        if not inquiries:
            self.result_label.config(text="No inquiries available.")
        else:
            result_text = "\n".join([f"Category: {cat}, Customer ID: {cust_id}, Content: {cont}" 
                                    for cat, cust_id, cont in inquiries])
            self.result_label.config(text=result_text)


class MainGUI:
    def __init__(self, root):
        self.root = root
        self.system = InquirySystem()
        self.root.title("Customer Service System")

        user_button = tk.Button(root, text="User", command=self.open_user_gui)
        user_button.pack(pady=10)

        admin_button = tk.Button(root, text="Admin", command=self.open_admin_gui)
        admin_button.pack(pady=10)

    def open_user_gui(self):
        InquiryUserGUI(self.root, self.system)

    def open_admin_gui(self):
        InquiryAdminGUI(self.root, self.system)


if __name__ == "__main__":
    root = tk.Tk()
    main_gui = MainGUI(root)
    root.mainloop()
