# 🧪 AI Judiciary Platform - Testing Guide

## 📋 **Quick Setup Verification**

### **1. Check Project Structure**
```
✅ Backend Structure:
├── backend/
│   ├── manage.py ✅
│   ├── requirements.txt ✅
│   ├── accounts/ ✅
│   ├── lawyers/ ✅
│   └── judiciary_platform/ ✅

✅ Frontend Structure:
├── frontend/
│   ├── pubspec.yaml ✅
│   ├── lib/ ✅
│   └── web/ ✅
```

### **2. Dependencies Check**
- ✅ **Django 5.2.5** - Available via `py -c "import django; print(django.get_version())"`
- ✅ **Flutter Project** - pubspec.yaml configured with all dependencies
- ⚠️  **Python Command** - Use `py` instead of `python` on Windows
- ⚠️  **Tesseract OCR** - Optional for OCR verification (run `python setup_ocr.py`)

---

## 🚀 **Manual Testing Steps**

### **Step 1: Start Django Backend**
```bash
# Navigate to backend directory
cd backend

# Install dependencies (if not done)
py -m pip install -r requirements.txt

# Run migrations
py manage.py migrate

# Create admin user (optional)
py manage.py createsuperuser

# Start Django server
py manage.py runserver
```

**Expected Result:** Server starts at `http://localhost:8000`

### **Step 2: Test Django APIs**
Open browser and test these endpoints:

1. **Health Check:** `http://localhost:8000/api/auth/health/`
   - Expected: `{"status": "healthy", "message": "Django backend is running successfully!"}`

2. **Admin Panel:** `http://localhost:8000/admin/`
   - Expected: Django admin login page

3. **API Endpoints Available:**
   - `POST /api/auth/register/` - User registration
   - `POST /api/auth/login/` - User login
   - `GET /api/auth/profile/` - User profile (requires auth)
   - `POST /api/lawyers/verify/ocr/` - OCR verification
   - `POST /api/lawyers/verify/mock-digilocker/` - Mock DigiLocker
   - `POST /api/lawyers/verify/manual/` - Manual verification

### **Step 3: Start Flutter Frontend**
```bash
# Navigate to frontend directory
cd frontend

# Get Flutter dependencies
flutter pub get

# Start Flutter web server
flutter run -d web-server --web-port 3000
```

**Expected Result:** Flutter app starts at `http://localhost:3000`

### **Step 4: Test Flutter App**
1. **Access App:** Open `http://localhost:3000`
2. **Registration:** Create a new lawyer account
3. **Login:** Sign in with created account
4. **Profile:** Access lawyer profile page
5. **Verification:** Test verification methods

---

## 🧪 **Feature Testing Checklist**

### **Authentication System** ✅
- [ ] User registration with role selection
- [ ] User login with JWT tokens
- [ ] Token refresh mechanism
- [ ] Protected route access
- [ ] Logout functionality

### **Lawyer Profile Management** ✅
- [ ] Profile creation and editing
- [ ] Profile information display
- [ ] Case statistics calculation
- [ ] Win rate visualization

### **Multi-Method Verification System** ✅
- [ ] **OCR Verification:**
  - [ ] File upload (PDF, JPG, PNG)
  - [ ] Text extraction (requires Tesseract)
  - [ ] Lawyer detail parsing
  - [ ] Confidence scoring
  - [ ] Admin review queue

- [ ] **Mock DigiLocker:**
  - [ ] OAuth simulation
  - [ ] Mock certificate generation
  - [ ] Auto-approval process
  - [ ] Demo mode indicators

- [ ] **Manual Verification:**
  - [ ] Form-based data entry
  - [ ] Field validation
  - [ ] Admin review submission

### **Admin Workflow** ✅
- [ ] Pending verifications list
- [ ] Verification approval/rejection
- [ ] Admin comments system
- [ ] Email notifications (configured)

---

## 🔧 **Troubleshooting**

### **Common Issues:**

#### **Python Command Not Found**
```bash
# Use 'py' instead of 'python' on Windows
py --version
py manage.py runserver
```

#### **Django Import Errors**
```bash
# Install requirements
py -m pip install -r backend/requirements.txt

# Check Django installation
py -c "import django; print(django.get_version())"
```

#### **Flutter Not Found**
```bash
# Check Flutter installation
flutter --version

# If not installed, download from: https://flutter.dev/docs/get-started/install
```

#### **OCR Not Working**
```bash
# Install Tesseract OCR
python setup_ocr.py

# Or manually install:
# Windows: https://github.com/UB-Mannheim/tesseract/wiki
# Ubuntu: sudo apt-get install tesseract-ocr
```

#### **Database Issues**
```bash
# Reset database
cd backend
del db.sqlite3
py manage.py migrate
py manage.py createsuperuser
```

---

## 📊 **Test Results Expected**

### **Backend Tests:**
- ✅ Django server starts without errors
- ✅ Health endpoint returns 200 OK
- ✅ User registration works
- ✅ JWT authentication functional
- ✅ Verification APIs respond correctly

### **Frontend Tests:**
- ✅ Flutter app builds successfully
- ✅ Web server starts on port 3000
- ✅ Login/registration screens load
- ✅ API calls work with authentication
- ✅ Verification interface functional

### **Integration Tests:**
- ✅ Frontend can communicate with backend
- ✅ Authentication flow works end-to-end
- ✅ File upload works (if Tesseract installed)
- ✅ Mock DigiLocker simulation works
- ✅ Admin workflow functional

---

## 🎯 **Success Criteria**

Your implementation is working correctly if:

1. **Django server starts** without import errors
2. **Flutter app builds** and runs on web
3. **User registration/login** works end-to-end
4. **At least one verification method** works (Mock DigiLocker always works)
5. **Admin panel** is accessible
6. **API endpoints** return proper responses

---

## 🚀 **Next Steps After Testing**

Once testing is complete:

1. **Continue Implementation:**
   - Task 5: Case Management APIs
   - Task 6: Lawyer Search Interface
   - Task 7: Data Visualization
   - Task 8-9: AI Prediction System

2. **Deploy for Demo:**
   - Use Railway/Heroku for backend
   - Use Netlify/Vercel for frontend
   - Configure production database

3. **Academic Presentation:**
   - Demonstrate multi-method verification
   - Show practical approach to DigiLocker constraints
   - Highlight technical competencies achieved

---

## 📞 **Support**

If you encounter issues:

1. **Check this guide** for troubleshooting steps
2. **Verify dependencies** are installed correctly
3. **Use `py` command** instead of `python` on Windows
4. **Check console output** for specific error messages
5. **Test one component at a time** (backend first, then frontend)

**Remember:** The Mock DigiLocker verification always works and doesn't require external dependencies - perfect for demonstrations! 🎉