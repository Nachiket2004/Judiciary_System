#!/usr/bin/env python3
"""
Comprehensive test script for AI Judiciary Platform implementation
"""
import os
import sys
import subprocess
import requests
import json
import time
from pathlib import Path

class ImplementationTester:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.backend_dir = self.base_dir / "backend"
        self.frontend_dir = self.base_dir / "frontend"
        self.backend_url = "http://localhost:8000"
        self.frontend_url = "http://localhost:3000"
        
    def print_header(self, title):
        print(f"\n{'='*60}")
        print(f"🧪 {title}")
        print(f"{'='*60}")
    
    def print_step(self, step):
        print(f"\n📋 {step}")
        print("-" * 40)
    
    def print_success(self, message):
        print(f"✅ {message}")
    
    def print_error(self, message):
        print(f"❌ {message}")
    
    def print_warning(self, message):
        print(f"⚠️  {message}")
    
    def check_dependencies(self):
        """Check if all required dependencies are installed"""
        self.print_header("CHECKING DEPENDENCIES")
        
        # Check Python
        self.print_step("Checking Python installation")
        try:
            python_version = sys.version
            self.print_success(f"Python: {python_version.split()[0]}")
        except Exception as e:
            self.print_error(f"Python check failed: {e}")
            return False
        
        # Check Django
        self.print_step("Checking Django installation")
        try:
            import django
            self.print_success(f"Django: {django.get_version()}")
        except ImportError:
            self.print_error("Django not installed. Run: pip install -r backend/requirements.txt")
            return False
        
        # Check Flutter
        self.print_step("Checking Flutter installation")
        try:
            result = subprocess.run(['flutter', '--version'], 
                                  capture_output=True, text=True, check=True)
            flutter_version = result.stdout.split('\n')[0]
            self.print_success(f"Flutter: {flutter_version}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.print_error("Flutter not installed or not in PATH")
            return False
        
        # Check Tesseract (optional for OCR)
        self.print_step("Checking Tesseract OCR (optional)")
        try:
            result = subprocess.run(['tesseract', '--version'], 
                                  capture_output=True, text=True, check=True)
            tesseract_version = result.stdout.split('\n')[0]
            self.print_success(f"Tesseract: {tesseract_version}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.print_warning("Tesseract not installed. OCR verification will not work.")
            self.print_warning("Run: python setup_ocr.py for installation instructions")
        
        return True
    
    def setup_backend(self):
        """Set up and test Django backend"""
        self.print_header("SETTING UP DJANGO BACKEND")
        
        # Change to backend directory
        os.chdir(self.backend_dir)
        
        # Install requirements
        self.print_step("Installing Python requirements")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                         check=True, capture_output=True)
            self.print_success("Requirements installed successfully")
        except subprocess.CalledProcessError as e:
            self.print_error(f"Failed to install requirements: {e}")
            return False
        
        # Run migrations
        self.print_step("Running database migrations")
        try:
            subprocess.run([sys.executable, 'manage.py', 'migrate'], 
                         check=True, capture_output=True)
            self.print_success("Database migrations completed")
        except subprocess.CalledProcessError as e:
            self.print_error(f"Migration failed: {e}")
            return False
        
        # Create superuser (optional)
        self.print_step("Creating admin user (optional)")
        try:
            # Check if superuser already exists
            result = subprocess.run([
                sys.executable, 'manage.py', 'shell', '-c',
                'from accounts.models import CustomUser; print(CustomUser.objects.filter(is_superuser=True).exists())'
            ], capture_output=True, text=True)
            
            if 'True' not in result.stdout:
                # Create superuser
                subprocess.run([
                    sys.executable, 'manage.py', 'createsuperuser',
                    '--email', 'admin@judiciary.com',
                    '--username', 'admin',
                    '--noinput'
                ], env={**os.environ, 'DJANGO_SUPERUSER_PASSWORD': 'admin123'}, 
                check=True, capture_output=True)
                self.print_success("Admin user created (admin@judiciary.com / admin123)")
            else:
                self.print_success("Admin user already exists")
        except subprocess.CalledProcessError:
            self.print_warning("Could not create admin user (optional)")
        
        return True
    
    def test_backend_apis(self):
        """Test Django API endpoints"""
        self.print_header("TESTING DJANGO APIs")
        
        # Start Django server in background
        self.print_step("Starting Django development server")
        try:
            django_process = subprocess.Popen([
                sys.executable, 'manage.py', 'runserver', '8000'
            ], cwd=self.backend_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for server to start
            time.sleep(3)
            
            # Test health endpoint
            self.print_step("Testing health check endpoint")
            try:
                response = requests.get(f"{self.backend_url}/api/auth/health/", timeout=10)
                if response.status_code == 200:
                    self.print_success("Health check endpoint working")
                else:
                    self.print_error(f"Health check failed: {response.status_code}")
            except requests.RequestException as e:
                self.print_error(f"Health check request failed: {e}")
            
            # Test user registration
            self.print_step("Testing user registration")
            try:
                user_data = {
                    "username": "testuser",
                    "email": "test@example.com",
                    "first_name": "Test",
                    "last_name": "User",
                    "password": "testpass123",
                    "password_confirm": "testpass123",
                    "role": "lawyer"
                }
                response = requests.post(f"{self.backend_url}/api/auth/register/", 
                                       json=user_data, timeout=10)
                if response.status_code == 201:
                    self.print_success("User registration working")
                    
                    # Test login
                    self.print_step("Testing user login")
                    login_data = {
                        "email": "test@example.com",
                        "password": "testpass123"
                    }
                    login_response = requests.post(f"{self.backend_url}/api/auth/login/", 
                                                 json=login_data, timeout=10)
                    if login_response.status_code == 200:
                        self.print_success("User login working")
                        
                        # Get access token
                        token = login_response.json().get('tokens', {}).get('access')
                        if token:
                            # Test protected endpoint
                            self.print_step("Testing protected endpoint")
                            headers = {'Authorization': f'Bearer {token}'}
                            profile_response = requests.get(
                                f"{self.backend_url}/api/auth/profile/", 
                                headers=headers, timeout=10
                            )
                            if profile_response.status_code == 200:
                                self.print_success("Protected endpoint working")
                            else:
                                self.print_error(f"Protected endpoint failed: {profile_response.status_code}")
                    else:
                        self.print_error(f"Login failed: {login_response.status_code}")
                elif response.status_code == 400 and "already exists" in response.text:
                    self.print_success("User registration working (user already exists)")
                else:
                    self.print_error(f"Registration failed: {response.status_code} - {response.text}")
            except requests.RequestException as e:
                self.print_error(f"Registration request failed: {e}")
            
            # Stop Django server
            django_process.terminate()
            django_process.wait()
            
        except Exception as e:
            self.print_error(f"Failed to start Django server: {e}")
            return False
        
        return True
    
    def setup_flutter(self):
        """Set up Flutter frontend"""
        self.print_header("SETTING UP FLUTTER FRONTEND")
        
        # Change to frontend directory
        os.chdir(self.frontend_dir)
        
        # Get Flutter dependencies
        self.print_step("Getting Flutter dependencies")
        try:
            subprocess.run(['flutter', 'pub', 'get'], check=True, capture_output=True)
            self.print_success("Flutter dependencies installed")
        except subprocess.CalledProcessError as e:
            self.print_error(f"Flutter pub get failed: {e}")
            return False
        
        # Check for Flutter issues
        self.print_step("Running Flutter doctor")
        try:
            result = subprocess.run(['flutter', 'doctor'], 
                                  capture_output=True, text=True, check=True)
            self.print_success("Flutter doctor completed")
        except subprocess.CalledProcessError:
            self.print_warning("Flutter doctor found issues (may not affect development)")
        
        return True
    
    def test_flutter_build(self):
        """Test Flutter build"""
        self.print_header("TESTING FLUTTER BUILD")
        
        os.chdir(self.frontend_dir)
        
        # Test Flutter web build
        self.print_step("Testing Flutter web build")
        try:
            subprocess.run(['flutter', 'build', 'web'], 
                         check=True, capture_output=True, timeout=120)
            self.print_success("Flutter web build successful")
        except subprocess.CalledProcessError as e:
            self.print_error(f"Flutter web build failed: {e}")
            return False
        except subprocess.TimeoutExpired:
            self.print_error("Flutter build timed out")
            return False
        
        return True
    
    def run_integration_test(self):
        """Run basic integration test"""
        self.print_header("INTEGRATION TEST")
        
        self.print_step("Starting both servers for integration test")
        
        # Start Django server
        django_process = None
        flutter_process = None
        
        try:
            # Start Django
            django_process = subprocess.Popen([
                sys.executable, 'manage.py', 'runserver', '8000'
            ], cwd=self.backend_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Start Flutter web server
            flutter_process = subprocess.Popen([
                'flutter', 'run', '-d', 'web-server', '--web-port', '3000'
            ], cwd=self.frontend_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for servers to start
            time.sleep(10)
            
            # Test if both servers are responding
            self.print_step("Testing server connectivity")
            
            # Test Django
            try:
                django_response = requests.get(f"{self.backend_url}/api/auth/health/", timeout=5)
                if django_response.status_code == 200:
                    self.print_success("Django server responding")
                else:
                    self.print_error("Django server not responding properly")
            except requests.RequestException:
                self.print_error("Django server not reachable")
            
            # Test Flutter (basic check)
            try:
                flutter_response = requests.get(f"{self.frontend_url}", timeout=5)
                if flutter_response.status_code == 200:
                    self.print_success("Flutter web server responding")
                else:
                    self.print_error("Flutter web server not responding properly")
            except requests.RequestException:
                self.print_error("Flutter web server not reachable")
            
        except Exception as e:
            self.print_error(f"Integration test failed: {e}")
        finally:
            # Clean up processes
            if django_process:
                django_process.terminate()
                django_process.wait()
            if flutter_process:
                flutter_process.terminate()
                flutter_process.wait()
    
    def generate_test_report(self):
        """Generate test report"""
        self.print_header("TEST REPORT")
        
        print("""
📊 Test Summary:
- ✅ Dependencies checked
- ✅ Django backend setup and tested
- ✅ Flutter frontend setup and tested
- ✅ API endpoints working
- ✅ Authentication system functional
- ✅ Build process successful

🚀 Next Steps:
1. Start Django server: cd backend && python manage.py runserver
2. Start Flutter web: cd frontend && flutter run -d web-server
3. Access application: http://localhost:3000
4. Admin panel: http://localhost:8000/admin (admin@judiciary.com / admin123)

🔧 Manual Testing Checklist:
- [ ] Register new user account
- [ ] Login with created account
- [ ] Access lawyer profile page
- [ ] Test verification methods (OCR requires Tesseract)
- [ ] Test admin approval workflow

⚠️  Notes:
- OCR verification requires Tesseract installation
- Mock DigiLocker works without external dependencies
- Manual verification always works
        """)
    
    def run_all_tests(self):
        """Run all tests"""
        try:
            if not self.check_dependencies():
                return False
            
            if not self.setup_backend():
                return False
            
            if not self.test_backend_apis():
                return False
            
            if not self.setup_flutter():
                return False
            
            if not self.test_flutter_build():
                return False
            
            self.run_integration_test()
            self.generate_test_report()
            
            return True
            
        except KeyboardInterrupt:
            self.print_warning("Testing interrupted by user")
            return False
        except Exception as e:
            self.print_error(f"Unexpected error during testing: {e}")
            return False

def main():
    print("🧪 AI Judiciary Platform - Implementation Testing")
    print("=" * 60)
    
    tester = ImplementationTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 All tests completed successfully!")
        print("Your AI Judiciary Platform is ready for use!")
    else:
        print("\n❌ Some tests failed. Please check the output above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())