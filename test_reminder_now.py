#!/usr/bin/env python3
"""
立即测试提醒功能
"""

import time
from datetime import datetime, timedelta
from managers.task_manager import TaskManager
from managers.reminder_manager import ReminderManager

def test_immediate_reminder():
    """测试立即提醒"""
    print("创建测试任务和提醒...")
    
    # 创建任务管理器和提醒管理器
    task_manager = TaskManager()
    reminder_manager = ReminderManager()
    
    # 创建一个3秒后提醒的任务
    reminder_time = datetime.now() + timedelta(seconds=3)
    due_time = datetime.now() + timedelta(hours=2)
    
    task = task_manager.add_task(
        content="这是一个测试提醒任务",
        priority="高",
        due_date=due_time,
        reminder_time=reminder_time
    )
    
    print(f"任务已创建: {task.content}")
    print(f"提醒时间: {reminder_time.strftime('%H:%M:%S')}")
    print("启动提醒管理器...")
    
    # 启动提醒管理器
    reminder_manager.start()
    reminder_manager.add_reminder(task)
    
    print("等待3秒后的提醒通知...")
    print("注意观察：")
    print("1. 是否弹出桌面通知")
    print("2. 点击通知后是否打开任务管理界面")
    print("3. 如果不支持点击，请手动运行: python main.py show")
    
    # 等待提醒触发
    time.sleep(5)  # 等待5秒确保提醒触发
    
    # 清理测试任务
    task_manager.delete_task(task.id)
    reminder_manager.stop()
    
    print("✅ 测试完成，测试任务已清理")

def test_daily_summary():
    """测试每日摘要提醒"""
    print("\n测试每日摘要提醒...")
    
    reminder_manager = ReminderManager()
    reminder_manager.start()
    
    print("手动触发每日摘要通知...")
    reminder_manager._send_daily_summary()
    
    print("观察每日摘要通知是否弹出，然后点击通知打开界面...")
    time.sleep(3)
    
    reminder_manager.stop()
    print("✅ 每日摘要测试完成")

if __name__ == "__main__":
    print("Echo 提醒功能实时测试")
    print("=" * 50)
    
    # 测试立即提醒
    test_immediate_reminder()
    
    # 测试每日摘要
    test_daily_summary()
    
    print("\n" + "=" * 50)
    print("测试说明：")
    print("1. 如果看到桌面通知弹出 = 通知功能正常")
    print("2. 如果点击通知后打开任务管理界面 = 点击功能正常")
    print("3. 如果界面显示任务列表 = 界面功能正常")
    print("4. 如果不支持点击，请手动运行: python main.py show")