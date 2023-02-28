from sqlalchemy import Column, Integer, String
from database import Base


class EmployeeData(Base):
    __tablename__ = 'employee'
    roll_id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(Integer)
    major = Column(String)
