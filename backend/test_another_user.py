import requests
import json

# Test adding another new user
new_user = {
    'name': 'Another Test User',
    'age': 35,
    'occupation': 'Marketing Manager',
    'income_level': 'medium',
    'monthly_income': 55000,
    'education_level': 4,
    'upi_transactions': 35,
    'rent_paid_on_time': True,
    'utility_bills_paid': True,
    'has_savings_account': True,
    'employment_months': 48
}

response = requests.post('http://localhost:8000/calculate_score', json=new_user)
result = response.json()
print('New User Added!')
print(f'Name: {new_user["name"]}')
print(f'Score: {result["score"]}')
print(f'Risk Category: {result["risk_category"]}')
print(f'User ID: {result["user_id"]}')
print(f'Message: {result["message"]}')

# Check total users
users_response = requests.get('http://localhost:8000/get_users')
users = users_response.json()
print(f'\nTotal users now: {len(users)}')
