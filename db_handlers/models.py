from sqlalchemy import Column, Integer, Date, Float
from create_bot import Base

class Order(Base):
    __tablename__ = "client_bills"

    order_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    sum = Column(Float, nullable=False)