"""
Database management for Project Nova
Handles SQLite operations and user data management
"""

import sqlite3
import os
from typing import List, Optional, Dict, Any
from schema import UserResponse
import random

class DatabaseManager:
    def __init__(self, db_path: str = "nova_credit.db"):
        self.db_path = db_path
        
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def initialize_database(self):
        """Initialize database with tables and seed data"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            occupation TEXT NOT NULL,
            income_level TEXT NOT NULL,
            monthly_income REAL NOT NULL,
            education_level INTEGER NOT NULL,
            upi_transactions INTEGER NOT NULL,
            rent_paid_on_time BOOLEAN NOT NULL,
            utility_bills_paid BOOLEAN NOT NULL,
            has_savings_account BOOLEAN NOT NULL,
            employment_months INTEGER NOT NULL,
            credit_score INTEGER NOT NULL,
            risk_category TEXT NOT NULL
        )
        ''')
        
        # Check if we need to seed data
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        
        if count == 0:
            self._seed_database(cursor)
        
        conn.commit()
        conn.close()
    
    def _seed_database(self, cursor):
        """Seed database with dummy test users"""
        seed_users = [
            ("Arjun Sharma", 28, "Software Engineer", "high", 85000, 4, 45, True, True, True, 24, 750, "Low Risk"),
            ("Priya Patel", 32, "Teacher", "medium", 45000, 5, 25, True, True, True, 60, 680, "Medium Risk"),
            ("Rahul Kumar", 26, "Delivery Partner", "low", 25000, 2, 80, False, True, False, 8, 520, "High Risk"),
            ("Sneha Gupta", 29, "Marketing Manager", "high", 75000, 4, 35, True, True, True, 36, 720, "Low Risk"),
            ("Amit Singh", 35, "Shopkeeper", "medium", 35000, 3, 50, True, False, True, 48, 600, "Medium Risk"),
            ("Kavya Reddy", 24, "Data Analyst", "medium", 55000, 4, 40, True, True, True, 18, 695, "Low Risk"),
            ("Ravi Nair", 40, "Auto Driver", "low", 20000, 1, 60, False, False, False, 72, 480, "High Risk"),
            ("Ananya Das", 27, "Nurse", "medium", 42000, 4, 30, True, True, True, 30, 665, "Medium Risk"),
            ("Kiran Joshi", 31, "Bank Employee", "high", 65000, 4, 25, True, True, True, 84, 740, "Low Risk"),
            ("Pooja Verma", 25, "Freelancer", "low", 30000, 3, 70, False, True, False, 12, 550, "High Risk"),
            ("Suresh Agarwal", 45, "Small Business Owner", "medium", 50000, 2, 40, True, False, True, 120, 620, "Medium Risk"),
            ("Deepika Iyer", 30, "HR Manager", "high", 70000, 5, 20, True, True, True, 42, 715, "Low Risk"),
            ("Vikram Yadav", 28, "Sales Executive", "medium", 48000, 3, 55, True, True, False, 24, 640, "Medium Risk"),
            ("Meera Kapoor", 33, "Graphic Designer", "medium", 40000, 4, 35, True, True, True, 36, 675, "Medium Risk"),
            ("Rohit Malhotra", 26, "Student/Part-time", "low", 15000, 3, 90, False, False, False, 6, 450, "High Risk")
        ]
        
        cursor.executemany('''
        INSERT INTO users (name, age, occupation, income_level, monthly_income, education_level, 
                          upi_transactions, rent_paid_on_time, utility_bills_paid, has_savings_account,
                          employment_months, credit_score, risk_category)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_users)
    
    def get_all_users(self) -> List[UserResponse]:
        """Get all users from database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        
        users = []
        for row in rows:
            user = UserResponse(
                id=row[0],
                name=row[1],
                age=row[2],
                occupation=row[3],
                income_level=row[4],
                monthly_income=row[5],
                education_level=row[6],
                upi_transactions=row[7],
                rent_paid_on_time=bool(row[8]),
                utility_bills_paid=bool(row[9]),
                has_savings_account=bool(row[10]),
                employment_months=row[11],
                credit_score=row[12],
                risk_category=row[13]
            )
            users.append(user)
        
        conn.close()
        return users
    
    def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        """Get specific user by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return None
        
        user = UserResponse(
            id=row[0],
            name=row[1],
            age=row[2],
            occupation=row[3],
            income_level=row[4],
            monthly_income=row[5],
            education_level=row[6],
            upi_transactions=row[7],
            rent_paid_on_time=bool(row[8]),
            utility_bills_paid=bool(row[9]),
            has_savings_account=bool(row[10]),
            employment_months=row[11],
            credit_score=row[12],
            risk_category=row[13]
        )
        
        conn.close()
        return user
    
    def add_user(self, user_data: Dict[str, Any]) -> int:
        """Add new user to database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO users (name, age, occupation, income_level, monthly_income, education_level,
                          upi_transactions, rent_paid_on_time, utility_bills_paid, has_savings_account,
                          employment_months, credit_score, risk_category)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_data['name'], user_data['age'], user_data['occupation'],
            user_data['income_level'], user_data['monthly_income'], user_data['education_level'],
            user_data['upi_transactions'], user_data['rent_paid_on_time'], user_data['utility_bills_paid'],
            user_data['has_savings_account'], user_data['employment_months'],
            user_data['credit_score'], user_data['risk_category']
        ))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return user_id
    
    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> bool:
        """Update existing user in database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        UPDATE users SET 
            name = ?, age = ?, occupation = ?, income_level = ?, monthly_income = ?,
            education_level = ?, upi_transactions = ?, rent_paid_on_time = ?,
            utility_bills_paid = ?, has_savings_account = ?, employment_months = ?,
            credit_score = ?, risk_category = ?
        WHERE id = ?
        ''', (
            user_data['name'], user_data['age'], user_data['occupation'],
            user_data['income_level'], user_data['monthly_income'], user_data['education_level'],
            user_data['upi_transactions'], user_data['rent_paid_on_time'], user_data['utility_bills_paid'],
            user_data['has_savings_account'], user_data['employment_months'],
            user_data['credit_score'], user_data['risk_category'], user_id
        ))
        
        updated = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return updated

    def user_exists_by_name(self, name: str) -> Optional[int]:
        """Check if user exists by name and return user ID if found"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM users WHERE name = ?", (name,))
        row = cursor.fetchone()
        
        conn.close()
        return row[0] if row else None
