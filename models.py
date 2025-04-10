from sqlalchemy import Column, Integer, String, Float, Date
from .db import Base

class SalesData(Base):
    __tablename__ = "sales_data"

    id = Column(Integer, primary_key=True, index=True)
    sales_date = Column(Date, index=True)
    product_name = Column(String, index=True)
    sales_amount = Column(Integer)
    revenue = Column(Float) 