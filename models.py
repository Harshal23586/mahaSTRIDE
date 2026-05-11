from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass
from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DELAYED = "delayed"

class Framework(Enum):
    SAMARTH = "SAMARTH"
    NEP = "NEP"
    AEGIS = "AEGIS"
    IKS = "IKS"

class University(Base):
    __tablename__ = 'universities'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    coordinators = Column(String)  # Stored as comma-separated string
    
    tasks = relationship("TaskProgress", back_populates="university")

class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True)
    day = Column(Integer, nullable=False, unique=True)
    framework = Column(String, nullable=False)
    task_name = Column(String, nullable=False)
    description = Column(String)
    
    progress = relationship("TaskProgress", back_populates="task")

class TaskProgress(Base):
    __tablename__ = 'task_progress'
    
    id = Column(Integer, primary_key=True)
    university_id = Column(Integer, ForeignKey('universities.id'))
    task_id = Column(Integer, ForeignKey('tasks.id'))
    status = Column(String, default=TaskStatus.PENDING.value)
    updated_at = Column(DateTime, default=datetime.now)
    remarks = Column(String)
    
    university = relationship("University", back_populates="tasks")
    task = relationship("Task", back_populates="progress")

@dataclass
class ProjectTimeline:
    """Project timeline configuration"""
    start_date: datetime
    total_days: int = 50
    
    def get_date_for_day(self, day: int) -> datetime:
        return self.start_date + timedelta(days=day - 1)
    
    def get_current_day(self) -> int:
        days_passed = (datetime.now() - self.start_date).days
        return min(days_passed + 1, self.total_days)

# Task definitions based on the 50-day plan
TASK_SCHEDULE = {
    1: ("SAMARTH", "Faculty Roster - Day 1"),
    2: ("SAMARTH", "Faculty Roster - Day 2"),
    3: ("SAMARTH", "Students Documentation - Day 3"),
    4: ("SAMARTH", "Students Documentation - Day 4"),
    5: ("SAMARTH", "Financial Records - Day 5"),
    6: ("SAMARTH", "Financial Records - Day 6"),
    7: ("SAMARTH", "IPR/Patents - Day 7"),
    8: ("SAMARTH", "IPR/Patents - Day 8"),
    9: ("SAMARTH", "Publications - Day 9"),
    10: ("SAMARTH", "Publications - Day 10"),
    11: ("SAMARTH", "PhD Faculties - Day 11"),
    12: ("SAMARTH", "PhD Faculties - Day 12"),
    13: ("SAMARTH", "SAM TLR - Day 13"),
    14: ("SAMARTH", "SAM TLR - Day 14"),
    15: ("SAMARTH", "SAM TLR - Day 15"),
    16: ("SAMARTH", "SAM TLR - Day 16"),
    17: ("SAMARTH", "SAM RP - Day 17"),
    18: ("SAMARTH", "SAM RP - Day 18"),
    19: ("SAMARTH", "SAM RP - Day 19"),
    20: ("SAMARTH", "SAM RP - Day 20"),
    21: ("SAMARTH", "SAM-GO - Day 21"),
    22: ("SAMARTH", "SAM-GO - Day 22"),
    23: ("SAMARTH", "SAM-OI - Day 23"),
    24: ("SAMARTH", "SAM-OI - Day 24"),
    25: ("SAMARTH", "SAM PR - Day 25"),
    26: ("NEP", "NEP CUR - Day 26"),
    27: ("NEP", "NEP CUR - Day 27"),
    28: ("NEP", "NEP-TCH - Day 28"),
    29: ("NEP", "NEP-TCH - Day 29"),
    30: ("NEP", "NEP RES - Day 30"),
    31: ("NEP", "NEP GOV - Day 31"),
    32: ("NEP", "NEP INC - Day 32"),
    33: ("NEP", "NEP OUT - Day 33"),
    34: ("NEP", "NEP-DIG - Day 34"),
    35: ("NEP", "NEP SUS - Day 35"),
    36: ("AEGIS", "AEG-BI - Day 36"),
    37: ("AEGIS", "AEG-BI - Day 37"),
    38: ("AEGIS", "AEG-EDU - Day 38"),
    39: ("AEGIS", "AEG-EDU - Day 39"),
    40: ("AEGIS", "AEG-GRD - Day 40"),
    41: ("AEGIS", "AEG-INC - Day 41"),
    42: ("AEGIS", "AEG-SAF - Day 42"),
    43: ("IKS", "IKS-CUR - Day 43"),
    44: ("IKS", "IKS-CUR - Day 44"),
    45: ("IKS", "IKS-TCH - Day 45"),
    46: ("IKS", "IKS-TCH - Day 46"),
    47: ("IKS", "IKS-RES - Day 47"),
    48: ("IKS", "IKS-GOV - Day 48"),
    49: ("IKS", "IKS-OUT - Day 49"),
    50: ("IKS", "IKS-DIG - Day 50"),
}
