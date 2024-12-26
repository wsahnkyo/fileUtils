import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import json
import shutil


class Page1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.style = ttk.Style(self)
        self.style.configure('TButton', padding=6, relief="flat", background="#ccc")
        self.style.configure('TLabel', padding=6)

        # 创建并放置文本编辑框和标签
        self.text_label = ttk.Label(self, text="Enter keywords (one per line):")
        self.text_label.pack(pady=(20, 5))

        self.text_edit = tk.Text(self, wrap='word', height=10, width=50)
        self.text_edit.pack(pady=10)

        # 添加文件类型限制的输入框
        self.types_label = ttk.Label(self, text="Enter allowed file types (comma separated, e.g., .mp4,.jpg):")
        self.types_label.pack(pady=(10, 5))

        self.types_edit = tk.Entry(self, width=50 )
        self.types_edit.pack(pady=5)
        self.load_types()

        # 加载上次保存的文本
        self.load_text()

        # 文件夹选择按钮和标签
        self.folder_frame = ttk.Frame(self)
        self.folder_frame.pack(pady=10, fill=tk.X)

        self.folder_label = ttk.Label(self.folder_frame, text="Source Folder: Not Selected")
        self.folder_label.pack(side=tk.LEFT, padx=(0, 10))

        folder_select_button = ttk.Button(self.folder_frame, text="Select",
                                          command=self.select_folder)
        folder_select_button.pack(side=tk.RIGHT)

        # 输出文件夹选择按钮和标签
        self.output_folder_frame = ttk.Frame(self)
        self.output_folder_frame.pack(pady=10, fill=tk.X)

        self.output_folder_label = ttk.Label(self.output_folder_frame, text="Output Folder: Not Selected")
        self.output_folder_label.pack(side=tk.LEFT, padx=(0, 10))

        output_folder_select_button = ttk.Button(self.output_folder_frame, text="Select",
                                                 command=self.select_output_folder)
        output_folder_select_button.pack(side=tk.RIGHT)

        # 分类按钮
        classify_button = ttk.Button(self, text="Classify Files",
                                     command=self.classify_files)
        classify_button.pack(pady=20)

        self.selected_folder = None
        self.output_folder = None

    def load_text(self):
        """加载之前保存的文本"""
        try:
            with open('saved_text.json', 'r') as f:
                data = json.load(f)
                self.text_edit.insert('1.0', data.get('text', ''))
        except FileNotFoundError:
            pass

    def save_text(self):
        """保存当前文本到文件"""
        text_content = self.text_edit.get("1.0", tk.END).strip()
        with open('saved_text.json', 'w') as f:
            json.dump({'text': text_content}, f)

    def load_types(self):
        """加载之前保存的文件类型"""
        try:
            with open('saved_types.json', 'r') as f:
                data = json.load(f)
                self.types_edit.insert(0, data.get('types', ''))
        except FileNotFoundError:
            pass

    def save_types(self):
        """保存当前文件类型到文件"""
        types_content = self.types_edit.get().strip()
        with open('saved_types.json', 'w') as f:
            json.dump({'types': types_content}, f)

    def select_folder(self):
        """打开源文件夹选择对话框"""
        self.selected_folder = filedialog.askdirectory()
        if self.selected_folder:
            self.update_label(self.folder_label, "Source Folder:", self.selected_folder)

    def select_output_folder(self):
        """打开输出文件夹选择对话框"""
        self.output_folder = filedialog.askdirectory()
        if self.output_folder:
            self.update_label(self.output_folder_label, "Output Folder:", self.output_folder)

    def update_label(self, label, prefix, path):
        """更新标签以显示选择的全路径，并设置鼠标悬停提示"""
        max_length = 50  # 显示的最大字符数
        display_path = path if len(path) <= max_length else f"...{path[-max_length:]}"
        label.config(text=f"{prefix} {display_path}")
        label.bind("<Enter>", lambda e, p=path: self.show_tooltip(e, p))
        label.bind("<Leave>", lambda e: self.hide_tooltip(e))

    def show_tooltip(self, event, path):
        """显示完整路径作为工具提示"""
        tooltip = tk.Toplevel(event.widget)
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{event.x_root + 20}+{event.y_root + 10}")
        label = tk.Label(tooltip, text=path, background="#ffffe0", relief='solid', borderwidth=1)
        label.pack()
        self.tooltip = tooltip  # Keep a reference to avoid garbage collection

    def hide_tooltip(self, event):
        """隐藏工具提示"""
        if hasattr(self, 'tooltip'):
            self.tooltip.destroy()
            delattr(self, 'tooltip')

    def classify_files(self):
        """根据文本编辑框中的关键字对文件进行分类"""
        if not self.selected_folder:
            messagebox.showwarning("Warning", "Please select a source folder first.")
            return

        if not self.output_folder:
            messagebox.showwarning("Warning", "Please select an output folder first.")
            return

        # 获取允许的文件类型列表
        allowed_types = [ext.strip().lower() for ext in self.types_edit.get().split(',')]
        if not any(allowed_types):
            messagebox.showwarning("Warning", "Please enter at least one allowed file type.")
            return

        keywords = self.text_edit.get("1.0", tk.END).strip().splitlines()
        for keyword in keywords:
            keyword = keyword.strip()
            if keyword:
                keyword_dir = os.path.join(self.output_folder, keyword)
                os.makedirs(keyword_dir, exist_ok=True)

        for root, dirs, files in os.walk(self.selected_folder):
            for file in files:
                # 检查文件扩展名是否在允许的列表中
                _, ext = os.path.splitext(file)
                if ext.lower() in allowed_types:
                    for keyword in keywords:
                        keyword = keyword.strip()
                        if keyword and keyword.lower() in file.lower():
                            dest_dir = os.path.join(self.output_folder, keyword)
                            shutil.move(os.path.join(root, file), dest_dir)
                            break

        self.save_text()
        self.save_types()
        messagebox.showinfo("Classification Complete", "Files have been classified.")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("File Classifier")

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    page1 = Page1(mainframe, root)
    page1.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

    root.mainloop()