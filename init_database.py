import os
import sys
import asyncio
from pathlib import Path

# 將當前目錄添加到 Python 路徑
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

from app.init_db import init_database

async def setup():
    print("Initializing database...")
    await init_database()
    print("Database initialization complete!")

if __name__ == "__main__":
    asyncio.run(setup()) 