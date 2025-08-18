#!/usr/bin/env python3
"""
Quick setup script for the AI-Enhanced Judiciary Platform
"""
import os
import sys
import subprocess

def run_command(command, cwd=None, show_output=True):
    """Run a command and return the result"""
    try:
        if show_output:
            print(f"Running: {command}")
        
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
    
    # Install Python dependencies
    print("1. Installing Python dependencies...")
    success = False
    
    # Try basic requirements first
    if run_command("pip install -r requirements_basic.txt", cwd="backend"):
        success = True
        print("✅ Basic dependencies installed")
    elif run_command("pip install setuptools", cwd="backend") and run_command("pip install -r requirements_basic.txt", cwd="backend"):
        success = True
        print("✅ Dependencies installed after setuptools fix")
    else:
        print("❌ Failed to install dependencies")
        return False
    
    # Run migrations with basic settings
    print("2. Creating database tables...")
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
    
    # Check if Flutter is installed
    if not run_command("flutter --version", show_output=False):
        print("❌ Flutter is not installed or not in PATH")
        print("Please install Flutter from: https://flutter.dev/docs/get-started/install")
        return False
    
    # Enable web support
    print("1. Enabling Flutter web support...")
    run_command("flutter config --enable-web", cwd="frontend", show_output=False)
    
    # Clean and get dependencies
    print("2. Cleaning and getting Flutter dependencies...")
    run_command("flutter clean", cwd="frontend", show_output=False)
    if not run_command("flutter pub get", cwd="frontend"):
        print("❌ Failed to get Flutter dependencies")
        return False
    
    print("✅ Frontend setup complete!")
    return True

def main():
    """Main setup function"""
    print("🚀 AI-Enhanced Judiciary Platform - Quick Setup")
    print("=" * 50)
    
    # Setup backend
    if not setup_backend():
        print("\n❌ Backend setup failed!")
        sys.exit(1)
    
    # Setup frontend
    if not setup_frontend():
        print("\n❌ Frontend setup failed!")
        sys.exit(1)
    
    print("\n🎉 Setup Complete!")
    print("\n🚀 Next Steps:")
    print("1. Start Django server:")
    print("   cd backend")
    print("   python manage.py runserver --settings=judiciary_platform.settings_basic")
    print("\n2. Start Flutter app (in new terminal):")
    print("   cd frontend")
    print("   flutter run -d chrome")
    print("\n3. Test the setup:")
    print("   python test_setup.py")
    print("\n📝 Note: Using basic settings without JWT for initial testing")

if __name__ == "__main__":
    main()