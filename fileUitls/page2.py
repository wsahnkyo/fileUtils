# page2.py
import tkinter as tk
from tkinter import ttk

class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = ttk.Label(self, text="This is Page 2")
        label.pack(side="top", fill="x", pady=10)

        button = ttk.Button(self, text="Go to Page 1",
                            command=lambda: controller.show_frame("Page1"))
        button.pack()