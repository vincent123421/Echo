from datetime import datetime
from typing import Optional

class Task:
    def __init__(self, id: Optional[int] = None, content: str = "", 
                 status: str = "pending", priority: Optional[str] = None,
                 due_date: Optional[datetime] = None, created_at: Optional[datetime] = None):
        self.id = id
        self.content = content
        self.status = status
        self.priority = priority
        self.due_date = due_date
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'content': self.content,
            'status': self.status,
            'priority': self.priority,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'created_at': self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        task = cls(
            id=data.get('id'),
            content=data.get('content', ''),
            status=data.get('status', 'pending'),
            priority=data.get('priority')
        )
        
        if data.get('due_date'):
            task.due_date = datetime.fromisoformat(data['due_date'])
        if data.get('created_at'):
            task.created_at = datetime.fromisoformat(data['created_at'])
            
        return task