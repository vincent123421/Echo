from datetime import datetime, date
from typing import Optional, List
from managers.task_manager import TaskManager
from utils.datetime_parser import parse_datetime
from models.task import Task

class CLIHandler:
    def __init__(self):
        self.task_manager = TaskManager()
    
    def add_task(self, content: str, priority: Optional[str] = None, 
                 due_date: Optional[str] = None, reminder_time: Optional[str] = None):
        due_datetime = None
        reminder_datetime = None
        
        if due_date:
            due_datetime = parse_datetime(due_date)
            if not due_datetime:
                print(f"无效的截止日期格式: {due_date}")
                return
        
        if reminder_time:
            reminder_datetime = parse_datetime(reminder_time)
            if not reminder_datetime:
                print(f"无效的提醒时间格式: {reminder_time}")
                return
        
        task = self.task_manager.add_task(content, priority, due_datetime, reminder_datetime)
        print(f"任务已添加: [{task.id}] {task.content}")
        
        return task
    
    def list_tasks(self):
        tasks = self.task_manager.get_all_tasks()
        if not tasks:
            print("暂无任务")
            return
        
        # 按状态分组
        pending_tasks = [t for t in tasks if t.status != "completed"]
        completed_tasks = [t for t in tasks if t.status == "completed"]
        
        # 对待办任务排序
        sorted_pending = self._sort_tasks_by_priority_and_deadline(pending_tasks)
        
        print("\n任务列表:")
        print("=" * 80)
        
        if sorted_pending:
            print("○ 待办任务:")
            print("-" * 80)
            for task in sorted_pending:
                self._print_task(task)
        
        if completed_tasks:
            print("\n✓ 已完成任务:")
            print("-" * 80)
            for task in completed_tasks[-5:]:  # 只显示最近5个已完成任务
                self._print_task(task)
        
        print("=" * 80)
    
    def _print_task(self, task: Task):
        """打印单个任务信息"""
        status_icon = "✓" if task.status == "completed" else "○"
        
        # 优先级显示
        priority_str = f"[{task.priority}]" if task.priority else "[无]"
        
        # 截止日期显示
        due_str = ""
        if task.due_date:
            now = datetime.now()
            if task.due_date < now:
                due_str = f"截止: {task.due_date.strftime('%Y-%m-%d %H:%M')} ⚠️已过期"
            elif task.due_date.date() == date.today():
                due_str = f"截止: 今天 {task.due_date.strftime('%H:%M')}"
            else:
                due_str = f"截止: {task.due_date.strftime('%Y-%m-%d %H:%M')}"
        
        # 提醒时间显示
        remind_str = ""
        if task.reminder_time:
            if task.reminder_time.date() == date.today():
                remind_str = f"提醒: 今天 {task.reminder_time.strftime('%H:%M')}"
            else:
                remind_str = f"提醒: {task.reminder_time.strftime('%Y-%m-%d %H:%M')}"
        
        print(f"{status_icon} [{task.id}] {task.content} {priority_str}")
        
        info_parts = [part for part in [due_str, remind_str] if part]
        if info_parts:
            print(f"    {' | '.join(info_parts)}")
    
    def _sort_tasks_by_priority_and_deadline(self, tasks: List[Task]) -> List[Task]:
        """按优先级和截止时间排序"""
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
    
    def show_today_summary(self):
        """显示今日任务摘要"""
        today_tasks = self._get_today_tasks()
        if not today_tasks:
            print("今天没有待办任务")
            return
        
        sorted_tasks = self._sort_tasks_by_priority_and_deadline(today_tasks)
        
        print("\n⚠️ 今日任务摘要:")
        print("=" * 60)
        print("○ 待办事项:")
        print("-" * 60)
        
        for task in sorted_tasks:
            priority_str = f"[{task.priority}]" if task.priority else "[无]"
            due_str = ""
            if task.due_date:
                if task.due_date.date() == date.today():
                    due_str = f" ({task.due_date.strftime('%H:%M')})"
                elif task.due_date.date() < date.today():
                    due_str = f" (已过期: {task.due_date.strftime('%m-%d %H:%M')})"
                else:
                    due_str = f" ({task.due_date.strftime('%m-%d %H:%M')})"
            
            print(f"{priority_str} {task.content}{due_str}")
        
        print("=" * 60)
    
    def _get_today_tasks(self) -> List[Task]:
        """获取今日相关任务"""
        all_tasks = self.task_manager.get_all_tasks()
        today = date.today()
        today_tasks = []
        
        for task in all_tasks:
            if task.status == "completed":
                continue
            
            if task.due_date and task.due_date.date() == today:
                today_tasks.append(task)
            elif task.reminder_time and task.reminder_time.date() == today:
                today_tasks.append(task)
            elif task.due_date and task.due_date.date() < today:
                today_tasks.append(task)
        
        return today_tasks
    
    def quick_add_task(self, content: str, priority: Optional[str] = None):
        """用于快速输入窗口的任务添加"""
        task = self.task_manager.add_task(content, priority)
        return task