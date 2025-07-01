# Echo - 任务管理工具

一个支持命令行操作和全局快捷键的轻量级任务管理工具。

## 功能特性

- 命令行任务增删改查
- 全局快捷键快速添加任务
- SQLite数据持久化
- 任务优先级和截止日期支持

## 安装

```bash
pip install -r requirements.txt
```

## 使用方法

### 命令行操作

```bash
# 添加任务
python main.py add "完成项目文档" -p 高 -d 2024-12-31

# 列出所有任务
python main.py list

# 标记任务完成
python main.py done 1

# 删除任务
python main.py delete 1
```

### 全局快捷键

```bash
# 启动后台监听
python main.py daemon
```

启动后，按 `Ctrl+Shift+T` 可快速呼出任务添加窗口。

## 项目结构

```
Echo/
├── main.py              # 主程序入口
├── config.py            # 配置文件
├── models/
│   └── task.py         # Task数据模型
├── managers/
│   └── task_manager.py # 任务管理器
├── ui/
│   ├── cli_handler.py  # 命令行处理
│   └── quick_input.py  # 快速输入窗口
├── data/               # 数据库文件目录
└── tests/              # 测试文件
```
