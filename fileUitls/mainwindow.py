import tkinter as tk
from tkinter import ttk
from .page1 import Page1
from .page2 import Page2

class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("文件处理工具")
        self.geometry('600x600')

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.notebook = ttk.Notebook(container)
        self.notebook.grid(row=0, column=0, sticky='nsew')

        self.pages = {}

        for F, tab_name in [(Page1, "自动分类"), (Page2, "Page 2")]:
            page_name = F.__name__
            frame = F(parent=self.notebook, controller=self)
            self.pages[page_name] = frame
            self.notebook.add(frame, text=tab_name)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # 添加窗口关闭事件处理器

    def on_closing(self):
        """当窗口关闭时触发"""
        if "Page1" in self.pages:
            self.pages["Page1"].save_text()
        self.destroy()

    def show_frame(self, page_name):
        '''显示当前页面'''
        frame = self.pages[page_name]
        self.notebook.select(frame)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()