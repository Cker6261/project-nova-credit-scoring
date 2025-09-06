import requests
import json

try:
    # Get all users to verify our new user was added
    response = requests.get('http://localhost:8000/get_users')
    users = response.json()
    
    print(f'Total users in database: {len(users)}')
    print('\nLast few users:')
    for user in users[-3:]:  # Show last 3 users
        print(f'ID: {user["id"]}, Name: {user["name"]}, Score: {user["credit_score"]}, Risk: {user["risk_category"]}')
        
    # Test updating the same user
    print('\n--- Testing update functionality ---')
    test_user_update = {
        'name': 'Test User New',  # Same name as before
        'age': 29,  # Changed age
        'occupation': 'Senior Software Developer',  # Changed occupation
        'income_level': 'high',
        'monthly_income': 90000,  # Increased income
        'education_level': 5,  # Changed education
        'upi_transactions': 60,  # Increased transactions
        'rent_paid_on_time': True,
        'utility_bills_paid': True,
        'has_savings_account': True,
        'employment_months': 30  # Increased employment
    }
    
    update_response = requests.post('http://localhost:8000/calculate_score', json=test_user_update)
    print('Update Status Code:', update_response.status_code)
    update_result = update_response.json()
    print('Updated Score:', update_result['score'])
    print('Message:', update_result['message'])
    
    # Check users again
    response = requests.get('http://localhost:8000/get_users')
    users = response.json()
    print(f'\nTotal users after update: {len(users)}')
    
    # Find our test user
    test_user = next((u for u in users if u['name'] == 'Test User New'), None)
    if test_user:
        print(f'Updated User - ID: {test_user["id"]}, Age: {test_user["age"]}, Occupation: {test_user["occupation"]}, Score: {test_user["credit_score"]}')
    
except Exception as e:
    print('Error:', e)
