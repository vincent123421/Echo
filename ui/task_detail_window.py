import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
from typing import List
from models.task import Task
from managers.task_manager import TaskManager
from managers.reminder_manager import ReminderManager

class TaskDetailWindow:
    def __init__(self):
        self.task_manager = TaskManager()
        self.reminder_manager = ReminderManager()
        self.window = None
        self.task_vars = {}  # 存储任务复选框变量
    
    def show(self):
        """显示任务详情窗口"""
        if self.window:
            self.window.destroy()
        
        self.window = tk.Tk()
        self.window.title("Echo - 任务管理")
        self.window.geometry("800x600")
        self.window.configure(bg='#f0f0f0')
        
        # 置顶显示
        self.window.attributes('-topmost', True)
        self.window.focus_force()
        
        self._create_widgets()
        self._load_tasks()
        
        self.window.mainloop()
    
    def _create_widgets(self):
        """创建界面组件"""
        # 标题
        title_frame = tk.Frame(self.window, bg='#2c3e50', height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="📋 任务管理", 
                              font=('Arial', 16, 'bold'), 
                              fg='white', bg='#2c3e50')
        title_label.pack(pady=15)
        
        # 主内容区域
        main_frame = tk.Frame(self.window, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 创建滚动区域
        canvas = tk.Canvas(main_frame, bg='#f0f0f0')
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg='#f0f0f0')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 底部按钮区域
        button_frame = tk.Frame(self.window, bg='#f0f0f0')
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(button_frame, text="标记完成", command=self._mark_completed,
                 bg='#27ae60', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="删除选中", command=self._delete_selected,
                 bg='#e74c3c', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="刷新", command=self._load_tasks,
                 bg='#3498db', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="关闭", command=self._close,
                 bg='#95a5a6', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.RIGHT, padx=5)
    
    def _load_tasks(self):
        """加载并显示任务"""
        # 清空现有内容
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.task_vars.clear()
        
        # 获取任务并排序
        all_tasks = self.task_manager.get_all_tasks()
        pending_tasks = [t for t in all_tasks if t.status != "completed"]
        completed_tasks = [t for t in all_tasks if t.status == "completed"]
        
        sorted_pending = self._sort_tasks(pending_tasks)
        
        # 显示待办任务
        if sorted_pending:
            self._create_section_header("🔥 待办任务", "#e74c3c")
            for task in sorted_pending:
                self._create_task_item(task, False)
        
        # 显示已完成任务
        if completed_tasks:
            self._create_section_header("✅ 已完成任务", "#27ae60")
            for task in completed_tasks[-10:]:  # 只显示最近10个已完成任务
                self._create_task_item(task, True)
        
        if not all_tasks:
            no_task_label = tk.Label(self.scrollable_frame, text="暂无任务", 
                                   font=('Arial', 14), fg='#7f8c8d', bg='#f0f0f0')
            no_task_label.pack(pady=50)
    
    def _create_section_header(self, title: str, color: str):
        """创建分组标题"""
        header_frame = tk.Frame(self.scrollable_frame, bg=color, height=40)
        header_frame.pack(fill=tk.X, pady=(20, 0))
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(header_frame, text=title, 
                               font=('Arial', 12, 'bold'), 
                               fg='white', bg=color)
        header_label.pack(pady=8)
    
    def _create_task_item(self, task: Task, is_completed: bool):
        """创建单个任务项"""
        # 任务容器
        task_frame = tk.Frame(self.scrollable_frame, bg='white', relief=tk.RAISED, bd=1)
        task_frame.pack(fill=tk.X, pady=2, padx=5)
        
        # 复选框和任务内容
        content_frame = tk.Frame(task_frame, bg='white')
        content_frame.pack(fill=tk.X, padx=15, pady=10)
        
        # 复选框
        var = tk.BooleanVar()
        self.task_vars[task.id] = var
        checkbox = tk.Checkbutton(content_frame, variable=var, bg='white')
        checkbox.pack(side=tk.LEFT)
        
        # 任务信息区域
        info_frame = tk.Frame(content_frame, bg='white')
        info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        # 任务标题行
        title_frame = tk.Frame(info_frame, bg='white')
        title_frame.pack(fill=tk.X)
        
        # 任务内容
        content_text = task.content
        if is_completed:
            content_text = f"✓ {content_text}"
        
        content_label = tk.Label(title_frame, text=content_text, 
                               font=('Arial', 11, 'bold' if not is_completed else 'normal'),
                               fg='#2c3e50' if not is_completed else '#7f8c8d',
                               bg='white', anchor='w')
        content_label.pack(side=tk.LEFT)
        
        # 优先级标签
        if task.priority:
            priority_colors = {"高": "#e74c3c", "中": "#f39c12", "低": "#3498db"}
            priority_label = tk.Label(title_frame, text=f"[{task.priority}]",
                                    font=('Arial', 9, 'bold'),
                                    fg=priority_colors.get(task.priority, "#95a5a6"),
                                    bg='white')
            priority_label.pack(side=tk.RIGHT)
        
        # 时间信息行
        time_info = []
        
        if task.due_date:
            now = datetime.now()
            if task.due_date < now and not is_completed:
                due_text = f"截止: {task.due_date.strftime('%Y-%m-%d %H:%M')} ⚠️已过期"
                due_color = "#e74c3c"
            elif task.due_date.date() == date.today():
                due_text = f"截止: 今天 {task.due_date.strftime('%H:%M')}"
                due_color = "#f39c12"
            else:
                due_text = f"截止: {task.due_date.strftime('%Y-%m-%d %H:%M')}"
                due_color = "#7f8c8d"
            time_info.append((due_text, due_color))
        
        if task.reminder_time and not is_completed:
            if task.reminder_time.date() == date.today():
                remind_text = f"提醒: 今天 {task.reminder_time.strftime('%H:%M')}"
            else:
                remind_text = f"提醒: {task.reminder_time.strftime('%Y-%m-%d %H:%M')}"
            time_info.append((remind_text, "#3498db"))
        
        if time_info:
            time_frame = tk.Frame(info_frame, bg='white')
            time_frame.pack(fill=tk.X, pady=(5, 0))
            
            for i, (text, color) in enumerate(time_info):
                if i > 0:
                    sep_label = tk.Label(time_frame, text=" | ", 
                                       font=('Arial', 9), fg='#bdc3c7', bg='white')
                    sep_label.pack(side=tk.LEFT)
                
                time_label = tk.Label(time_frame, text=text,
                                    font=('Arial', 9), fg=color, bg='white')
                time_label.pack(side=tk.LEFT)
    
    def _sort_tasks(self, tasks: List[Task]) -> List[Task]:
        """按优先级和截止时间排序任务"""
        priority_order = {"高": 3, "中": 2, "低": 1, None: 0}
        
        def sort_key(task):
            priority_weight = priority_order.get(task.priority, 0)
            
            time_weight = 0
            if task.due_date:
                now = datetime.now()
                time_diff = (task.due_date - now).total_seconds()
                if time_diff < 0:  # 过期
                    time_weight = 1000
                elif time_diff < 86400:  # 24小时内
                    time_weight = 100
                else:
                    time_weight = max(0, 50 - time_diff / 86400)
            
            return -(priority_weight * 10 + time_weight)
        
        return sorted(tasks, key=sort_key)
    
    def _mark_completed(self):
        """标记选中任务为完成"""
        selected_ids = [task_id for task_id, var in self.task_vars.items() if var.get()]
        if not selected_ids:
            messagebox.showwarning("提示", "请选择要标记完成的任务")
            return
        
        for task_id in selected_ids:
            self.task_manager.update_task(task_id, status="completed")
            self.reminder_manager.remove_reminder(task_id)
        
        messagebox.showinfo("成功", f"已标记 {len(selected_ids)} 个任务为完成")
        self._load_tasks()
    
    def _delete_selected(self):
        """删除选中任务"""
        selected_ids = [task_id for task_id, var in self.task_vars.items() if var.get()]
        if not selected_ids:
            messagebox.showwarning("提示", "请选择要删除的任务")
            return
        
        if messagebox.askyesno("确认", f"确定要删除 {len(selected_ids)} 个任务吗？"):
            for task_id in selected_ids:
                self.task_manager.delete_task(task_id)
                self.reminder_manager.remove_reminder(task_id)
            
            messagebox.showinfo("成功", f"已删除 {len(selected_ids)} 个任务")
            self._load_tasks()
    
    def _close(self):
        """关闭窗口"""
        if self.window:
            self.window.destroy()
            self.window = None