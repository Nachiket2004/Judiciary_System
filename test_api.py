#!/usr/bin/env python3
"""
API Testing Script for AI Judiciary Platform
"""
import requests
import json
import time

class APITester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.access_token = None
    
    def test_health(self):
        """Test health endpoint"""
        print("🔍 Testing health endpoint...")
        try:
            response = self.session.get(f"{self.base_url}/api/auth/health/")
            if response.status_code == 200:
                print("✅ Health endpoint working")
                print(f"   Response: {response.json()}")
                return True
            else:
                print(f"❌ Health endpoint failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Health endpoint error: {e}")
            return False
    
    def test_registration(self):
        """Test user registration"""
        print("\n🔍 Testing user registration...")
        
        user_data = {
            "username": "testlawyer",
            "email": "test@lawyer.com",
            "first_name": "Test",
            "last_name": "Lawyer",
            "password": "testpass123",
            "password_confirm": "testpass123",
            "role": "lawyer",
            "phone_number": "+1234567890"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/auth/register/",
                json=user_data
            )
            
            if response.status_code == 201:
                print("✅ User registration successful")
                data = response.json()
                self.access_token = data.get('tokens', {}).get('access')
                print(f"   User: {data.get('user', {}).get('email')}")
                return True
            elif response.status_code == 400 and "already exists" in response.text:
                print("✅ User already exists (registration working)")
                return True
            else:
                print(f"❌ Registration failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Registration error: {e}")
            return False
    
    def test_login(self):
        """Test user login"""
        print("\n🔍 Testing user login...")
        
        login_data = {
            "email": "test@lawyer.com",
            "password": "testpass123"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/auth/login/",
                json=login_data
            )
            
            if response.status_code == 200:
                print("✅ User login successful")
                data = response.json()
                self.access_token = data.get('tokens', {}).get('access')
                print(f"   User: {data.get('user', {}).get('email')}")
                return True
            else:
                print(f"❌ Login failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
    
    def test_protected_endpoint(self):
        """Test protected endpoint with JWT"""
        print("\n🔍 Testing protected endpoint...")
        
        if not self.access_token:
            print("❌ No access token available")
            return False
        
        headers = {'Authorization': f'Bearer {self.access_token}'}
        
        try:
            response = self.session.get(
                f"{self.base_url}/api/auth/profile/",
                headers=headers
            )
            
            if response.status_code == 200:
                print("✅ Protected endpoint working")
                data = response.json()
                print(f"   User profile: {data.get('user', {}).get('email')}")
                return True
            else:
                print(f"❌ Protected endpoint failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Protected endpoint error: {e}")
            return False
    
    def test_mock_digilocker(self):
        """Test mock DigiLocker verification"""
        print("\n🔍 Testing Mock DigiLocker verification...")
        
        if not self.access_token:
            print("❌ No access token available")
            return False
        
        headers = {'Authorization': f'Bearer {self.access_token}'}
        
        verification_data = {
            "name": "Test Lawyer",
            "bar_id": "TEST123",
            "specialization": "Criminal Law",
            "state": "Delhi"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/lawyers/verify/mock-digilocker/",
                json=verification_data,
                headers=headers
            )
            
            if response.status_code == 200:
                print("✅ Mock DigiLocker verification working")
                data = response.json()
                print(f"   Verification ID: {data.get('verification_id')}")
                print(f"   Demo mode: {data.get('demo_mode')}")
                return True
            else:
                print(f"❌ Mock DigiLocker failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Mock DigiLocker error: {e}")
            return False
    
    def test_manual_verification(self):
        """Test manual verification"""
        print("\n🔍 Testing Manual verification...")
        
        if not self.access_token:
            print("❌ No access token available")
            return False
        
        headers = {'Authorization': f'Bearer {self.access_token}'}
        
        verification_data = {
            "name": "Test Lawyer Manual",
            "bar_id": "MANUAL123",
            "specialization": "Civil Law",
            "experience_years": 5,
            "location": "Mumbai"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/lawyers/verify/manual/",
                json=verification_data,
                headers=headers
            )
            
            if response.status_code == 200:
                print("✅ Manual verification working")
                data = response.json()
                print(f"   Verification ID: {data.get('verification_id')}")
                print(f"   Requires admin review: {data.get('requires_admin_review')}")
                return True
            else:
                print(f"❌ Manual verification failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Manual verification error: {e}")
            return False
    
    def test_verification_status(self):
        """Test verification status endpoint"""
        print("\n🔍 Testing verification status...")
        
        if not self.access_token:
            print("❌ No access token available")
            return False
        
        headers = {'Authorization': f'Bearer {self.access_token}'}
        
        try:
            response = self.session.get(
                f"{self.base_url}/api/lawyers/verification/status/",
                headers=headers
            )
            
            if response.status_code == 200:
                print("✅ Verification status working")
                data = response.json()
                print(f"   Is verified: {data.get('is_verified')}")
                print(f"   Recent verifications: {len(data.get('recent_verifications', []))}")
                return True
            else:
                print(f"❌ Verification status failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Verification status error: {e}")
            return False
    
    def run_all_tests(self):
        """Run all API tests"""
        print("🧪 AI Judiciary Platform - API Testing")
        print("=" * 50)
        
        tests = [
            self.test_health,
            self.test_registration,
            self.test_login,
            self.test_protected_endpoint,
            self.test_mock_digilocker,
            self.test_manual_verification,
            self.test_verification_status
        ]
        
        results = []
        for test in tests:
            try:
                result = test()
                results.append(result)
                time.sleep(0.5)  # Small delay between tests
            except Exception as e:
                print(f"❌ Test failed with exception: {e}")
                results.append(False)
        
        print(f"\n📊 Test Results: {sum(results)}/{len(results)} passed")
        
        if all(results):
            print("🎉 All API tests passed!")
            print("\n✅ Your backend is working correctly!")
        else:
            print("❌ Some API tests failed")
            print("   Make sure Django server is running: py manage.py runserver")
        
        return all(results)

def main():
    print("⚡ Quick API Test")
    print("Make sure Django server is running on http://localhost:8000")
    print("Start with: cd backend && py manage.py runserver")
    print()
    
    # Wait a moment for user to start server if needed
    input("Press Enter when Django server is running...")
    
    tester = APITester()
    success = tester.run_all_tests()
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())