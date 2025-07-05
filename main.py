import argparse
import sys
import threading
from ui.cli_handler import CLIHandler
from ui.quick_input import QuickInputWindow
from managers.reminder_manager import ReminderManager
from config import GLOBAL_HOTKEY

try:
    import keyboard
except ImportError:
    keyboard = None
    print("警告: 未安装keyboard库，全局快捷键功能不可用")
    print("请运行: pip install keyboard")

def setup_global_hotkey():
    """设置全局快捷键"""
    if not keyboard:
        return
    
    def show_quick_input():
        quick_input = QuickInputWindow()
        quick_input.show()
    
    keyboard.add_hotkey(GLOBAL_HOTKEY, show_quick_input)
    print(f"全局快捷键已设置: {GLOBAL_HOTKEY}")

def main():
    cli_handler = CLIHandler()
    reminder_manager = ReminderManager()
    reminder_manager.start()
    
    parser = argparse.ArgumentParser(description='任务管理工具')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # add命令
    add_parser = subparsers.add_parser('add', help='添加任务')
    add_parser.add_argument('content', help='任务内容')
    add_parser.add_argument('-p', '--priority', help='优先级')
    add_parser.add_argument('-d', '--due-date', help='截止日期 (YYYY-MM-DD HH:MM)')
    add_parser.add_argument('-r', '--remind', help='提醒时间 (YYYY-MM-DD HH:MM)')
    
    # list命令
    subparsers.add_parser('list', help='列出所有任务')
    
    # done命令
    done_parser = subparsers.add_parser('done', help='标记任务完成')
    done_parser.add_argument('id', type=int, help='任务ID')
    
    # delete命令
    delete_parser = subparsers.add_parser('delete', help='删除任务')
    delete_parser.add_argument('id', type=int, help='任务ID')
    
    # today命令 - 显示今日任务摘要
    subparsers.add_parser('today', help='显示今日任务摘要')
    
    # show命令 - 打开任务管理界面
    subparsers.add_parser('show', help='打开任务管理界面')
    
    # daemon命令 - 启动后台监听
    subparsers.add_parser('daemon', help='启动后台快捷键监听')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'add':
        task = cli_handler.add_task(args.content, args.priority, args.due_date, args.remind)
        if task and task.reminder_time:
            reminder_manager.add_reminder(task)
    elif args.command == 'list':
        cli_handler.list_tasks()
    elif args.command == 'done':
        cli_handler.mark_done(args.id)
    elif args.command == 'delete':
        cli_handler.delete_task(args.id)
    elif args.command == 'today':
        cli_handler.show_today_summary()
    elif args.command == 'show':
        from ui.task_detail_window import TaskDetailWindow
        detail_window = TaskDetailWindow()
        detail_window.show()
    elif args.command == 'daemon':
        if keyboard:
            setup_global_hotkey()
            print("后台监听已启动，按Ctrl+C退出")
            try:
                keyboard.wait()
            except KeyboardInterrupt:
                print("\n后台监听已停止")
                reminder_manager.stop()
        else:
            print("无法启动后台监听，请安装keyboard库")

if __name__ == '__main__':
    main()
