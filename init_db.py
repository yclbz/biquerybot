import asyncio
from datetime import datetime, timedelta
from sqlalchemy import insert
from .models import SalesData
from .db import async_session, init_db

async def create_test_data():
    """創建測試數據"""
    # 產品列表
    products = ["筆記型電腦", "智慧手機", "平板電腦", "耳機", "智慧手錶"]
    
    # 生成過去60天的銷售數據
    today = datetime.now().date()
    data = []
    
    for i in range(60):
        date = today - timedelta(days=i)
        for product in products:
            # 模擬銷售數量（1-10）和單價（1000-5000）
            sales_amount = (i % 10) + 1
            price = (products.index(product) + 1) * 1000
            revenue = sales_amount * price
            
            data.append({
                "sales_date": date,
                "product_name": product,
                "sales_amount": sales_amount,
                "revenue": revenue
            })
    
    async with async_session() as session:
        # 插入數據
        await session.execute(insert(SalesData), data)
        await session.commit()

async def init_database():
    """初始化數據庫並創建測試數據"""
    try:
        # 初始化數據庫結構
        await init_db()
        print("Database structure initialized successfully")
        
        # 創建測試數據
        await create_test_data()
        print("Test data created successfully")
        
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        raise 