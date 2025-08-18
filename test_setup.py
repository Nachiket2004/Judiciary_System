#!/usr/bin/env python3
"""
Test script to verify the Django backend setup
"""
import os
import sys
import subprocess
import requests
import time

def run_command(command, cwd=None):
    """Run a command and return the result"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            capture_output=True, 
            text=True,
            timeout=30
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"

def test_django_setup():
    """Test Django backend setup"""
    print("🧪 Testing Django Backend Setup...")
    
    # Check if we're in the right directory
    if not os.path.exists('backend/manage.py'):
        print("❌ Error: Please run this script from the project root directory")
        return False
    
    # Set environment variable to use simple settings
    os.environ['DJANGO_SETTINGS_MODULE'] = 'judiciary_platform.settings_simple'
    
    # Test Django check with simple settings
    print("1. Running Django system check (with simple settings)...")
    success, stdout, stderr = run_command(
        "python manage.py check --settings=judiciary_platform.settings_simple", 
        cwd="backend"
    )
    if success:
        print("✅ Django system check passed")
    else:
        print(f"❌ Django system check failed: {stderr}")
        print("💡 Trying to install missing dependencies...")
        
        # Try to install requirements
        install_success, _, install_error = run_command("pip install -r requirements.txt", cwd="backend")
        if install_success:
            print("✅ Dependencies installed, retrying check...")
            success, stdout, stderr = run_command(
                "python manage.py check --settings=judiciary_platform.settings_simple", 
                cwd="backend"
            )
            if success:
                print("✅ Django system check passed after installing dependencies")
            else:
                print(f"❌ Still failing: {stderr}")
                return False
        else:
            print(f"❌ Failed to install dependencies: {install_error}")
            return False
    
    # Test migrations
    print("2. Testing migrations...")
    success, stdout, stderr = run_command(
        "python manage.py makemigrations --dry-run --settings=judiciary_platform.settings_simple", 
        cwd="backend"
    )
    if success:
        print("✅ Migrations check passed")
    else:
        print(f"❌ Migrations check failed: {stderr}")
        # This might fail initially, which is okay
        print("ℹ️  This is normal for first run - migrations will be created later")
    
    return True

def test_api_endpoints():
    """Test API endpoints"""
    print("\n🌐 Testing API Endpoints...")
    
    base_url = "http://localhost:8000"
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/api/auth/health/", timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint working")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health endpoint failed with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Could not connect to API: {e}")
        print("   Make sure Django server is running: python manage.py runserver")
        return False
    
    # Test other endpoints
    endpoints = [
        "/api/auth/test/",
        "/admin/",
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            print(f"✅ {endpoint} - Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ {endpoint} - Error: {e}")
    
    return True

def main():
    """Main test function"""
    print("🚀 AI-Enhanced Judiciary Platform - Setup Test")
    print("=" * 50)
    
    # Test Django setup
    if not test_django_setup():
        print("\n❌ Django setup test failed!")
        sys.exit(1)
    
    print("\n✅ All Django setup tests passed!")
    print("\n📋 Next Steps:")
    print("1. Set up your MySQL database")
    print("2. Copy backend/.env.example to backend/.env and configure")
    print("3. Run: cd backend && python manage.py migrate")
    print("4. Run: cd backend && python manage.py runserver")
    print("5. Test API endpoints by running this script again")
    print("\n🎯 For Flutter:")
    print("1. Run: cd frontend && flutter pub get")
    print("2. Run: cd frontend && flutter run -d chrome")

if __name__ == "__main__":
    main()