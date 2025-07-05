import unittest
from datetime import datetime, date
from utils.datetime_parser import parse_datetime

class TestDateTimeParser(unittest.TestCase):
    
    def test_full_datetime(self):
        """测试完整日期时间格式"""
        result = parse_datetime("2024-12-25 18:00")
        expected = datetime(2024, 12, 25, 18, 0)
        self.assertEqual(result, expected)
    
    def test_date_only(self):
        """测试仅日期格式"""
        result = parse_datetime("2024-12-25")
        expected = datetime(2024, 12, 25, 0, 0)
        self.assertEqual(result, expected)
    
    def test_time_only(self):
        """测试仅时间格式（应设置为今天）"""
        result = parse_datetime("18:00")
        today = date.today()
        expected = datetime(today.year, today.month, today.day, 18, 0)
        self.assertEqual(result, expected)
    
    def test_month_day_time(self):
        """测试月日时间格式（应设置为今年）"""
        result = parse_datetime("12-25 14:30")
        current_year = datetime.now().year
        expected = datetime(current_year, 12, 25, 14, 30)
        self.assertEqual(result, expected)
    
    def test_invalid_format(self):
        """测试无效格式"""
        result = parse_datetime("invalid-date")
        self.assertIsNone(result)
    
    def test_empty_string(self):
        """测试空字符串"""
        result = parse_datetime("")
        self.assertIsNone(result)
    
    def test_none_input(self):
        """测试None输入"""
        result = parse_datetime(None)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()