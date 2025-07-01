import sqlite3
import os
from typing import List, Optional
from datetime import datetime
from models.task import Task
from config import DATABASE_PATH

class TaskManager:
    def __init__(self):
        self._init_database()
    
    def _init_database(self):
        os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
        
        with sqlite3.connect(DATABASE_PATH) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    status TEXT NOT NULL,
                    priority TEXT,
                    due_date DATETIME,
                    created_at DATETIME
                )
            ''')
            conn.commit()
    
    def add_task(self, content: str, priority: Optional[str] = None, 
                 due_date: Optional[datetime] = None) -> Task:
        task = Task(content=content, priority=priority, due_date=due_date)
        
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.execute('''
                INSERT INTO tasks (content, status, priority, due_date, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (task.content, task.status, task.priority,
                  task.due_date.isoformat() if task.due_date else None,
                  task.created_at.isoformat()))
            
            task.id = cursor.lastrowid
            conn.commit()
        
        return task
    
    def get_all_tasks(self) -> List[Task]:
        with sqlite3.connect(DATABASE_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('SELECT * FROM tasks ORDER BY created_at DESC')
            rows = cursor.fetchall()
        
        tasks = []
        for row in rows:
            task_data = dict(row)
            if task_data['due_date']:
                task_data['due_date'] = datetime.fromisoformat(task_data['due_date'])
            if task_data['created_at']:
                task_data['created_at'] = datetime.fromisoformat(task_data['created_at'])
            tasks.append(Task(**task_data))
        
        return tasks
    
    def update_task(self, task_id: int, **kwargs) -> bool:
        if not kwargs:
            return False
            
        set_clause = ', '.join([f"{key} = ?" for key in kwargs.keys()])
        values = list(kwargs.values())
        values.append(task_id)
        
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.execute(f'UPDATE tasks SET {set_clause} WHERE id = ?', values)
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_task(self, task_id: int) -> bool:
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            conn.commit()
            return cursor.rowcount > 0