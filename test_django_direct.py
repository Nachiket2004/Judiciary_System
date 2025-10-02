#!/usr/bin/env python3
"""
Direct Django test without subprocess
"""
import os
import sys
from pathlib import Path

# Add backend to Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'judiciary_platform.settings')

def test_django_import():
    """Test Django imports"""
    print("🔍 Testing Django imports...")
    
    try:
        import django
        print(f"✅ Django {django.get_version()} imported successfully")
        
        # Setup Django
        django.setup()
        print("✅ Django setup completed")
        
        return True
    except Exception as e:
        print(f"❌ Django import failed: {e}")
        return False

def test_models():
    """Test model imports"""
    print("\n🔍 Testing model imports...")
    
    try:
        from accounts.models import CustomUser
        print("✅ CustomUser model imported")
        
        from lawyers.models import Lawyer, LawyerVerification, Case
        print("✅ Lawyer models imported")
        
        return True
    except Exception as e:
        print(f"❌ Model import failed: {e}")
        return False

def test_views():
    """Test view imports"""
    print("\n🔍 Testing view imports...")
    
    try:
        from accounts.views import register, login
        print("✅ Auth views imported")
        
        from lawyers.views import verify_lawyer_ocr, verify_lawyer_mock_digilocker
        print("✅ Lawyer views imported")
        
        return True
    except Exception as e:
        print(f"❌ View import failed: {e}")
        return False

def test_services():
    """Test service imports"""
    print("\n🔍 Testing service imports...")
    
    try:
        from lawyers.services import OCRVerificationService, MockDigiLockerService
        print("✅ Verification services imported")
        
        return True
    except Exception as e:
        print(f"❌ Service import failed: {e}")
        return False

def test_urls():
    """Test URL configuration"""
    print("\n🔍 Testing URL configuration...")
    
    try:
        from django.urls import reverse
        from django.test import Client
        
        # Test URL patterns
        client = Client()
        
        # Test health endpoint
        response = client.get('/api/auth/health/')
        print(f"✅ Health endpoint: {response.status_code}")
        
        return True
    except Exception as e:
        print(f"❌ URL test failed: {e}")
        return False

def main():
    print("⚡ Direct Django Test")
    print("=" * 30)
    
    tests = [
        test_django_import,
        test_models,
        test_views,
        test_services,
        test_urls
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
    
    print(f"\n📋 Test Results: {sum(results)}/{len(results)} passed")
    
    if all(results):
        print("🎉 All Django tests passed!")
        print("\n🚀 Django backend is ready!")
        print("Next steps:")
        print("1. Run migrations: py manage.py migrate")
        print("2. Start server: py manage.py runserver")
    else:
        print("❌ Some tests failed")
    
    return 0 if all(results) else 1

if __name__ == "__main__":
    sys.exit(main())