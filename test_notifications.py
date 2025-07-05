#!/usr/bin/env python3
"""
测试通知功能的脚本
"""

import sys
import time
from datetime import datetime, timedelta
from managers.reminder_manager import ReminderManager
from managers.task_manager import TaskManager
from models.task import Task

def test_desktop_notification():
    """测试桌面通知"""
    print("测试桌面通知...")
    
    try:
        from plyer import notification
        notification.notify(
            title="Echo 测试通知",
            message="这是一个测试通知，如果你看到这个消息，说明通知功能正常工作！",
            timeout=5
        )
        print("✅ 桌面通知测试成功！")
        return True
    except Exception as e:
        print(f"❌ 桌面通知测试失败: {e}")
        return False

def test_reminder_manager():
    """测试提醒管理器"""
    print("\n测试提醒管理器...")
    
    try:
        # 创建测试任务
        task_manager = TaskManager()
        reminder_manager = ReminderManager()
        
        # 添加一个5秒后提醒的测试任务
        future_time = datetime.now() + timedelta(seconds=5)
        task = task_manager.add_task(
            content="测试提醒任务",
            priority="高",
            reminder_time=future_time
        )
        
        print(f"创建测试任务: {task.content}")
        print(f"提醒时间: {task.reminder_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 启动提醒管理器
        reminder_manager.start()
        reminder_manager.add_reminder(task)
        
        print("等待5秒后的提醒通知...")
        time.sleep(7)  # 等待7秒确保提醒触发
        
        # 清理测试任务
        task_manager.delete_task(task.id)
        reminder_manager.stop()
        
        print("✅ 提醒管理器测试完成！")
        return True
        
    except Exception as e:
        print(f"❌ 提醒管理器测试失败: {e}")
        return False

def test_daily_summary():
    """测试每日摘要功能"""
    print("\n测试每日摘要功能...")
    
    try:
        reminder_manager = ReminderManager()
        reminder_manager.start()
        
        # 手动触发每日摘要
        reminder_manager._send_daily_summary()
        
        reminder_manager.stop()
        print("✅ 每日摘要测试完成！")
        return True
        
    except Exception as e:
        print(f"❌ 每日摘要测试失败: {e}")
        return False

def main():
    print("Echo 通知功能测试")
    print("=" * 50)
    
    results = []
    
    # 测试桌面通知
    results.append(test_desktop_notification())
    
    # 测试提醒管理器
    results.append(test_reminder_manager())
    
    # 测试每日摘要
    results.append(test_daily_summary())
    
    print("\n" + "=" * 50)
    print("测试结果:")
    print(f"成功: {sum(results)}")
    print(f"失败: {len(results) - sum(results)}")
    
    if all(results):
        print("所有通知功能测试通过！")
    else:
        print("部分功能需要检查")

if __name__ == "__main__":
    main()