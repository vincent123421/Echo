#!/usr/bin/env python3
"""
测试点击通知功能
"""

from utils.notification_helper import NotificationHelper
from ui.task_detail_window import TaskDetailWindow

def test_click_notification():
    """测试点击通知功能"""
    print("测试点击通知功能...")
    
    notification_helper = NotificationHelper()
    
    def open_task_window():
        print("通知被点击了！正在打开任务管理界面...")
        detail_window = TaskDetailWindow()
        detail_window.show()
    
    print("发送测试通知...")
    print("请点击弹出的通知来测试点击功能")
    
    notification_helper.show_clickable_notification(
        title="Echo 测试通知",
        message="这是一个测试通知\n请点击这个通知来打开任务管理界面",
        callback=open_task_window,
        timeout=30
    )
    
    print("通知已发送，请观察：")
    print("1. 是否弹出桌面通知")
    print("2. 点击通知后是否打开任务管理界面")
    print("3. 如果不支持点击，会显示手动命令提示")

if __name__ == "__main__":
    test_click_notification()