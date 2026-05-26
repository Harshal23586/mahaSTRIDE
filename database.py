from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime
import enum

Base = declarative_base()

class TaskStatus(enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class University(Base):
    __tablename__ = 'universities'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    coordinators = Column(String(500), nullable=False)
    nodal_officer = Column(String(200), nullable=True)
    registrar = Column(String(200), nullable=True)
    vc = Column(String(200), nullable=True)
    created_at = Column(DateTime, default=func.now())
    
    def __repr__(self):
        return f"<University(name='{self.name}', code='{self.code}')>"

class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True)
    day = Column(Integer, nullable=False)
    framework = Column(String(50), nullable=False)
    task_name = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    def __repr__(self):
        return f"<Task(day={self.day}, framework='{self.framework}')>"

class TaskProgress(Base):
    __tablename__ = 'task_progress'
    
    id = Column(Integer, primary_key=True)
    university_id = Column(Integer, ForeignKey('universities.id'), nullable=False)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    status = Column(String(20), default=TaskStatus.PENDING.value)
    remarks = Column(String(1000), default="")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    updated_by = Column(String(100), nullable=True)
    
    def __repr__(self):
        return f"<TaskProgress(uni_id={self.university_id}, task_id={self.task_id}, status='{self.status}')>"

class DailyWorkLog(Base):
    __tablename__ = 'daily_work_logs'
    
    id = Column(Integer, primary_key=True)
    university_id = Column(Integer, ForeignKey('universities.id'), nullable=False)
    work_date = Column(String(20), nullable=False)  # YYYY-MM-DD format
    task_category = Column(String(100), nullable=False)
    task_name = Column(String(500), nullable=False)
    description = Column(String(2000), nullable=True)
    deliverables = Column(String(2000), nullable=True)
    status = Column(String(20), default="in_progress")
    hours_spent = Column(Float, default=0.0)
    remarks = Column(String(1000), nullable=True)
    swapped_from_default = Column(Boolean, default=False)
    edited_task = Column(Boolean, default=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    updated_by = Column(String(100), nullable=True)
    
    # Composite unique constraint handled by application logic
    
    def __repr__(self):
        return f"<DailyWorkLog(uni_id={self.university_id}, date='{self.work_date}')>"

class Assignment(Base):
    __tablename__ = 'assignments'
    
    id = Column(String(50), primary_key=True)
    title = Column(String(500), nullable=False)
    description = Column(String(2000), nullable=True)
    due_date = Column(String(20), nullable=False)
    created_by = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=func.now())
    status = Column(String(20), default="active")
    
    def __repr__(self):
        return f"<Assignment(id='{self.id}', title='{self.title}')>"

class AssignmentSubmission(Base):
    __tablename__ = 'assignment_submissions'
    
    id = Column(Integer, primary_key=True)
    assignment_id = Column(String(50), ForeignKey('assignments.id'), nullable=False)
    university_id = Column(Integer, ForeignKey('universities.id'), nullable=False)
    status = Column(String(20), default="pending")
    remarks = Column(String(1000), nullable=True)
    completed_at = Column(DateTime, nullable=True)
    completed_by = Column(String(200), nullable=True)
    submitted_at = Column(DateTime, default=func.now())
    
    def __repr__(self):
        return f"<AssignmentSubmission(assignment='{self.assignment_id}', uni={self.university_id})>"

class CustomTask(Base):
    __tablename__ = 'custom_tasks'
    
    id = Column(Integer, primary_key=True)
    date = Column(String(20), nullable=False)  # YYYY-MM-DD format
    task_category = Column(String(100), nullable=False)
    task_name = Column(String(500), nullable=False)
    description = Column(String(2000), nullable=False)
    deliverables = Column(String(2000), nullable=False)
    added_by = Column(String(200), nullable=False)
    added_at = Column(DateTime, default=func.now())
    
    def __repr__(self):
        return f"<CustomTask(date='{self.date}', task='{self.task_name}')>"

class CoordinatorCredentials(Base):
    __tablename__ = 'coordinator_credentials'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(200), unique=True, nullable=False)
    password_hash = Column(String(200), nullable=False)
    name = Column(String(200), nullable=False)
    university_code = Column(String(20), ForeignKey('universities.code'), nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    def __repr__(self):
        return f"<CoordinatorCredentials(email='{self.email}')>"
