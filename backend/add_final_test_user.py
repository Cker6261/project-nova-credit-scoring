import requests

# Add one more test user to verify scrolling
test_user = {
    'name': 'Final Test User', 
    'age': 32,
    'occupation': 'Data Scientist',
    'income_level': 'high',
    'monthly_income': 95000,
    'education_level': 5,
    'upi_transactions': 50,
    'rent_paid_on_time': True,
    'utility_bills_paid': True,
    'has_savings_account': True,
    'employment_months': 36
}

response = requests.post('http://localhost:8000/calculate_score', json=test_user)
result = response.json()
print(f'Added: {result["message"]}')
print(f'User ID: {result["user_id"]}, Score: {result["score"]}')

# Get current total
users = requests.get('http://localhost:8000/get_users').json()
print(f'Total users: {len(users)}')
print('Last 3 users:')
for user in users[-3:]:
    print(f'  ID: {user["id"]}, Name: {user["name"]}, Score: {user["credit_score"]}')
