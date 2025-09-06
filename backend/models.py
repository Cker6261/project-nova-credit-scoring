"""
ML Model for Credit Scoring
Implements the core scoring algorithm using scikit-learn
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import joblib
import os
from typing import List, Tuple, Dict, Any
from schema import UserData

class CreditScoreModel:
    def __init__(self, model_path: str = "credit_model.pkl"):
        self.model_path = model_path
        self.model = None
        self.label_encoders = {}
        self.feature_names = [
            'age', 'monthly_income', 'education_level', 'upi_transactions',
            'rent_paid_on_time', 'utility_bills_paid', 'has_savings_account',
            'employment_months', 'income_level_encoded'
        ]
    
    def generate_training_data(self) -> pd.DataFrame:
        """Generate synthetic training data for the model"""
        np.random.seed(42)  # For reproducible results
        
        # Generate 500 synthetic records
        n_samples = 500
        
        data = {
            'age': np.random.randint(18, 65, n_samples),
            'monthly_income': np.random.choice([15000, 25000, 35000, 45000, 55000, 65000, 75000, 85000, 95000], n_samples),
            'education_level': np.random.randint(1, 6, n_samples),
            'upi_transactions': np.random.randint(5, 100, n_samples),
            'rent_paid_on_time': np.random.choice([0, 1], n_samples, p=[0.2, 0.8]),
            'utility_bills_paid': np.random.choice([0, 1], n_samples, p=[0.15, 0.85]),
            'has_savings_account': np.random.choice([0, 1], n_samples, p=[0.3, 0.7]),
            'employment_months': np.random.randint(1, 120, n_samples),
            'income_level': np.random.choice(['low', 'medium', 'high'], n_samples, p=[0.3, 0.5, 0.2])
        }
        
        df = pd.DataFrame(data)
        
        # Encode income level
        le = LabelEncoder()
        df['income_level_encoded'] = le.fit_transform(df['income_level'])
        self.label_encoders['income_level'] = le
        
        # Generate target credit scores based on features (with some logic)
        scores = []
        for idx, row in df.iterrows():
            base_score = 400
            
            # Income contribution (0-150 points)
            if row['monthly_income'] >= 70000:
                base_score += 150
            elif row['monthly_income'] >= 50000:
                base_score += 100
            elif row['monthly_income'] >= 30000:
                base_score += 50
            
            # Education contribution (0-80 points)
            base_score += row['education_level'] * 15
            
            # Payment history (0-120 points)
            if row['rent_paid_on_time']:
                base_score += 60
            if row['utility_bills_paid']:
                base_score += 60
            
            # UPI activity (0-60 points)
            if row['upi_transactions'] >= 50:
                base_score += 60
            elif row['upi_transactions'] >= 30:
                base_score += 40
            elif row['upi_transactions'] >= 15:
                base_score += 20
            
            # Employment stability (0-80 points)
            if row['employment_months'] >= 60:
                base_score += 80
            elif row['employment_months'] >= 24:
                base_score += 50
            elif row['employment_months'] >= 12:
                base_score += 30
            
            # Savings account (0-30 points)
            if row['has_savings_account']:
                base_score += 30
            
            # Age factor (slight boost for stable age)
            if 25 <= row['age'] <= 45:
                base_score += 20
            
            # Add some random noise
            base_score += np.random.randint(-30, 31)
            
            # Cap between 300-900
            base_score = max(300, min(900, base_score))
            scores.append(base_score)
        
        df['credit_score'] = scores
        return df
    
    def train_model(self):
        """Train the Random Forest model"""
        # Generate training data
        df = self.generate_training_data()
        
        # Prepare features and target
        X = df[self.feature_names]
        y = df['credit_score']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train Random Forest model
        self.model = RandomForestRegressor(
            n_estimators=100,
            random_state=42,
            max_depth=10,
            min_samples_split=5
        )
        
        self.model.fit(X_train, y_train)
        
        # Save model and encoders
        model_data = {
            'model': self.model,
            'label_encoders': self.label_encoders,
            'feature_names': self.feature_names
        }
        joblib.dump(model_data, self.model_path)
        
        # Print model performance
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        print(f"Model trained successfully!")
        print(f"Training R² Score: {train_score:.3f}")
        print(f"Testing R² Score: {test_score:.3f}")
    
    def load_model(self):
        """Load trained model from file"""
        if os.path.exists(self.model_path):
            model_data = joblib.load(self.model_path)
            self.model = model_data['model']
            self.label_encoders = model_data['label_encoders']
            self.feature_names = model_data['feature_names']
            print("Model loaded successfully!")
            return True
        return False
    
    def load_or_train_model(self):
        """Load existing model or train new one"""
        if not self.load_model():
            print("No existing model found. Training new model...")
            self.train_model()
    
    def prepare_features(self, user_data: UserData) -> np.ndarray:
        """Prepare user data for model prediction"""
        # Encode income level
        if 'income_level' not in self.label_encoders:
            # Fallback encoding if not loaded
            income_mapping = {'low': 0, 'medium': 1, 'high': 2}
            income_encoded = income_mapping.get(user_data.income_level.value, 1)
        else:
            income_encoded = self.label_encoders['income_level'].transform([user_data.income_level.value])[0]
        
        # Prepare feature vector
        features = np.array([
            user_data.age,
            user_data.monthly_income,
            user_data.education_level,
            user_data.upi_transactions,
            int(user_data.rent_paid_on_time),
            int(user_data.utility_bills_paid),
            int(user_data.has_savings_account),
            user_data.employment_months,
            income_encoded
        ]).reshape(1, -1)
        
        return features
    
    def predict_score(self, features: np.ndarray, user_data: UserData) -> Tuple[float, List[str]]:
        """Predict credit score and generate explanations"""
        if self.model is None:
            raise ValueError("Model not loaded or trained")
        
        # Get prediction
        score = self.model.predict(features)[0]
        
        # Ensure score is in valid range
        score = max(300, min(900, score))
        
        # Generate explanations
        explanations = self._generate_explanations(user_data, score)
        
        return score, explanations
    
    def _generate_explanations(self, user_data: UserData, score: float) -> List[str]:
        """Generate human-readable explanations for the score"""
        explanations = []
        
        # Income analysis
        if user_data.monthly_income >= 70000:
            explanations.append("✅ High monthly income positively impacts your score")
        elif user_data.monthly_income >= 50000:
            explanations.append("✅ Good monthly income contributes to your score")
        elif user_data.monthly_income < 30000:
            explanations.append("⚠️ Lower income slightly reduces your score")
        
        # Payment history
        if user_data.rent_paid_on_time and user_data.utility_bills_paid:
            explanations.append("✅ Excellent payment history boosts your score")
        elif user_data.rent_paid_on_time or user_data.utility_bills_paid:
            explanations.append("✅ Good payment history helps your score")
        else:
            explanations.append("⚠️ Payment history needs improvement")
        
        # Digital activity
        if user_data.upi_transactions >= 50:
            explanations.append("✅ High digital payment activity shows financial engagement")
        elif user_data.upi_transactions >= 30:
            explanations.append("✅ Good digital payment activity")
        elif user_data.upi_transactions < 15:
            explanations.append("💡 Increase digital payments to improve score")
        
        # Education
        if user_data.education_level >= 4:
            explanations.append("✅ Higher education level positively affects score")
        elif user_data.education_level <= 2:
            explanations.append("💡 Education level considered in scoring")
        
        # Employment stability
        if user_data.employment_months >= 60:
            explanations.append("✅ Long employment history demonstrates stability")
        elif user_data.employment_months >= 24:
            explanations.append("✅ Good employment stability")
        elif user_data.employment_months < 12:
            explanations.append("⚠️ Short employment history affects score")
        
        # Savings account
        if user_data.has_savings_account:
            explanations.append("✅ Having a savings account shows financial responsibility")
        else:
            explanations.append("💡 Consider opening a savings account")
        
        # Overall score interpretation
        if score >= 750:
            explanations.append("🎉 Excellent credit score! You qualify for the best rates")
        elif score >= 650:
            explanations.append("👍 Good credit score with favorable lending options")
        elif score >= 550:
            explanations.append("📈 Fair score with room for improvement")
        else:
            explanations.append("📊 Building credit score - focus on payment history and stability")
        
        return explanations
