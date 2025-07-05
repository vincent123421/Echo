from datetime import datetime
from dateutil import parser
from typing import Optional

def parse_datetime(date_str: str) -> Optional[datetime]:
    """解析日期时间字符串"""
    if not date_str:
        return None
    
    try:
        return parser.parse(date_str)
    except (ValueError, TypeError):
        # 尝试常见格式
        formats = [
            '%Y-%m-%d %H:%M',
            '%Y-%m-%d',
            '%m-%d %H:%M',
            '%H:%M'
        ]
        
        for fmt in formats:
            try:
                parsed = datetime.strptime(date_str, fmt)
                # 如果只有时间，设置为今天
                if fmt == '%H:%M':
                    now = datetime.now()
                    parsed = parsed.replace(year=now.year, month=now.month, day=now.day)
                # 如果只有月日，设置为今年
                elif fmt == '%m-%d %H:%M':
                    parsed = parsed.replace(year=datetime.now().year)
                return parsed
            except ValueError:
                continue
        
        return None