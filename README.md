# 🏛️ AI-Enhanced Judiciary Platform

<div align="center">

![Platform Banner](https://img.shields.io/badge/AI--Enhanced-Judiciary%20Platform-blue?style=for-the-badge&logo=scales&logoColor=white)

**A revolutionary full-stack platform connecting users with verified lawyers and providing AI-powered case prediction services**

[![Django](https://img.shields.io/badge/Django-4.2.7-green?style=flat&logo=django)](https://djangoproject.com/)
[![Flutter](https://img.shields.io/badge/Flutter-3.10+-blue?style=flat&logo=flutter)](https://flutter.dev/)
[![Python](https://img.shields.io/badge/Python-3.9+-yellow?style=flat&logo=python)](https://python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange?style=flat&logo=mysql)](https://mysql.com/)
[![License](https://img.shields.io/badge/License-MIT-red?style=flat)](LICENSE)

[🚀 Quick Start](#-quick-start) • [📱 Features](#-features) • [🏗️ Architecture](#️-architecture) • [📖 Documentation](#-documentation) • [🤝 Contributing](#-contributing)

</div>

---

## 🌟 Overview

The **AI-Enhanced Judiciary Platform** is a cutting-edge legal technology solution that bridges the gap between legal professionals and clients while leveraging artificial intelligence to provide predictive insights for legal cases. Built with modern technologies and following industry best practices, this platform offers a comprehensive ecosystem for legal services.

### 🎯 Mission
To democratize access to legal services through technology while providing data-driven insights that enhance legal decision-making processes.

---

## 📱 Features

### 🔐 **Authentication & Security**
- **Multi-role Authentication**: Secure login system for Users, Lawyers, and Administrators
- **JWT Token Management**: Stateless authentication with refresh token rotation
- **Role-based Access Control**: Granular permissions based on user roles
- **Secure Data Storage**: Encrypted sensitive information storage

### ⚖️ **Lawyer Verification System**
- **DigiLocker Integration**: OAuth 2.0 integration with India's DigiLocker for authentic lawyer verification
- **Bar Council Certificate Validation**: Automated verification of legal credentials
- **Multi-step Verification Process**: Comprehensive validation workflow
- **Verification Audit Trail**: Complete logging of all verification attempts

### 👨‍💼 **Lawyer Management**
- **Comprehensive Profiles**: Detailed lawyer profiles with specializations, experience, and contact information
- **Case History Tracking**: Complete record of past cases with outcomes
- **Performance Analytics**: Win/loss ratios, case type distributions, and success trends
- **Interactive Dashboards**: Visual representation of lawyer performance metrics

### 🔍 **Advanced Search & Discovery**
- **Multi-criteria Search**: Filter by name, specialization, location, experience, and success rate
- **Intelligent Ranking**: AI-powered relevance scoring for search results
- **Geolocation Support**: Location-based lawyer discovery
- **Real-time Filtering**: Dynamic search results with instant updates

### 🤖 **AI-Powered Case Prediction**
- **Natural Language Processing**: Advanced text analysis using spaCy
- **Case Similarity Matching**: TF-IDF vectorization and cosine similarity algorithms
- **Outcome Prediction**: Machine learning models for case outcome probability
- **Legal Argument Suggestions**: AI-generated strategic legal arguments
- **Confidence Scoring**: Reliability indicators for predictions

### 📊 **Data Visualization & Analytics**
- **Interactive Charts**: Beautiful visualizations using fl_chart (Flutter) and Chart.js
- **Performance Metrics**: Comprehensive analytics for lawyers and cases
- **Trend Analysis**: Historical data analysis and pattern recognition
- **Export Capabilities**: Data export in multiple formats

### 🛡️ **Administrative Dashboard**
- **User Management**: Complete user lifecycle management
- **Lawyer Approval Workflow**: Streamlined verification and approval process
- **System Monitoring**: Real-time platform health and usage metrics
- **Bulk Operations**: Efficient mass data operations
- **Audit Logging**: Comprehensive activity tracking

---

## 🏗️ Architecture

### 🎨 **Frontend Architecture**
```
Flutter Application (Cross-platform)
├── 📱 Mobile Apps (Android/iOS)
├── 🌐 Web Application (Progressive Web App)
├── 🎨 Material Design UI/UX
├── 🔄 BLoC State Management
├── 📊 Interactive Charts (fl_chart)
└── 🔒 Secure Token Storage
```

### ⚙️ **Backend Architecture**
```
Django REST API
├── 🔐 JWT Authentication
├── 📊 RESTful API Design
├── 🗄️ MySQL Database
├── ⚡ Redis Caching
├── 🤖 AI/ML Pipeline
└── 🔗 External API Integration
```

### 🧠 **AI/ML Pipeline**
```
Natural Language Processing
├── 📝 Text Preprocessing (spaCy)
├── 🔢 TF-IDF Vectorization
├── 📐 Cosine Similarity Matching
├── 🎯 Outcome Prediction Models
└── 💡 Argument Generation
```

### 🔗 **Technology Stack**

| Layer | Technologies |
|-------|-------------|
| **Frontend** | Flutter, Dart, Material Design, fl_chart, BLoC |
| **Backend** | Django, Django REST Framework, Python |
| **Database** | MySQL, Redis (Caching) |
| **AI/ML** | spaCy, scikit-learn, TensorFlow |
| **Authentication** | JWT, OAuth 2.0 |
| **External APIs** | DigiLocker API |
| **DevOps** | Docker, GitHub Actions, AWS/GCP |

---

## 🚀 Quick Start

### 📋 Prerequisites

- **Python 3.9+** - Backend development
- **Flutter 3.10+** - Frontend development  
- **MySQL 8.0+** - Database (optional for testing)
- **Redis 6.0+** - Caching (optional for testing)
- **Git** - Version control

### ⚡ One-Command Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-judiciary-platform.git
cd ai-judiciary-platform

# Run complete setup
python setup_complete.py
```

### 🔧 Manual Setup

<details>
<summary><b>🐍 Backend Setup (Django)</b></summary>

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements_basic.txt

# Run migrations
python manage.py migrate --settings=judiciary_platform.settings_basic

# Create superuser (optional)
python manage.py createsuperuser --settings=judiciary_platform.settings_basic

# Start development server
python manage.py runserver --settings=judiciary_platform.settings_basic
```

**🌐 Backend will be available at:** `http://localhost:8000`

</details>

<details>
<summary><b>📱 Frontend Setup (Flutter)</b></summary>

```bash
# Navigate to frontend
cd frontend

# Enable web support
flutter config --enable-web

# Install dependencies
flutter pub get

# Run on web
flutter run -d chrome

# Run on mobile (with emulator/device)
flutter run
```

**🌐 Frontend will be available at:** `http://localhost:3000` (or auto-assigned port)

</details>

### 🧪 Testing Setup

```bash
# Test backend
python test_basic.py

# Test frontend
python test_flutter.py

# Test complete setup
python setup_complete.py
```

---

## 📊 API Documentation

### 🔐 Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/register/` | User registration |
| `POST` | `/api/auth/login/` | User login |
| `POST` | `/api/auth/logout/` | User logout |
| `POST` | `/api/auth/token/refresh/` | Refresh JWT token |
| `GET` | `/api/auth/profile/` | Get user profile |
| `GET` | `/api/auth/health/` | Health check |

### ⚖️ Lawyer Management Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/lawyers/` | List all lawyers |
| `POST` | `/api/lawyers/` | Create lawyer profile |
| `GET` | `/api/lawyers/{id}/` | Get lawyer details |
| `PUT` | `/api/lawyers/{id}/` | Update lawyer profile |
| `POST` | `/api/lawyers/verify/` | DigiLocker verification |
| `GET` | `/api/lawyers/search/` | Search lawyers |
| `GET` | `/api/lawyers/{id}/stats/` | Lawyer statistics |

### 📋 Case Management Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/cases/` | List cases |
| `POST` | `/api/cases/` | Create new case |
| `GET` | `/api/cases/{id}/` | Get case details |
| `PUT` | `/api/cases/{id}/` | Update case |
| `DELETE` | `/api/cases/{id}/` | Delete case |

### 🤖 AI Prediction Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/ai/predict/` | Get case prediction |
| `GET` | `/api/ai/history/` | Prediction history |
| `GET` | `/api/ai/similar-cases/` | Find similar cases |

---

## 🗂️ Project Structure

```
ai-judiciary-platform/
├── 📁 backend/                    # Django REST API
│   ├── 📁 judiciary_platform/     # Main Django project
│   │   ├── settings.py            # Django settings
│   │   ├── settings_basic.py      # Basic settings for testing
│   │   ├── urls.py                # URL routing
│   │   └── wsgi.py                # WSGI configuration
│   ├── 📁 accounts/               # User authentication app
│   │   ├── models.py              # User models
│   │   ├── views.py               # Authentication views
│   │   └── urls.py                # Auth URLs
│   ├── 📁 lawyers/                # Lawyer management app
│   ├── 📁 cases/                  # Case management app
│   ├── 📁 ai_prediction/          # AI/ML services app
│   ├── 📁 admin_panel/            # Admin functionality app
│   ├── requirements.txt           # Python dependencies
│   ├── requirements_basic.txt     # Basic dependencies for testing
│   └── manage.py                  # Django management script
├── 📁 frontend/                   # Flutter application
│   ├── 📁 lib/                    # Dart source code
│   │   ├── 📁 core/               # Core utilities
│   │   │   ├── 📁 constants/      # App constants
│   │   │   ├── 📁 network/        # HTTP client
│   │   │   ├── 📁 router/         # Navigation
│   │   │   └── 📁 theme/          # App theming
│   │   ├── 📁 features/           # Feature modules
│   │   │   ├── 📁 auth/           # Authentication
│   │   │   ├── 📁 lawyers/        # Lawyer features
│   │   │   ├── 📁 cases/          # Case features
│   │   │   └── 📁 ai_chat/        # AI chatbot
│   │   └── main.dart              # App entry point
│   ├── 📁 web/                    # Web-specific files
│   ├── 📁 assets/                 # Static assets
│   └── pubspec.yaml               # Flutter dependencies
├── 📁 .kiro/                      # Project specifications
│   └── 📁 specs/                  # Detailed specifications
├── 📄 README.md                   # This file
├── 📄 setup_complete.py           # Complete setup script
├── 📄 test_basic.py               # Backend testing script
├── 📄 test_flutter.py             # Frontend testing script
└── 📄 LICENSE                     # MIT License
```

---

## 🧪 Testing

### 🔬 Backend Testing

```bash
# Run Django tests
cd backend
python manage.py test --settings=judiciary_platform.settings_basic

# Run specific app tests
python manage.py test accounts --settings=judiciary_platform.settings_basic

# Test with coverage
pip install coverage
coverage run --source='.' manage.py test --settings=judiciary_platform.settings_basic
coverage report
```

### 📱 Frontend Testing

```bash
# Run Flutter tests
cd frontend
flutter test

# Run widget tests
flutter test test/widget_test.dart

# Run integration tests
flutter test integration_test/
```

### 🌐 API Testing

```bash
# Test API endpoints
python test_basic.py

# Manual API testing
curl -X GET http://localhost:8000/api/auth/health/
```

---

## 🚀 Deployment

### 🐳 Docker Deployment

<details>
<summary><b>Docker Configuration</b></summary>

```dockerfile
# Backend Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "judiciary_platform.wsgi:application", "--bind", "0.0.0.0:8000"]
```

```dockerfile
# Frontend Dockerfile
FROM nginx:alpine
COPY build/web /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

</details>

### ☁️ Cloud Deployment

<details>
<summary><b>AWS Deployment</b></summary>

- **Backend**: AWS Elastic Beanstalk or ECS
- **Frontend**: AWS S3 + CloudFront
- **Database**: AWS RDS (MySQL)
- **Cache**: AWS ElastiCache (Redis)
- **Storage**: AWS S3

</details>

<details>
<summary><b>Google Cloud Deployment</b></summary>

- **Backend**: Google App Engine or Cloud Run
- **Frontend**: Firebase Hosting
- **Database**: Cloud SQL (MySQL)
- **Cache**: Memorystore (Redis)
- **Storage**: Cloud Storage

</details>

---

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### 🔄 Development Workflow

1. **Fork the repository**
   ```bash
   git fork https://github.com/yourusername/ai-judiciary-platform.git
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes**
   - Follow coding standards
   - Add tests for new features
   - Update documentation

4. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```

5. **Push to your branch**
   ```bash
   git push origin feature/amazing-feature
   ```

6. **Open a Pull Request**

### 📝 Coding Standards

- **Python**: Follow PEP 8 guidelines
- **Dart/Flutter**: Follow official Dart style guide
- **Documentation**: Update README and inline comments
- **Testing**: Maintain test coverage above 80%

### 🐛 Bug Reports

Please use the [GitHub Issues](https://github.com/yourusername/ai-judiciary-platform/issues) page to report bugs.

---

## 📖 Documentation

- **📋 [Requirements](/.kiro/specs/ai-judiciary-platform/requirements.md)** - Detailed project requirements
- **🏗️ [Design Document](/.kiro/specs/ai-judiciary-platform/design.md)** - System architecture and design
- **📊 [Architecture Diagrams](/.kiro/specs/ai-judiciary-platform/architecture-diagrams.md)** - Visual system architecture
- **✅ [Implementation Tasks](/.kiro/specs/ai-judiciary-platform/tasks.md)** - Development roadmap
- **🔧 [Setup Instructions](/setup_instructions.md)** - Detailed setup guide

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Django Community** - For the robust web framework
- **Flutter Team** - For the amazing cross-platform framework
- **spaCy** - For natural language processing capabilities
- **DigiLocker** - For secure document verification services
- **Open Source Community** - For the countless libraries and tools

---

## 📞 Support & Contact

<div align="center">

**Need help? We're here for you!**

[![Email](https://img.shields.io/badge/Email-support%40judiciaryplatform.com-red?style=for-the-badge&logo=gmail)](mailto:support@judiciaryplatform.com)
[![GitHub Issues](https://img.shields.io/badge/GitHub-Issues-black?style=for-the-badge&logo=github)](https://github.com/yourusername/ai-judiciary-platform/issues)
[![Documentation](https://img.shields.io/badge/Documentation-Wiki-blue?style=for-the-badge&logo=gitbook)](https://github.com/yourusername/ai-judiciary-platform/wiki)

</div>

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

Made with ❤️ by the AI-Enhanced Judiciary Platform Team

</div>