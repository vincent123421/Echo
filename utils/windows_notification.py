import os
import sys
import tempfile
import subprocess
import threading
import time
from typing import Callable, Optional

class WindowsNotification:
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
        self.flag_file = os.path.join(self.temp_dir, "echo_notification_clicked.flag")
    
    def show_clickable_notification(self, title: str, message: str, 
                                  callback: Optional[Callable] = None,
                                  timeout: int = 10):
        """显示可点击的Windows通知"""
        try:
            # 清理旧的标志文件
            if os.path.exists(self.flag_file):
                os.remove(self.flag_file)
            
            # 创建PowerShell脚本来显示通知
            ps_script = self._create_powershell_script(title, message)
            
            # 在后台线程中执行
            threading.Thread(
                target=self._run_notification_with_callback,
                args=(ps_script, callback, timeout),
                daemon=True
            ).start()
            
            return True
            
        except Exception as e:
            print(f"Windows通知失败: {e}")
            return False
    
    def _create_powershell_script(self, title: str, message: str) -> str:
        """创建PowerShell通知脚本"""
        # 转义特殊字符
        title = title.replace('"', '""')
        message = message.replace('"', '""')
        
        script = f'''
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$notify = New-Object System.Windows.Forms.NotifyIcon
$notify.Icon = [System.Drawing.SystemIcons]::Information
$notify.BalloonTipTitle = "{title}"
$notify.BalloonTipText = "{message}\\n\\n点击此通知打开任务界面"
$notify.Visible = $true

# 添加点击事件处理
$notify.add_BalloonTipClicked({{
    # 创建标志文件表示被点击
    New-Item -Path "{self.flag_file}" -ItemType File -Force | Out-Null
}})

$notify.ShowBalloonTip(10000)
Start-Sleep -Seconds 15
$notify.Dispose()
'''
        return script
    
    def _run_notification_with_callback(self, ps_script: str, 
                                      callback: Optional[Callable], 
                                      timeout: int):
        """运行通知并监听点击事件"""
        try:
            # 执行PowerShell脚本
            process = subprocess.Popen([
                'powershell', '-Command', ps_script
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
            creationflags=subprocess.CREATE_NO_WINDOW)
            
            # 监听点击事件
            start_time = time.time()
            while time.time() - start_time < timeout + 5:  # 多等5秒
                if os.path.exists(self.flag_file):
                    # 通知被点击了
                    print("通知被点击，正在打开任务界面...")
                    if callback:
                        try:
                            callback()
                        except Exception as e:
                            print(f"执行回调失败: {e}")
                    
                    # 清理标志文件
                    try:
                        os.remove(self.flag_file)
                    except:
                        pass
                    break
                
                time.sleep(0.5)  # 每0.5秒检查一次
            
            # 确保进程结束
            try:
                process.terminate()
            except:
                pass
                
        except Exception as e:
            print(f"运行通知脚本失败: {e}")
            # 备用方案：显示简单提示
            print(f"通知: {title} - {message}")
            if callback:
                print("要打开任务界面，请运行: python main.py show")