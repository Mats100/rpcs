from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class EmployeeData(Base):
    __tablename__ = 'employee'
    roll_id = Column(Integer, unique=True, primary_key=True)
    name = Column(String)
    phone = Column(String)
    major = Column(String)
