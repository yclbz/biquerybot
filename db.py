from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Date, text
import os
from pathlib import Path

# 創建數據庫目錄（如果不存在）
db_dir = Path(__file__).parent.parent / "data"
db_dir.mkdir(exist_ok=True)

# 數據庫 URL
DATABASE_URL = f"sqlite+aiosqlite:///{db_dir}/sales.db"

# 創建異步引擎
engine = create_async_engine(DATABASE_URL, echo=True)

# 創建異步會話工廠
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# 創建 Base 類
Base = declarative_base()

async def init_db():
    """初始化數據庫"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db() -> AsyncSession:
    """獲取數據庫會話"""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

# Execute raw SQL query
async def execute_query(session: AsyncSession, query: str):
    result = await session.execute(text(query))
    return result.mappings().all() 