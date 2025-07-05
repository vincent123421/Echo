from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, date
from typing import Optional, List
from models.task import Task
from managers.task_manager import TaskManager
from config import DAILY_REMINDER_HOUR, DAILY_REMINDER_MINUTE
from utils.notification_helper import NotificationHelper
import threading

class ReminderManager:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.task_manager = TaskManager()
        self.notification_helper = NotificationHelper()
    
    def start(self):
        """启动调度器"""
        if not self.scheduler.running:
            self.scheduler.start()
            # 加载现有任务的提醒
            self._load_existing_reminders()
            # 设置每日定时提醒
            self._setup_daily_reminder()
    
    def stop(self):
        """停止调度器"""
        if self.scheduler.running:
            self.scheduler.shutdown()
    
    def add_reminder(self, task: Task):
        """为任务添加提醒"""
        if not task.reminder_time or not task.id:
            return
        
        # 如果提醒时间已过，不添加提醒
        if task.reminder_time <= datetime.now():
            return
        
        job_id = f"task_{task.id}"
        
        # 移除已存在的提醒
        try:
            self.scheduler.remove_job(job_id)
        except:
            pass
        
        # 添加新提醒
        self.scheduler.add_job(
            func=self._send_notification,
            trigger='date',
            run_date=task.reminder_time,
            args=[task.id],
            id=job_id
        )
    
    def remove_reminder(self, task_id: int):
        """移除任务提醒"""
        job_id = f"task_{task_id}"
        try:
            self.scheduler.remove_job(job_id)
        except:
            pass
    
    def _send_notification(self, task_id: int):
        """发送桌面通知"""
        task = self.task_manager.get_task_by_id(task_id)
        if not task:
            return
        
        title = "任务提醒"
        message = f"{task.content}"
        
        if task.due_date:
            due_str = task.due_date.strftime('%Y-%m-%d %H:%M')
            message += f"\n截止时间: {due_str}"
        
        # 使用新的通知系统，支持点击回调
        self.notification_helper.show_clickable_notification(
            title=title,
            message=message,
            callback=self._open_task_detail_window,
            timeout=10
        )
    
    def _open_task_detail_window(self):
        """打开任务详情窗口"""
        try:
            from ui.task_detail_window import TaskDetailWindow
            detail_window = TaskDetailWindow()
            detail_window.show()
        except Exception as e:
            print(f"打开任务窗口失败: {e}")
    
    def _setup_daily_reminder(self):
        """设置每日定时提醒"""
        self.scheduler.add_job(
            func=self._send_daily_summary,
            trigger='cron',
            hour=DAILY_REMINDER_HOUR,
            minute=DAILY_REMINDER_MINUTE,
            id='daily_reminder'
        )
    
    def _send_daily_summary(self):
        """发送每日任务摘要"""
        today_tasks = self._get_today_tasks()
        if not today_tasks:
            return
        
        # 按优先级和截止时间排序
        sorted_tasks = self._sort_tasks_by_priority_and_deadline(today_tasks)
        
        # 构建通知内容
        message = "⚠️ 早上好！这是今天的待办事项：\n\n--- 待办事项 ---\n"
        
        for task in sorted_tasks:
            priority_str = f"[{task.priority}]" if task.priority else "[无]"
            due_str = ""
            if task.due_date:
                if task.due_date.date() == date.today():
                    due_str = f" ({task.due_date.strftime('%H:%M')})"
                else:
                    due_str = f" ({task.due_date.strftime('%m-%d %H:%M')})"
            
            message += f"{priority_str} {task.content}{due_str}\n"
        
        # 使用新的通知系统发送每日提醒
        self.notification_helper.show_clickable_notification(
            title="今日任务提醒",
            message=message,
            callback=self._open_task_detail_window,
            timeout=15
        )
    

    
    def _get_today_tasks(self) -> List[Task]:
        """获取今日相关任务"""
        all_tasks = self.task_manager.get_all_tasks()
        today = date.today()
        today_tasks = []
        
        for task in all_tasks:
            if task.status == "completed":
                continue
            
            # 今天截止的任务
            if task.due_date and task.due_date.date() == today:
                today_tasks.append(task)
            # 今天提醒的任务
            elif task.reminder_time and task.reminder_time.date() == today:
                today_tasks.append(task)
            # 过期任务
            elif task.due_date and task.due_date.date() < today:
                today_tasks.append(task)
        
        return today_tasks
    
    def _sort_tasks_by_priority_and_deadline(self, tasks: List[Task]) -> List[Task]:
        """按优先级和截止时间排序"""
        priority_order = {"高": 3, "中": 2, "低": 1, None: 0}
        
        def sort_key(task):
            # 优先级权重
            priority_weight = priority_order.get(task.priority, 0)
            
            # 时间紧急度（越近的时间权重越高）
            time_weight = 0
            if task.due_date:
                now = datetime.now()
                time_diff = (task.due_date - now).total_seconds()
                # 过期任务最高优先级
                if time_diff < 0:
                    time_weight = 1000
                # 今天内的任务
                elif time_diff < 86400:  # 24小时
                    time_weight = 100
                # 未来任务
                else:
                    time_weight = max(0, 50 - time_diff / 86400)
            
            # 综合权重（优先级 * 10 + 时间紧急度）
            return -(priority_weight * 10 + time_weight)
        
        return sorted(tasks, key=sort_key)
    
    def _load_existing_reminders(self):
        """加载现有任务的提醒"""
        tasks = self.task_manager.get_all_tasks()
        for task in tasks:
            if task.status != "completed" and task.reminder_time:
                self.add_reminder(task)