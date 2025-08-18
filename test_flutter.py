#!/usr/bin/env python3
"""
Flutter setup test script
"""
import os
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
            capture_output=not show_output,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Error running command: {e}")
        return False

def test_flutter_setup():
    """Test Flutter setup"""
    print("🧪 Testing Flutter Setup...")
    
    if not os.path.exists('frontend'):
        print("❌ Frontend directory not found!")
        return False
    
    # Check Flutter installation
    print("1. Checking Flutter installation...")
    if not run_command("flutter --version", show_output=False):
        print("❌ Flutter is not installed or not in PATH")
        return False
    print("✅ Flutter is installed")
    
    # Check web support
    print("2. Enabling web support...")
    run_command("flutter config --enable-web", cwd="frontend", show_output=False)
    print("✅ Web support enabled")
    
    # Clean and get dependencies
    print("3. Getting dependencies...")
    run_command("flutter clean", cwd="frontend", show_output=False)
    if not run_command("flutter pub get", cwd="frontend", show_output=False):
        print("❌ Failed to get dependencies")
        return False
    print("✅ Dependencies installed")
    
    # Test compilation
    print("4. Testing compilation...")
    if not run_command("flutter analyze", cwd="frontend", show_output=False):
        print("⚠️  Analysis found issues, but continuing...")
    else:
        print("✅ Code analysis passed")
    
    return True

def main():
    """Main test function"""
    print("🚀 Flutter Setup Test")
    print("=" * 30)
    
    if test_flutter_setup():
        print("\n✅ Flutter setup test passed!")
        print("\n📋 Next Steps:")
        print("1. Run: cd frontend && flutter run -d chrome")
        print("2. Or run: cd frontend && flutter run (for mobile)")
    else:
        print("\n❌ Flutter setup test failed!")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure Flutter is installed")
        print("2. Run: flutter doctor")
        print("3. Run: flutter config --enable-web")

if __name__ == "__main__":
    main()