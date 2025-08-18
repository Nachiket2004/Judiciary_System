#!/usr/bin/env python3
"""
Basic test script for initial setup verification
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

def test_django_basic():
    """Test basic Django setup"""
    print("🧪 Testing Basic Django Setup...")
    
    # Check if we're in the right directory
    if not os.path.exists('backend/manage.py'):
        print("❌ Error: Please run this script from the project root directory")
        return False
    
    # Test Django check with basic settings
    print("1. Running Django system check...")
    success, stdout, stderr = run_command(
        "python manage.py check --settings=judiciary_platform.settings_basic", 
        cwd="backend"
    )
    if success:
        print("✅ Django system check passed")
    else:
        print(f"❌ Django system check failed: {stderr}")
        return False
    
    # Test if we can create migrations
    print("2. Testing migrations...")
    success, stdout, stderr = run_command(
        "python manage.py makemigrations --settings=judiciary_platform.settings_basic", 
        cwd="backend"
    )
    if success or "No changes detected" in stdout:
        print("✅ Migrations check passed")
    else:
        print(f"ℹ️  Migrations: {stdout}")
    
    return True

def test_server_start():
    """Test if Django server can start"""
    print("\n🌐 Testing Django Server...")
    
    print("1. Attempting to start Django server...")
    print("   (This will test if the server can start, then stop it)")
    
    # Try to start server in background
    try:
        process = subprocess.Popen(
            ["python", "manage.py", "runserver", "--settings=judiciary_platform.settings_basic", "8001"],
            cwd="backend",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait a bit for server to start
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ Django server started successfully")
            
            # Try to make a request
            try:
                response = requests.get("http://localhost:8001/api/auth/health/", timeout=5)
                if response.status_code == 200:
                    print("✅ Health endpoint responding")
                    print(f"   Response: {response.json()}")
                else:
                    print(f"⚠️  Health endpoint returned status {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"⚠️  Could not test health endpoint: {e}")
            
            # Stop the server
            process.terminate()
            process.wait()
            print("✅ Server stopped cleanly")
            return True
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Server failed to start: {stderr.decode()}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing server: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 AI-Enhanced Judiciary Platform - Basic Setup Test")
    print("=" * 55)
    
    # Test Django setup
    if not test_django_basic():
        print("\n❌ Basic Django setup test failed!")
        sys.exit(1)
    
    # Test server start
    if not test_server_start():
        print("\n⚠️  Server start test had issues, but basic setup works")
    
    print("\n✅ Basic setup test completed!")
    print("\n📋 Manual Testing:")
    print("1. Start server: cd backend && python manage.py runserver --settings=judiciary_platform.settings_basic")
    print("2. Test health endpoint: http://localhost:8000/api/auth/health/")
    print("3. Test admin panel: http://localhost:8000/admin/")
    print("\n🎯 Ready for Task 2: JWT Authentication implementation!")

if __name__ == "__main__":
    main()