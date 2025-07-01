import unittest
import os
import tempfile
from datetime import datetime
from managers.task_manager import TaskManager
from models.task import Task

class TestTaskManager(unittest.TestCase):
    def setUp(self):
        # 使用临时数据库进行测试
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        
        # 临时修改数据库路径
        import config
        self.original_db_path = config.DATABASE_PATH
        config.DATABASE_PATH = self.temp_db.name
        
        self.task_manager = TaskManager()
    
    def tearDown(self):
        # 恢复原始数据库路径
        import config
        config.DATABASE_PATH = self.original_db_path
        
        # 删除临时数据库
        os.unlink(self.temp_db.name)
    
    def test_add_task(self):
        task = self.task_manager.add_task("测试任务", "高")
        self.assertIsNotNone(task.id)
        self.assertEqual(task.content, "测试任务")
        self.assertEqual(task.priority, "高")
        self.assertEqual(task.status, "pending")
    
    def test_get_all_tasks(self):
        self.task_manager.add_task("任务1")
        self.task_manager.add_task("任务2")
        
        tasks = self.task_manager.get_all_tasks()
        self.assertEqual(len(tasks), 2)
    
    def test_update_task(self):
        task = self.task_manager.add_task("测试任务")
        result = self.task_manager.update_task(task.id, status="completed")
        self.assertTrue(result)
    
    def test_delete_task(self):
        task = self.task_manager.add_task("测试任务")
        result = self.task_manager.delete_task(task.id)
        self.assertTrue(result)
        
        tasks = self.task_manager.get_all_tasks()
        self.assertEqual(len(tasks), 0)

if __name__ == '__main__':
    unittest.main()