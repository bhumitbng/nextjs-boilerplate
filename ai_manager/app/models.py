from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship

class Employee(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False)

class PerformanceData(Model):
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employee.id'), nullable=False)
    employee = relationship('Employee')
    date = Column(Date, nullable=False)
    performance_score = Column(Float, nullable=False)
    tasks_completed = Column(Integer, nullable=False)

class Goal(Model):
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employee.id'), nullable=False)
    employee = relationship('Employee')
    description = Column(String(500), nullable=False)