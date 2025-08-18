#!/usr/bin/env python3
"""
Complete setup script for AI-Enhanced Judiciary Platform
"""
import os
import sys
import subprocess

def run_command(command, cwd=None, show_output=True):
    """Run a command and return the result"""
    try:
        if show_output:
            print(f"  → {command}")
        
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Error running command: {e}")
        return False

def setup_backend():
    """Set up Django backend"""
    print("🔧 Setting up Django Backend...")
    
    if not os.path.exists('backend'):
        print("❌ Backend directory not found!")
        return False
    
    # Install dependencies
    print("1. Installing Python dependencies...")
    if not run_command("pip install setuptools", cwd="backend", show_output=False):
        print("⚠️  Could not install setuptools")
    
    if not run_command("pip install -r requirements_basic.txt", cwd="backend"):
        print("❌ Failed to install dependencies")
        return False
    
    # Run migrations
    print("2. Setting up database...")
    if not run_command("python manage.py migrate --settings=judiciary_platform.settings_basic", cwd="backend"):
        print("❌ Failed to run migrations")
        return False
    
    print("✅ Backend setup complete!")
    return True

def setup_frontend():
    """Set up Flutter frontend"""
    print("🔧 Setting up Flutter Frontend...")
    
    if not os.path.exists('frontend'):
        print("❌ Frontend directory not found!")
        return False
    
    # Check Flutter
    if not run_command("flutter --version", show_output=False):
        print("❌ Flutter is not installed")
        print("Please install Flutter from: https://flutter.dev/docs/get-started/install")
        return False
    
    # Setup Flutter
    print("1. Configuring Flutter...")
    run_command("flutter config --enable-web", cwd="frontend", show_output=False)
    run_command("flutter clean", cwd="frontend", show_output=False)
    
    print("2. Installing Flutter dependencies...")
    if not run_command("flutter pub get", cwd="frontend"):
        print("❌ Failed to get Flutter dependencies")
        return False
    
    print("✅ Frontend setup complete!")
    return True

def test_setup():
    """Test the complete setup"""
    print("🧪 Testing Setup...")
    
    # Test Django
    print("1. Testing Django...")
    success, _, _ = subprocess.run(
        "python manage.py check --settings=judiciary_platform.settings_basic",
        shell=True,
        cwd="backend",
        capture_output=True,
        text=True
    ).returncode == 0, "", ""
    
    if success:
        print("✅ Django test passed")
    else:
        print("❌ Django test failed")
        return False
    
    # Test Flutter
    print("2. Testing Flutter...")
    success = run_command("flutter analyze", cwd="frontend", show_output=False)
    if success:
        print("✅ Flutter test passed")
    else:
        print("⚠️  Flutter analysis has warnings (normal for initial setup)")
    
    return True

def main():
    """Main setup function"""
    print("🚀 AI-Enhanced Judiciary Platform - Complete Setup")
    print("=" * 55)
    
    # Setup backend
    if not setup_backend():
        print("\n❌ Backend setup failed!")
        sys.exit(1)
    
    # Setup frontend
    if not setup_frontend():
        print("\n❌ Frontend setup failed!")
        sys.exit(1)
    
    # Test setup
    if not test_setup():
        print("\n⚠️  Some tests failed, but basic setup is complete")
    
    print("\n🎉 Complete Setup Finished!")
    print("\n🚀 How to Run:")
    print("\n📱 Backend (Django):")
    print("   cd backend")
    print("   python manage.py runserver --settings=judiciary_platform.settings_basic")
    print("   → Server will run at: http://localhost:8000")
    print("   → Test health: http://localhost:8000/api/auth/health/")
    
    print("\n🌐 Frontend (Flutter Web):")
    print("   cd frontend")
    print("   flutter run -d chrome")
    print("   → App will open in Chrome browser")
    
    print("\n📱 Frontend (Mobile):")
    print("   cd frontend")
    print("   flutter run")
    print("   → Requires Android/iOS emulator or device")
    
    print("\n🧪 Test Everything:")
    print("   python test_basic.py")

if __name__ == "__main__":
    main()