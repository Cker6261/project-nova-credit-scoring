"""
Basic tests for Project Nova API
Run with: python test_api.py
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health_endpoint():
    """Test the health check endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        print("✅ Health check passed")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_get_users():
    """Test getting all users"""
    try:
        response = requests.get(f"{BASE_URL}/get_users")
        assert response.status_code == 200
        users = response.json()
        assert len(users) > 0
        print(f"✅ Get users passed - {len(users)} users found")
        return True
    except Exception as e:
        print(f"❌ Get users failed: {e}")
        return False

def test_get_specific_user():
    """Test getting a specific user"""
    try:
        response = requests.get(f"{BASE_URL}/get_user/1")
        assert response.status_code == 200
        user = response.json()
        assert "name" in user
        assert "credit_score" in user
        print(f"✅ Get specific user passed - {user['name']}")
        return True
    except Exception as e:
        print(f"❌ Get specific user failed: {e}")
        return False

def test_calculate_score():
    """Test credit score calculation"""
    try:
        test_user = {
            "name": "Test User",
            "age": 28,
            "occupation": "Software Engineer",
            "income_level": "high",
            "monthly_income": 75000,
            "education_level": 4,
            "upi_transactions": 45,
            "rent_paid_on_time": True,
            "utility_bills_paid": True,
            "has_savings_account": True,
            "employment_months": 24
        }
        
        response = requests.post(f"{BASE_URL}/calculate_score", json=test_user)
        assert response.status_code == 200
        result = response.json()
        assert "score" in result
        assert "explanations" in result
        assert 300 <= result["score"] <= 900
        print(f"✅ Calculate score passed - Score: {result['score']}")
        return True
    except Exception as e:
        print(f"❌ Calculate score failed: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("🧪 Running Project Nova API Tests")
    print("=" * 40)
    
    tests = [
        test_health_endpoint,
        test_get_users,
        test_get_specific_user,
        test_calculate_score
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("⚠️ Some tests failed. Check the backend server.")

if __name__ == "__main__":
    run_all_tests()
