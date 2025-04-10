import os
from pathlib import Path
from datetime import datetime, timedelta
import re

class LLMAgent:
    def __init__(self):
        # 定義查詢模式和對應的 SQL 模板
        self.query_patterns = {
            r"上個月的(總)?銷售額": """
                SELECT SUM(revenue) as total_revenue 
                FROM sales_data 
                WHERE sales_date >= date('now', 'start of month', '-1 month') 
                AND sales_date < date('now', 'start of month')
            """,
            
            r"(統計|查詢)每個產品的(總)?銷售數量": """
                SELECT product_name, SUM(sales_amount) as total_sales 
                FROM sales_data 
                GROUP BY product_name 
                ORDER BY total_sales DESC
            """,
            
            r"銷售(額|收入|金額)最高的前(?P<limit>\d+)名產品": """
                SELECT product_name, SUM(revenue) as total_revenue 
                FROM sales_data 
                GROUP BY product_name 
                ORDER BY total_revenue DESC 
                LIMIT {limit}
            """,
            
            r"(?P<product>.+)的平均每日銷售量": """
                SELECT product_name, AVG(sales_amount) as avg_daily_sales 
                FROM sales_data 
                WHERE product_name = '{product}' 
                GROUP BY product_name
            """,
            
            r"本月(每天的)?(總)?(收入|銷售額)": """
                SELECT sales_date, SUM(revenue) as daily_revenue 
                FROM sales_data 
                WHERE sales_date >= date('now', 'start of month') 
                GROUP BY sales_date 
                ORDER BY sales_date
            """,
            
            r"過去(?P<days>\d+)天的銷售趨勢": """
                SELECT sales_date, SUM(revenue) as daily_revenue 
                FROM sales_data 
                WHERE sales_date >= date('now', '-{days} days') 
                GROUP BY sales_date 
                ORDER BY sales_date
            """
        }

    async def generate_sql_query(self, question: str) -> str:
        """
        根據預定義的模式生成 SQL 查詢
        """
        try:
            # 清理輸入的問題
            question = question.strip().lower()
            
            # 尋找匹配的模式
            for pattern, sql_template in self.query_patterns.items():
                match = re.search(pattern, question)
                if match:
                    # 如果有捕獲組，使用它們來格式化 SQL
                    if match.groupdict():
                        return sql_template.format(**match.groupdict()).strip()
                    return sql_template.strip()
            
            # 如果沒有找到匹配的模式，返回一個基本的查詢
            return """
                SELECT sales_date, product_name, sales_amount, revenue 
                FROM sales_data 
                ORDER BY sales_date DESC 
                LIMIT 10
            """.strip()
            
        except Exception as e:
            print(f"Error generating SQL query: {str(e)}")
            raise Exception(f"Failed to generate SQL query: {str(e)}")

    def _format_date(self, date_str: str) -> str:
        """
        將日期字符串轉換為 SQL 日期格式
        """
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            return date.strftime("%Y-%m-%d")
        except:
            return date_str 