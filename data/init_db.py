import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import DatabaseManager

def initialize_database():
    """Initialize the database with all required data"""
    print("Initializing mahaSTRIDE database...")
    db = DatabaseManager()
    db.initialize_data()
    print("Database initialized successfully!")

if __name__ == "__main__":
    initialize_database()
