from datetime import datetime
from typing import Optional
from managers.task_manager import TaskManager

class CLIHandler:
    def __init__(self):
        self.task_manager = TaskManager()
    
    def add_task(self, content: str, priority: Optional[str] = None, 
                 due_date: Optional[str] = None):
        due_datetime = None
        if due_date:
            try:
                due_datetime = datetime.fromisoformat(due_date)
            except ValueError:
                print(f"无效的日期格式: {due_date}")
                return
        
        task = self.task_manager.add_task(content, priority, due_datetime)
        print(f"任务已添加: [{task.id}] {task.content}")
    
    def list_tasks(self):
        tasks = self.task_manager.get_all_tasks()
        if not tasks:
            print("暂无任务")
            return
        
        print("\n任务列表:")
        print("-" * 60)
        for task in tasks:
            status_icon = "✓" if task.status == "completed" else "○"
            priority_str = f"[{task.priority}]" if task.priority else ""
            due_str = f"截止: {task.due_date.strftime('%Y-%m-%d')}" if task.due_date else ""
            
            print(f"{status_icon} [{task.id}] {task.content} {priority_str} {due_str}")
        print("-" * 60)
    
    def mark_done(self, task_id: int):
        if self.task_manager.update_task(task_id, status="completed"):
            print(f"任务 [{task_id}] 已标记为完成")
        else:
            print(f"未找到任务 [{task_id}]")
    
    def delete_task(self, task_id: int):
        if self.task_manager.delete_task(task_id):
            print(f"任务 [{task_id}] 已删除")
        else:
            print(f"未找到任务 [{task_id}]")
    
    def quick_add_task(self, content: str, priority: Optional[str] = None):
        """用于快速输入窗口的任务添加"""
        task = self.task_manager.add_task(content, priority)
        return task