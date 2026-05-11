from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from typing import List, Dict, Optional
import pandas as pd
from datetime import datetime, date
import os

from models import Base, University, Task, TaskProgress, TaskStatus, TASK_SCHEDULE

class DatabaseManager:
    def __init__(self, db_path: str = "mahastride.db"):
        self.engine = create_engine(f'sqlite:///{db_path}', echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        
    def initialize_data(self):
        """Initialize universities and tasks if not already present"""
        session = self.Session()
        try:
            # Initialize Universities
            universities_data = [
                (1, "Mumbai University", "MU", "Ms Sneha, Shubham"),
                (2, "SSPU Pune", "SSPU", "Mr Jagan"),
                (3, "COEP Tech University", "COEP", "Mr Vaibhav"),
                (4, "Amravati University", "AU", "Mr Pratham"),
                (5, "Nagpur University", "NU", "Ms Anjali"),
                (6, "KBCNMU Jalgaon University", "KBCNMU", "Mr Nitish"),
                (7, "BAMU University Aurangabad", "BAMU", "Mr Atharv"),
            ]
            
            for uni_id, name, code, coordinators in universities_data:
                existing = session.query(University).filter_by(code=code).first()
                if not existing:
                    university = University(id=uni_id, name=name, code=code, coordinators=coordinators)
                    session.add(university)
            
            # Initialize Tasks
            for day, (framework, task_name) in TASK_SCHEDULE.items():
                existing = session.query(Task).filter_by(day=day).first()
                if not existing:
                    task = Task(day=day, framework=framework, task_name=task_name)
                    session.add(task)
            
            session.commit()
            
            # Initialize Task Progress for all universities
            universities = session.query(University).all()
            tasks = session.query(Task).all()
            
            for university in universities:
                for task in tasks:
                    existing = session.query(TaskProgress).filter_by(
                        university_id=university.id, task_id=task.id
                    ).first()
                    if not existing:
                        progress = TaskProgress(
                            university_id=university.id,
                            task_id=task.id,
                            status=TaskStatus.PENDING.value
                        )
                        session.add(progress)
            
            session.commit()
            
        except Exception as e:
            session.rollback()
            print(f"Error initializing data: {e}")
        finally:
            session.close()
    
    def update_task_status(self, university_code: str, day: int, status: str, remarks: str = ""):
        """Update task status for a specific university and day"""
        session = self.Session()
        try:
            university = session.query(University).filter_by(code=university_code).first()
            task = session.query(Task).filter_by(day=day).first()
            
            if university and task:
                progress = session.query(TaskProgress).filter_by(
                    university_id=university.id, task_id=task.id
                ).first()
                
                if progress:
                    progress.status = status
                    progress.updated_at = datetime.now()
                    progress.remarks = remarks
                    session.commit()
                    return True
            return False
        except Exception as e:
            session.rollback()
            print(f"Error updating task status: {e}")
            return False
        finally:
            session.close()
    
    def get_university_progress(self, university_code: str) -> pd.DataFrame:
        """Get progress DataFrame for a specific university"""
        session = self.Session()
        try:
            university = session.query(University).filter_by(code=university_code).first()
            if not university:
                return pd.DataFrame()
            
            query = session.query(
                Task.day,
                Task.framework,
                Task.task_name,
                TaskProgress.status,
                TaskProgress.updated_at,
                TaskProgress.remarks
            ).join(TaskProgress, Task.id == TaskProgress.task_id)\
             .filter(TaskProgress.university_id == university.id)\
             .order_by(Task.day)
            
            df = pd.read_sql(query.statement, session.bind)
            return df
        except Exception as e:
            print(f"Error getting university progress: {e}")
            return pd.DataFrame()
        finally:
            session.close()
    
    def get_all_universities_progress(self) -> Dict:
        """Get progress for all universities"""
        session = self.Session()
        try:
            universities = session.query(University).all()
            result = {}
            
            for uni in universities:
                progress_data = self.get_university_progress(uni.code)
                result[uni.name] = {
                    'code': uni.code,
                    'coordinators': uni.coordinators,
                    'progress': progress_data
                }
            return result
        finally:
            session.close()
    
    def get_summary_stats(self) -> pd.DataFrame:
        """Get summary statistics for all universities"""
        session = self.Session()
        try:
            stats = []
            universities = session.query(University).all()
            
            for uni in universities:
                progress = session.query(TaskProgress).filter_by(university_id=uni.id)
                total = progress.count()
                completed = progress.filter_by(status=TaskStatus.COMPLETED.value).count()
                in_progress = progress.filter_by(status=TaskStatus.IN_PROGRESS.value).count()
                pending = progress.filter_by(status=TaskStatus.PENDING.value).count()
                
                stats.append({
                    'University': uni.name,
                    'Code': uni.code,
                    'Coordinators': uni.coordinators,
                    'Total Tasks': total,
                    'Completed': completed,
                    'In Progress': in_progress,
                    'Pending': pending,
                    'Completion %': round((completed / total * 100), 2) if total > 0 else 0
                })
            
            return pd.DataFrame(stats)
        finally:
            session.close()
    
    def get_framework_wise_progress(self, university_code: str = None) -> pd.DataFrame:
        """Get framework-wise progress"""
        session = self.Session()
        try:
            query = session.query(
                Task.framework,
                University.name.label('university'),
                func.count(Task.id).label('total_tasks'),
                func.sum(func.case([(TaskProgress.status == TaskStatus.COMPLETED.value, 1)], else_=0)).label('completed')
            ).join(TaskProgress, Task.id == TaskProgress.task_id)\
             .join(University, University.id == TaskProgress.university_id)
            
            if university_code:
                query = query.filter(University.code == university_code)
            
            results = query.group_by(Task.framework, University.name).all()
            
            df = pd.DataFrame(results, columns=['framework', 'university', 'total_tasks', 'completed'])
            df['completion_percentage'] = (df['completed'] / df['total_tasks'] * 100).round(2)
            return df
        finally:
            session.close()
