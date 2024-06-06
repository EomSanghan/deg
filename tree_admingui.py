import tkinter as tk
from tkinter import ttk
from tkinter.simpledialog import askstring
from tkinter import messagebox

class tree_AdminApp:
    def __init__(self, root, tree):
        self.tree = tree
        self.root = tk.Toplevel(root)
        self.root.title("Concert Hall Tree - Admin Mode")

        self.style = ttk.Style()
        self.style.configure('Unavailable.TButton', background='red')

        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.BOTH, expand=True)
        
        self.create_buttons(self.tree.root, self.button_frame)

        # 이름 변경 버튼 추가
        self.rename_button = ttk.Button(self.root, text="Change Node Name", command=self.change_node_name)
        self.rename_button.pack(side=tk.BOTTOM, pady=10)

    def create_buttons(self, node, parent_frame, level=0):
        frame = ttk.Frame(parent_frame)
        frame.pack(fill=tk.X, padx=20*level)

        button_style = 'Unavailable.TButton' if not node.is_available else 'TButton'
        button = ttk.Button(frame, text=node.name, style=button_style, command=lambda n=node: self.toggle_availability(n))
        button.pack(fill=tk.X, expand=True, padx=5, pady=5)

        for child in node.children:
            self.create_buttons(child, parent_frame, level+1)

    def change_node_name(self):
        old_name = askstring("Change Node Name", "Enter the old node name:")
        if not old_name:
            return

        node = self.find_node(self.tree.root, old_name)
        if not node:
            messagebox.showerror("Error", "Node not found. Make sure the name is correct.")
            return
        
        new_name = askstring("Change Node Name", "Enter the new name for the node:")
        if new_name:
            node.name = new_name
            self.refresh_buttons()
        
    def find_node(self, node, name):
        if node.name == name:
            return node
        for child in node.children:
            result = self.find_node(child, name)
            if result:
                return result
        return None

    def toggle_availability(self, node):
        new_state = not node.is_available
        self.set_availability_recursive(node, new_state)
        self.refresh_buttons()

    def set_availability_recursive(self, node, state):
        node.is_available = state
        for child in node.children:
            self.set_availability_recursive(child, state)

    def refresh_buttons(self):
        for widget in self.button_frame.winfo_children():
            widget.destroy()
        self.create_buttons(self.tree.root, self.button_frame)
