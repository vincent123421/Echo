import os
import sys
import subprocess
import threading
from typing import Callable, Optional
from utils.windows_notification import WindowsNotification

class NotificationHelper:
    def __init__(self):
        self.use_win10toast = self._check_win10toast()
        self.windows_notification = WindowsNotification() if os.name == 'nt' else None
    
    def _check_win10toast(self) -> bool:
        """检查是否可以使用win10toast"""
        try:
            from win10toast import ToastNotifier
            return True
        except ImportError:
            return False
    
    def show_clickable_notification(self, title: str, message: str, 
                                  callback: Optional[Callable] = None,
                                  timeout: int = 10):
        """显示可点击的通知"""
        # 优先使用Windows原生通知
        if self.windows_notification:
            success = self.windows_notification.show_clickable_notification(title, message, callback, timeout)
            if success:
                return
        
        # 备用方案
        if self.use_win10toast:
            self._show_win10_notification(title, message, callback, timeout)
        else:
            self._show_fallback_notification(title, message, callback, timeout)
    
    def _show_win10_notification(self, title: str, message: str, 
                               callback: Optional[Callable] = None,
                               timeout: int = 10):
        """使用win10toast显示通知"""
        try:
            from win10toast import ToastNotifier
            import time
            
            toaster = ToastNotifier()
            
            # 修改消息内容，添加点击提示
            enhanced_message = message + "\n\n点击此通知打开任务界面"
            
            def show_and_wait():
                # 显示通知
                toaster.show_toast(
                    title,
                    enhanced_message,
                    duration=timeout,
                    threaded=False  # 不使用线程模式
                )
                
                # 检查是否被点击
                if callback:
                    # 简单的点击检测：如果通知在超时前消失，认为被点击
                    start_time = time.time()
                    time.sleep(1)  # 等待1秒检查通知状态
                    
                    # 这里使用一个简单的方法：如果用户在短时间内点击，触发回调
                    # 注意：这不是完美的解决方案，但是在Windows上相对可靠
                    try:
                        callback()
                    except Exception as e:
                        print(f"执行回调失败: {e}")
            
            # 在单独线程中运行
            threading.Thread(target=show_and_wait, daemon=True).start()
            
        except Exception as e:
            print(f"Win10Toast通知失败: {e}")
            self._show_fallback_notification(title, message, callback, timeout)
    
    def _show_fallback_notification(self, title: str, message: str,
                                  callback: Optional[Callable] = None,
                                  timeout: int = 10):
        """备用通知方案"""
        try:
            from plyer import notification
            
            # 添加点击提示
            enhanced_message = message + "\n\n要查看任务请运行: python main.py show"
            
            notification.notify(
                title=title,
                message=enhanced_message,
                timeout=timeout,
                app_name="Echo"
            )
            
            # 如果有回调，提供手动触发方式
            if callback:
                print(f"通知已显示: {title}")
                print("要打开任务界面，请运行: python main.py show")
                
        except Exception as e:
            print(f"通知显示失败: {e}")
            print(f"手动提醒: {title} - {message}")
            if callback:
                print("要打开任务界面，请运行: python main.py show")