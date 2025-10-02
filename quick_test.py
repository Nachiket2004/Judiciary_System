#!/usr/bin/env python3
"""
Quick test script to verify basic setup
"""
import os
import sys
import subprocess
from pathlib import Path

def test_django_setup():
    """Quick Django setup test"""
    print("🔍 Testing Django Setup...")
    
    backend_dir = Path(__file__).parent / "backend"
    os.chdir(backend_dir)
    
    try:
        # Test Django import
        result = subprocess.run([
            sys.executable, '-c', 
            'import django; print(f"Django {django.get_version()} imported successfully")'
        ], capture_output=True, text=True, check=True)
        print(f"✅ {result.stdout.strip()}")
        
        # Test Django project
        result = subprocess.run([
            sys.executable, 'manage.py', 'check'
        ], capture_output=True, text=True, check=True)
        print("✅ Django project check passed")
        
        # Test migrations
        result = subprocess.run([
            sys.executable, 'manage.py', 'showmigrations'
        ], capture_output=True, text=True, check=True)
        print("✅ Django migrations check passed")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Django test failed: {e}")
        print(f"   Error output: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Django test error: {e}")
        return False

def test_flutter_setup():
    """Quick Flutter setup test"""
    print("\n🔍 Testing Flutter Setup...")
    
    frontend_dir = Path(__file__).parent / "frontend"
    os.chdir(frontend_dir)
    
    try:
        # Test Flutter version
        result = subprocess.run([
            'flutter', '--version'
        ], capture_output=True, text=True, check=True)
        print("✅ Flutter is installed")
        
        # Test Flutter analyze
        result = subprocess.run([
            'flutter', 'analyze'
        ], capture_output=True, text=True, check=True)
        print("✅ Flutter analyze passed")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Flutter test failed: {e}")
        return False
    except FileNotFoundError:
        print("❌ Flutter not found in PATH")
        return False
    except Exception as e:
        print(f"❌ Flutter test error: {e}")
        return False

def test_dependencies():
    """Test key dependencies"""
    print("\n🔍 Testing Key Dependencies...")
    
    # Test Python packages
    packages = [
        'django',
        'djangorestframework', 
        'djangorestframework_simplejwt',
        'django_cors_headers',
        'pytesseract',
        'PIL'
    ]
    
    for package in packages:
        try:
            __import__(package)
            print(f"✅ {package} imported successfully")
        except ImportError:
            print(f"❌ {package} not installed")
    
    # Test Tesseract (optional)
    try:
        result = subprocess.run(['tesseract', '--version'], 
                              capture_output=True, text=True, check=True)
        print("✅ Tesseract OCR is installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Tesseract OCR not installed (OCR verification will not work)")

def main():
    print("⚡ Quick Implementation Test")
    print("=" * 40)
    
    django_ok = test_django_setup()
    flutter_ok = test_flutter_setup()
    test_dependencies()
    
    print("\n📋 Test Summary:")
    print(f"Django Backend: {'✅ Ready' if django_ok else '❌ Issues'}")
    print(f"Flutter Frontend: {'✅ Ready' if flutter_ok else '❌ Issues'}")
    
    if django_ok and flutter_ok:
        print("\n🎉 Basic setup looks good!")
        print("\n🚀 To start the application:")
        print("1. Backend: cd backend && python manage.py runserver")
        print("2. Frontend: cd frontend && flutter run -d web-server")
        return 0
    else:
        print("\n❌ Some issues found. Please check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())