#!/usr/bin/env python3
"""
测试任务界面的脚本
"""

from datetime import datetime, timedelta
from managers.task_manager import TaskManager
from ui.task_detail_window import TaskDetailWindow

def create_test_tasks():
    """创建一些测试任务"""
    task_manager = TaskManager()
    
    # 创建不同优先级和时间的测试任务
    test_tasks = [
        {
            "content": "完成项目文档",
            "priority": "高",
            "due_date": datetime.now() + timedelta(hours=2),
            "reminder_time": datetime.now() + timedelta(hours=1)
        },
        {
            "content": "买菜做饭",
            "priority": "中",
            "due_date": datetime.now() + timedelta(days=1),
            "reminder_time": datetime.now() + timedelta(hours=18)
        },
        {
            "content": "学习Python",
            "priority": "低",
            "due_date": datetime.now() + timedelta(days=3),
            "reminder_time": None
        },
        {
            "content": "过期任务测试",
            "priority": "高",
            "due_date": datetime.now() - timedelta(hours=2),
            "reminder_time": None
        },
        {
            "content": "已完成的任务",
            "priority": "中",
            "due_date": datetime.now() - timedelta(days=1),
            "reminder_time": None
        }
    ]
    
    created_tasks = []
    for task_data in test_tasks:
        task = task_manager.add_task(
            content=task_data["content"],
            priority=task_data["priority"],
            due_date=task_data["due_date"],
            reminder_time=task_data["reminder_time"]
        )
        created_tasks.append(task)
    
    # 标记最后一个任务为已完成
    task_manager.update_task(created_tasks[-1].id, status="completed")
    
    print(f"创建了 {len(created_tasks)} 个测试任务")
    return created_tasks

def main():
    print("创建测试任务...")
    create_test_tasks()
    
    print("打开任务管理界面...")
    detail_window = TaskDetailWindow()
    detail_window.show()

if __name__ == "__main__":
    main()