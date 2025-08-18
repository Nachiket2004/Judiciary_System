# Setup and Testing Instructions

## 🚀 Quick Setup Guide

### 1. Backend Setup (Django)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env file with your database credentials

# Run Django checks
python manage.py check

# Create and run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### 2. Frontend Setup (Flutter)

```bash
# Navigate to frontend directory
cd frontend

# Get Flutter dependencies
flutter pub get

# Run Flutter app (web)
flutter run -d chrome

# Or run on mobile device/emulator
flutter run
```

### 3. Test the Setup

```bash
# From project root directory
python test_setup.py
```

## 🧪 Testing Checklist

### Backend Tests
- [ ] Django system check passes
- [ ] Migrations work correctly
- [ ] Development server starts
- [ ] Health endpoint responds: `http://localhost:8000/api/auth/health/`
- [ ] Admin panel accessible: `http://localhost:8000/admin/`

### Frontend Tests
- [ ] Flutter dependencies install successfully
- [ ] App compiles without errors
- [ ] App runs on web browser
- [ ] API connection test works
- [ ] UI displays correctly

## 🔧 Troubleshooting

### Common Backend Issues

1. **MySQL Connection Error**
   ```
   Solution: Check MySQL is running and credentials in .env are correct
   ```

2. **Migration Errors**
   ```bash
   # Reset migrations if needed
   python manage.py migrate --fake-initial
   ```

3. **Port Already in Use**
   ```bash
   # Use different port
   python manage.py runserver 8001
   ```

### Common Frontend Issues

1. **Flutter Dependencies Error**
   ```bash
   flutter clean
   flutter pub get
   ```

2. **Web Build Issues**
   ```bash
   flutter config --enable-web
   flutter create . --platforms web
   ```

3. **API Connection Issues**
   - Check Django server is running
   - Verify CORS settings in Django
   - Check API URLs in `api_constants.dart`

## 📊 Expected Results

### Successful Backend Test
```
🧪 Testing Django Backend Setup...
1. Running Django system check...
✅ Django system check passed
2. Testing migrations...
✅ Migrations check passed

🌐 Testing API Endpoints...
✅ Health endpoint working
   Response: {'status': 'healthy', 'message': 'Django backend is running successfully!', 'version': '1.0.0'}
✅ /api/auth/test/ - Status: 200
✅ /admin/ - Status: 200
```

### Successful Frontend Test
- Flutter app opens in browser
- "API Connection Successful!" message appears
- All UI components render correctly
- No console errors

## 🎯 Next Steps After Successful Testing

1. **Task 2**: Implement JWT Authentication
2. **Task 3**: Create Lawyer Profile APIs
3. **Task 4**: DigiLocker Integration
4. Continue with remaining tasks...

## 📞 Support

If you encounter issues:
1. Check the error messages carefully
2. Verify all dependencies are installed
3. Ensure database is running
4. Check environment variables
5. Review the troubleshooting section above