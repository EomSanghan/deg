#tree_admingui.py
import tkinter as tk
from tkinter import ttk

class tree_AdminApp:
    def __init__(self, root, tree):
        self.tree = tree
        self.root = tk.Toplevel(root)
        self.root.title("Concert Hall Tree - Admin Mode")

        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.BOTH, expand=True)
        
        self.create_buttons(self.tree.root, self.button_frame)

    def create_buttons(self, node, parent_frame, level=0):
        frame = ttk.Frame(parent_frame)
        frame.pack(fill=tk.X, padx=20*level)
        button_style = 'Red.TButton' if not node.is_available else 'TButton'
        button = ttk.Button(frame, text=node.name, style=button_style, command=lambda n=node: self.toggle_availability(n))
        button.pack(fill=tk.X, padx=5, pady=5)

        for child in node.children:
            self.create_buttons(child, parent_frame, level+1)

    def toggle_availability(self, node):
        new_availability = not node.is_available
        node.set_availability(new_availability)
        self.refresh_buttons()

    def refresh_buttons(self):
        for widget in self.button_frame.winfo_children():
            widget.destroy()
        self.create_buttons(self.tree.root, self.button_frame)
