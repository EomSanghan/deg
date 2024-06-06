#tree_usergui.py
import tkinter as tk
from tkinter import ttk

class tree_UserApp:
    def __init__(self, root, tree):
        self.tree = tree
        self.root = tk.Toplevel(root)
        self.root.title("Concert Hall Tree - User Mode")

        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.BOTH, expand=True)
        
        self.create_labels(self.tree.root, self.button_frame)

    def create_labels(self, node, parent_frame, level=0):
        frame = ttk.Frame(parent_frame)
        frame.pack(fill=tk.X, padx=20*level)
        label = ttk.Label(frame, text=node.name, background="red" if not node.is_available else "white")
        label.pack(fill=tk.X, padx=5, pady=5)

        for child in node.children:
            self.create_labels(child, parent_frame, level+1)
