"""
ML Model Training Script for Project Nova
Generates training data and trains the credit scoring model
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

def generate_training_data(n_samples=1000):
    """Generate synthetic training data"""
    np.random.seed(42)
    
    # Generate realistic demographic and financial data
    data = {
        'age': np.random.randint(18, 65, n_samples),
        'monthly_income': np.random.choice([15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000, 65000, 70000, 75000, 80000, 85000, 90000, 95000], n_samples),
        'education_level': np.random.randint(1, 6, n_samples),
        'upi_transactions': np.random.randint(5, 100, n_samples),
        'rent_paid_on_time': np.random.choice([0, 1], n_samples, p=[0.2, 0.8]),
        'utility_bills_paid': np.random.choice([0, 1], n_samples, p=[0.15, 0.85]),
        'has_savings_account': np.random.choice([0, 1], n_samples, p=[0.3, 0.7]),
        'employment_months': np.random.randint(1, 120, n_samples),
        'income_level': np.random.choice(['low', 'medium', 'high'], n_samples, p=[0.3, 0.5, 0.2])
    }
    
    df = pd.DataFrame(data)
    
    # Generate realistic credit scores based on features
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

def prepare_features(df):
    """Prepare features for training"""
    # Encode categorical variables
    le_income = LabelEncoder()
    df['income_level_encoded'] = le_income.fit_transform(df['income_level'])
    
    # Feature columns
    feature_cols = [
        'age', 'monthly_income', 'education_level', 'upi_transactions',
        'rent_paid_on_time', 'utility_bills_paid', 'has_savings_account',
        'employment_months', 'income_level_encoded'
    ]
    
    X = df[feature_cols]
    y = df['credit_score']
    
    return X, y, le_income, feature_cols

def train_model():
    """Train the credit scoring model"""
    print("Generating training data...")
    df = generate_training_data(1000)
    
    print("Preparing features...")
    X, y, le_income, feature_cols = prepare_features(df)
    
    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest model...")
    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate model
    train_pred = model.predict(X_train)
    test_pred = model.predict(X_test)
    
    train_r2 = r2_score(y_train, train_pred)
    test_r2 = r2_score(y_test, test_pred)
    train_rmse = np.sqrt(mean_squared_error(y_train, train_pred))
    test_rmse = np.sqrt(mean_squared_error(y_test, test_pred))
    
    print(f"\nModel Performance:")
    print(f"Training R² Score: {train_r2:.3f}")
    print(f"Testing R² Score: {test_r2:.3f}")
    print(f"Training RMSE: {train_rmse:.2f}")
    print(f"Testing RMSE: {test_rmse:.2f}")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': feature_cols,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print(f"\nFeature Importance:")
    print(feature_importance)
    
    # Save model
    model_data = {
        'model': model,
        'label_encoders': {'income_level': le_income},
        'feature_names': feature_cols,
        'feature_importance': feature_importance
    }
    
    joblib.dump(model_data, 'credit_model.pkl')
    print(f"\nModel saved as 'credit_model.pkl'")
    
    # Save training data as CSV
    df.to_csv('training_data.csv', index=False)
    print(f"Training data saved as 'training_data.csv'")
    
    return model, feature_importance, df

def visualize_results(df, feature_importance):
    """Create visualizations"""
    plt.figure(figsize=(15, 10))
    
    # Feature importance plot
    plt.subplot(2, 3, 1)
    sns.barplot(data=feature_importance, x='importance', y='feature')
    plt.title('Feature Importance')
    plt.xlabel('Importance')
    
    # Score distribution
    plt.subplot(2, 3, 2)
    plt.hist(df['credit_score'], bins=30, alpha=0.7, color='skyblue')
    plt.title('Credit Score Distribution')
    plt.xlabel('Credit Score')
    plt.ylabel('Frequency')
    
    # Income vs Score
    plt.subplot(2, 3, 3)
    plt.scatter(df['monthly_income'], df['credit_score'], alpha=0.6)
    plt.title('Income vs Credit Score')
    plt.xlabel('Monthly Income')
    plt.ylabel('Credit Score')
    
    # UPI transactions vs Score
    plt.subplot(2, 3, 4)
    plt.scatter(df['upi_transactions'], df['credit_score'], alpha=0.6, color='orange')
    plt.title('UPI Transactions vs Credit Score')
    plt.xlabel('UPI Transactions per Month')
    plt.ylabel('Credit Score')
    
    # Payment behavior vs Score
    plt.subplot(2, 3, 5)
    payment_score = df['rent_paid_on_time'].astype(int) + df['utility_bills_paid'].astype(int)
    plt.boxplot([df[payment_score == 0]['credit_score'],
                df[payment_score == 1]['credit_score'],
                df[payment_score == 2]['credit_score']])
    plt.title('Payment Behavior vs Credit Score')
    plt.xlabel('Number of Bills Paid On Time')
    plt.ylabel('Credit Score')
    plt.xticks([1, 2, 3], ['0', '1', '2'])
    
    # Age vs Score
    plt.subplot(2, 3, 6)
    plt.scatter(df['age'], df['credit_score'], alpha=0.6, color='green')
    plt.title('Age vs Credit Score')
    plt.xlabel('Age')
    plt.ylabel('Credit Score')
    
    plt.tight_layout()
    plt.savefig('model_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("Visualizations saved as 'model_analysis.png'")

if __name__ == "__main__":
    print("Project Nova - Credit Scoring Model Training")
    print("=" * 50)
    
    model, feature_importance, df = train_model()
    
    try:
        visualize_results(df, feature_importance)
    except Exception as e:
        print(f"Note: Visualization requires matplotlib and seaborn. Install with: pip install matplotlib seaborn")
        print(f"Error: {e}")
    
    print("\nTraining completed successfully!")
    print("Files generated:")
    print("- credit_model.pkl (trained model)")
    print("- training_data.csv (training dataset)")
    print("- model_analysis.png (visualizations, if matplotlib available)")
