"""
Project Nova Demo Script
Demonstrates the credit scoring functionality
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def print_banner():
    print("=" * 60)
    print("🌟 PROJECT NOVA - EQUITABLE CREDIT SCORING ENGINE")
    print("=" * 60)
    print()

def demo_score_calculation():
    """Demonstrate score calculation for different user profiles"""
    
    demo_users = [
        {
            "name": "Sarah Chen",
            "age": 28,
            "occupation": "Software Engineer",
            "income_level": "high",
            "monthly_income": 85000,
            "education_level": 5,
            "upi_transactions": 50,
            "rent_paid_on_time": True,
            "utility_bills_paid": True,
            "has_savings_account": True,
            "employment_months": 36
        },
        {
            "name": "Raj Patel",
            "age": 32,
            "occupation": "Small Business Owner",
            "income_level": "medium",
            "monthly_income": 45000,
            "education_level": 3,
            "upi_transactions": 75,
            "rent_paid_on_time": True,
            "utility_bills_paid": False,
            "has_savings_account": True,
            "employment_months": 48
        },
        {
            "name": "Maya Singh",
            "age": 24,
            "occupation": "Delivery Partner",
            "income_level": "low",
            "monthly_income": 25000,
            "education_level": 2,
            "upi_transactions": 90,
            "rent_paid_on_time": False,
            "utility_bills_paid": True,
            "has_savings_account": False,
            "employment_months": 8
        }
    ]
    
    print("🎯 CREDIT SCORE CALCULATIONS")
    print("-" * 40)
    
    for i, user in enumerate(demo_users, 1):
        print(f"\n👤 Demo {i}: {user['name']}")
        print(f"   Occupation: {user['occupation']}")
        print(f"   Income: ₹{user['monthly_income']:,}/month ({user['income_level']})")
        print(f"   UPI Transactions: {user['upi_transactions']}/month")
        print(f"   Payment History: Rent {'✅' if user['rent_paid_on_time'] else '❌'}, Utilities {'✅' if user['utility_bills_paid'] else '❌'}")
        
        try:
            response = requests.post(f"{BASE_URL}/calculate_score", json=user)
            if response.status_code == 200:
                result = response.json()
                score = result['score']
                
                # Determine risk level
                if score >= 750:
                    risk_level = "🟢 LOW RISK"
                elif score >= 650:
                    risk_level = "🟡 MEDIUM RISK"
                else:
                    risk_level = "🔴 HIGH RISK"
                
                print(f"   💳 CREDIT SCORE: {score}/900 ({risk_level})")
                print(f"   📝 KEY FACTORS:")
                
                for explanation in result['explanations'][:3]:  # Show top 3 factors
                    print(f"      • {explanation}")
                    
            else:
                print(f"   ❌ Error calculating score: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Connection error: {e}")
        
        time.sleep(1)  # Pause for readability

def demo_user_portfolio():
    """Demonstrate bank dashboard functionality"""
    print("\n\n🏦 BANK DASHBOARD - CUSTOMER PORTFOLIO")
    print("-" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/get_users")
        if response.status_code == 200:
            users = response.json()
            
            # Calculate portfolio stats
            total_users = len(users)
            low_risk = sum(1 for u in users if u['risk_category'] == 'Low Risk')
            medium_risk = sum(1 for u in users if u['risk_category'] == 'Medium Risk')
            high_risk = sum(1 for u in users if u['risk_category'] == 'High Risk')
            avg_score = sum(u['credit_score'] for u in users) / total_users
            
            print(f"\n📊 PORTFOLIO SUMMARY:")
            print(f"   Total Customers: {total_users}")
            print(f"   Average Score: {avg_score:.0f}")
            print(f"   🟢 Low Risk: {low_risk} ({low_risk/total_users*100:.1f}%)")
            print(f"   🟡 Medium Risk: {medium_risk} ({medium_risk/total_users*100:.1f}%)")
            print(f"   🔴 High Risk: {high_risk} ({high_risk/total_users*100:.1f}%)")
            
            print(f"\n👥 TOP CUSTOMERS (by score):")
            sorted_users = sorted(users, key=lambda x: x['credit_score'], reverse=True)
            
            for i, user in enumerate(sorted_users[:5], 1):
                risk_emoji = {"Low Risk": "🟢", "Medium Risk": "🟡", "High Risk": "🔴"}
                print(f"   {i}. {user['name']:<15} | Score: {user['credit_score']} | {risk_emoji[user['risk_category']]} {user['risk_category']}")
            
        else:
            print(f"   ❌ Error fetching users: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Connection error: {e}")

def check_server():
    """Check if the server is running"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    print_banner()
    
    # Check server connection
    if not check_server():
        print("❌ Backend server is not running!")
        print("Please start the server with: cd backend && python main.py")
        print("Then run this demo again.")
        return
    
    print("✅ Connected to Project Nova backend")
    
    # Run demonstrations
    demo_score_calculation()
    demo_user_portfolio()
    
    print("\n\n" + "=" * 60)
    print("🎉 DEMO COMPLETE!")
    print("💡 Try the web interface at: http://localhost:3000")
    print("📚 API docs available at: http://localhost:8000/docs")
    print("=" * 60)

if __name__ == "__main__":
    main()
