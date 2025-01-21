from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Float, Integer, String,DateTime
from datetime import datetime

Base = declarative_base()

class ticket_price(Base):
     __tablename__ = "stock_price"
     id = id = Column(Integer, primary_key=True)
     valor = Column(Float)
     data = Column(DateTime)