#!/usr/bin/env python3
"""
测试Windows原生通知功能
"""

from utils.windows_notification import WindowsNotification
from ui.task_detail_window import TaskDetailWindow
import time

def test_windows_notification():
    """测试Windows原生通知"""
    print("测试Windows原生通知系统...")
    
    notification = WindowsNotification()
    
    def open_task_window():
        print("✅ 通知被点击了！正在打开任务管理界面...")
        try:
            detail_window = TaskDetailWindow()
            detail_window.show()
        except Exception as e:
            print(f"打开界面失败: {e}")
    
    print("发送测试通知...")
    print("⚠️ 请注意观察系统托盘区域的通知气泡")
    print("📱 点击通知气泡来测试点击功能")
    
    success = notification.show_clickable_notification(
        title="Echo 测试通知",
        message="这是一个测试通知\n请点击这个通知来打开任务管理界面",
        callback=open_task_window,
        timeout=15
    )
    
    if success:
        print("✅ 通知已发送")
        print("⏰ 等待15秒观察点击效果...")
        time.sleep(16)
        print("⏹️ 测试结束")
    else:
        print("❌ 通知发送失败")

if __name__ == "__main__":
    test_windows_notification()