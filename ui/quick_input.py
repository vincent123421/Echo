import tkinter as tk
from tkinter import ttk
from ui.cli_handler import CLIHandler
from managers.reminder_manager import ReminderManager

class QuickInputWindow:
    def __init__(self):
        self.cli_handler = CLIHandler()
        self.reminder_manager = ReminderManager()
        self.reminder_manager.start()
        self.window = None
    
    def show(self):
        if self.window:
            self.window.destroy()
        
        self.window = tk.Tk()
        self.window.title("快速添加任务")
        self.window.geometry("400x200")
        self.window.resizable(False, False)
        
        # 置顶显示
        self.window.attributes('-topmost', True)
        self.window.focus_force()
        
        # 任务内容输入
        tk.Label(self.window, text="任务内容:").pack(pady=5)
        self.content_entry = tk.Entry(self.window, width=50)
        self.content_entry.pack(pady=5)
        self.content_entry.focus()
        
        # 优先级选择
        priority_frame = tk.Frame(self.window)
        priority_frame.pack(pady=5)
        tk.Label(priority_frame, text="优先级:").pack(side=tk.LEFT)
        
        self.priority_var = tk.StringVar()
        priority_combo = ttk.Combobox(priority_frame, textvariable=self.priority_var,
                                     values=["", "高", "中", "低"], width=10)
        priority_combo.pack(side=tk.LEFT, padx=5)
        
        # 提醒时间输入
        tk.Label(self.window, text="提醒时间 (可选):").pack(pady=5)
        self.reminder_entry = tk.Entry(self.window, width=50)
        self.reminder_entry.pack(pady=5)
        
        # 提示文本
        hint_label = tk.Label(self.window, text="格式: 2024-12-25 18:00 或 18:00 或 12-25 18:00", 
                             font=('Arial', 8), fg='gray')
        hint_label.pack()
        
        # 按钮
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="添加", command=self.add_task).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="取消", command=self.close).pack(side=tk.LEFT, padx=5)
        
        # 绑定回车键
        self.window.bind('<Return>', lambda e: self.add_task())
        self.window.bind('<Escape>', lambda e: self.close())
        
        self.window.mainloop()
    
    def add_task(self):
        content = self.content_entry.get().strip()
        if not content:
            return
        
        priority = self.priority_var.get() if self.priority_var.get() else None
        reminder_time = self.reminder_entry.get().strip() if self.reminder_entry.get().strip() else None
        
        task = self.cli_handler.add_task(content, priority, None, reminder_time)
        if task:  # 只有成功添加才关闭窗口
            if task.reminder_time:
                self.reminder_manager.add_reminder(task)
            self.close()
    
    def close(self):
        if self.window:
            self.window.destroy()
            self.window = None