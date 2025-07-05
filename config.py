import os

# 数据库配置
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'data', 'tasks.db')

# 全局快捷键配置
GLOBAL_HOTKEY = 'ctrl+shift+t'

# 每日提醒时间配置
DAILY_REMINDER_HOUR = 8
DAILY_REMINDER_MINUTE = 0