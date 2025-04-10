import asyncio
from datetime import datetime, timedelta
from sqlalchemy import insert
from db import init_db, async_session, SalesData

async def insert_test_data():
    # Initialize database
    await init_db()
    
    # Generate test data
    test_data = []
    products = ["筆記型電腦", "智慧手機", "平板電腦", "耳機", "滑鼠"]
    
    # Generate data for the last 3 months
    today = datetime.now()
    for i in range(90):
        date = today - timedelta(days=i)
        for product in products:
            # Random sales amount between 1 and 10
            sales_amount = (i % 10) + 1
            # Random revenue between 1000 and 50000
            revenue = sales_amount * (1000 + (i % 50) * 1000)
            
            test_data.append({
                "product_name": product,
                "sales_date": date.date(),
                "sales_amount": sales_amount,
                "revenue": revenue
            })

    # Insert data
    async with async_session() as session:
        await session.execute(insert(SalesData), test_data)
        await session.commit()

if __name__ == "__main__":
    asyncio.run(insert_test_data())
    print("測試資料已成功插入！") 