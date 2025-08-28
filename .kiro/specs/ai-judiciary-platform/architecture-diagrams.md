# Architecture Diagrams

## 1. Overall System Architecture with Task Mapping

```mermaid
graph TB
    subgraph "Flutter Frontend (Tasks 2, 3, 5, 6, 7, 9, 11, 12)"
        UI[Flutter UI Layer]
        STATE[State Management - BLoC]
        AUTH_UI[Auth Screens]
        LAWYER_UI[Lawyer Profile Screens]
        SEARCH_UI[Search Interface]
        CHAT_UI[AI Chatbot Interface]
        ADMIN_UI[Admin Dashboard]
        CHARTS[fl_chart Visualizations]
    end
    
    subgraph "Django REST API Backend (Tasks 1, 2, 4, 8, 10)"
        subgraph "Authentication (Task 2)"
            JWT[JWT Token Management]
            USER_API[User Registration/Login APIs]
        end
        
        subgraph "Lawyer Management (Tasks 3, 4)"
            LAWYER_API[Lawyer Profile APIs]
            OCR_VERIFICATION[OCR Verification System]
            MOCK_VERIFICATION[Mock Verification Demo]
            VERIFICATION[Verification Workflow]
        end
        
        subgraph "Case Management (Task 5)"
            CASE_API[Case CRUD APIs]
            STATS_API[Statistics Calculation]
        end
        
        subgraph "AI Prediction Engine (Tasks 8, 9)"
            NLP_PIPELINE[spaCy NLP Pipeline]
            TFIDF[TF-IDF Vectorization]
            SIMILARITY[Cosine Similarity]
            PREDICTION[Case Outcome Prediction]
        end
        
        subgraph "Admin Panel (Task 11)"
            ADMIN_API[Admin Management APIs]
            BULK_OPS[Bulk Operations]
        end
    end
    
    subgraph "External Services"
        TESSERACT_OCR[Tesseract OCR Engine]
        EMAIL_SERVICE[Email Notification Service]
        FILE_STORAGE[File Storage Service]
    end
    
    subgraph "Data Layer (Task 1)"
        MYSQL[(MySQL Database)]
        REDIS[(Redis Cache)]
    end
    
    UI --> STATE
    STATE --> JWT
    AUTH_UI --> USER_API
    LAWYER_UI --> LAWYER_API
    SEARCH_UI --> LAWYER_API
    CHAT_UI --> NLP_PIPELINE
    ADMIN_UI --> ADMIN_API
    CHARTS --> STATS_API
    
    OCR_VERIFICATION --> TESSERACT_OCR
    VERIFICATION --> EMAIL_SERVICE
    LAWYER_API --> MYSQL
    CASE_API --> MYSQL
    NLP_PIPELINE --> MYSQL
    ADMIN_API --> MYSQL
    STATS_API --> REDIS
```

## 2. AI/NLP Pipeline Architecture (Tasks 8, 9)

```mermaid
graph TB
    subgraph "Flutter Chat Interface (Task 9)"
        CHAT_INPUT[User Case Input]
        CHAT_DISPLAY[Prediction Display]
        CONFIDENCE[Confidence Score UI]
        ARGUMENTS[Suggested Arguments UI]
    end
    
    subgraph "AI Processing Pipeline (Task 8)"
        subgraph "Text Preprocessing"
            CLEAN[Text Cleaning]
            TOKENIZE[spaCy Tokenization]
            LEMMA[Lemmatization]
            STOP_WORDS[Stop Words Removal]
        end
        
        subgraph "Feature Extraction"
            TFIDF_VEC[TF-IDF Vectorizer]
            FEATURE_MATRIX[Feature Matrix Generation]
        end
        
        subgraph "Similarity Matching"
            COSINE_SIM[Cosine Similarity Calculation]
            CASE_MATCHING[Historical Case Matching]
            THRESHOLD[Similarity Threshold Filter]
        end
        
        subgraph "Prediction Logic"
            OUTCOME_CALC[Outcome Probability Calculation]
            CONFIDENCE_SCORE[Confidence Score Generation]
            ARGUMENT_GEN[Legal Arguments Generation]
        end
    end
    
    subgraph "Data Sources"
        HISTORICAL_CASES[(Historical Cases DB)]
        CASE_OUTCOMES[(Case Outcomes)]
        LEGAL_PRECEDENTS[(Legal Precedents)]
    end
    
    CHAT_INPUT --> CLEAN
    CLEAN --> TOKENIZE
    TOKENIZE --> LEMMA
    LEMMA --> STOP_WORDS
    STOP_WORDS --> TFIDF_VEC
    TFIDF_VEC --> FEATURE_MATRIX
    FEATURE_MATRIX --> COSINE_SIM
    COSINE_SIM --> CASE_MATCHING
    CASE_MATCHING --> THRESHOLD
    THRESHOLD --> OUTCOME_CALC
    OUTCOME_CALC --> CONFIDENCE_SCORE
    CONFIDENCE_SCORE --> ARGUMENT_GEN
    
    CASE_MATCHING --> HISTORICAL_CASES
    OUTCOME_CALC --> CASE_OUTCOMES
    ARGUMENT_GEN --> LEGAL_PRECEDENTS
    
    OUTCOME_CALC --> CHAT_DISPLAY
    CONFIDENCE_SCORE --> CONFIDENCE
    ARGUMENT_GEN --> ARGUMENTS
```

## 3. Authentication Flow Architecture (Task 2)

```mermaid
sequenceDiagram
    participant F as Flutter App
    participant D as Django API
    participant DB as MySQL Database
    participant R as Redis Cache
    
    Note over F,R: User Registration Flow
    F->>D: POST /api/auth/register
    D->>DB: Create User Record
    D->>D: Generate JWT Tokens
    D->>R: Cache Refresh Token
    D->>F: Return Access & Refresh Tokens
    F->>F: Store Tokens Securely
    
    Note over F,R: Login Flow
    F->>D: POST /api/auth/login
    D->>DB: Validate Credentials
    D->>D: Generate JWT Tokens
    D->>R: Cache Refresh Token
    D->>F: Return Tokens + User Data
    
    Note over F,R: Token Refresh Flow
    F->>D: POST /api/auth/refresh
    D->>R: Validate Refresh Token
    D->>D: Generate New Access Token
    D->>F: Return New Access Token
    
    Note over F,R: Protected API Calls
    F->>D: API Call with JWT Header
    D->>D: Validate JWT Token
    D->>DB: Execute Request
    D->>F: Return Response
```

## 4. Multi-Method Verification System Architecture (Task 4)

```mermaid
graph TB
    subgraph "Flutter App"
        VERIFY_CHOICE[Verification Method Selection]
        OCR_UPLOAD[OCR Document Upload]
        MOCK_DEMO[Mock DigiLocker Demo]
        MANUAL_FORM[Manual Entry Form]
        STATUS_UI[Verification Status UI]
    end
    
    subgraph "Django Backend"
        subgraph "OCR Processing"
            FILE_UPLOAD[File Upload Handler]
            OCR_EXTRACT[OCR Text Extraction]
            REGEX_PARSE[Regex Pattern Matching]
            CONFIDENCE_CALC[Confidence Calculation]
        end
        
        subgraph "Mock Demo System"
            MOCK_OAUTH[Mock OAuth Simulation]
            MOCK_CERT[Mock Certificate Generator]
            AUTO_APPROVE[Auto Approval for Demo]
        end
        
        subgraph "Verification Logic"
            ADMIN_QUEUE[Admin Review Queue]
            UPDATE_STATUS[Update Lawyer Status]
            LOG_ATTEMPT[Log Verification Attempt]
            SEND_NOTIFICATION[Send Email Notification]
        end
    end
    
    subgraph "External Services"
        TESSERACT[Tesseract OCR Engine]
        EMAIL_SVC[Email Service]
        FILE_STORE[File Storage]
    end
    
    subgraph "Database"
        LAWYER_TABLE[(Lawyers Table)]
        VERIFICATION_LOG[(Verification Logs)]
    end
    
    VERIFY_CHOICE --> OCR_UPLOAD
    VERIFY_CHOICE --> MOCK_DEMO
    VERIFY_CHOICE --> MANUAL_FORM
    
    OCR_UPLOAD --> FILE_UPLOAD
    FILE_UPLOAD --> OCR_EXTRACT
    OCR_EXTRACT --> TESSERACT
    OCR_EXTRACT --> REGEX_PARSE
    REGEX_PARSE --> CONFIDENCE_CALC
    CONFIDENCE_CALC --> ADMIN_QUEUE
    
    MOCK_DEMO --> MOCK_OAUTH
    MOCK_OAUTH --> MOCK_CERT
    MOCK_CERT --> AUTO_APPROVE
    
    MANUAL_FORM --> ADMIN_QUEUE
    
    ADMIN_QUEUE --> UPDATE_STATUS
    AUTO_APPROVE --> UPDATE_STATUS
    UPDATE_STATUS --> LAWYER_TABLE
    UPDATE_STATUS --> LOG_ATTEMPT
    LOG_ATTEMPT --> VERIFICATION_LOG
    UPDATE_STATUS --> SEND_NOTIFICATION
    SEND_NOTIFICATION --> EMAIL_SVC
    FILE_UPLOAD --> FILE_STORE
    
    UPDATE_STATUS --> STATUS_UI
```

## 5. Lawyer Search Algorithm Architecture (Task 6)

```mermaid
graph TB
    subgraph "Flutter Search Interface"
        SEARCH_FORM[Search Form]
        FILTERS[Filter Options]
        RESULTS_LIST[Results List with Pagination]
    end
    
    subgraph "Search Algorithm Engine"
        subgraph "Query Processing"
            PARSE_QUERY[Parse Search Query]
            NORMALIZE[Normalize Input]
            EXTRACT_FILTERS[Extract Filter Criteria]
        end
        
        subgraph "Database Query Optimization"
            INDEX_SCAN[Use Database Indexes]
            FILTER_CHAIN[Apply Filter Chain]
            SCORE_CALC[Calculate Relevance Score]
        end
        
        subgraph "Ranking Algorithm"
            WEIGHT_FACTORS["Weight Factors:<br/>- Name Match: 30%<br/>- Specialization: 25%<br/>- Location: 20%<br/>- Win Rate: 25%"]
            SORT_RESULTS[Sort by Relevance]
            PAGINATION[Apply Pagination]
        end
    end
    
    subgraph "Database Queries"
        NAME_SEARCH[Name LIKE Query]
        SPEC_FILTER[Specialization Filter]
        LOCATION_FILTER[Location Filter]
        WIN_RATE_CALC[Win Rate Calculation]
    end
    
    SEARCH_FORM --> PARSE_QUERY
    FILTERS --> EXTRACT_FILTERS
    PARSE_QUERY --> NORMALIZE
    EXTRACT_FILTERS --> FILTER_CHAIN
    NORMALIZE --> INDEX_SCAN
    INDEX_SCAN --> NAME_SEARCH
    FILTER_CHAIN --> SPEC_FILTER
    FILTER_CHAIN --> LOCATION_FILTER
    FILTER_CHAIN --> WIN_RATE_CALC
    
    NAME_SEARCH --> SCORE_CALC
    SPEC_FILTER --> SCORE_CALC
    LOCATION_FILTER --> SCORE_CALC
    WIN_RATE_CALC --> SCORE_CALC
    
    SCORE_CALC --> WEIGHT_FACTORS
    WEIGHT_FACTORS --> SORT_RESULTS
    SORT_RESULTS --> PAGINATION
    PAGINATION --> RESULTS_LIST
```

## 6. Case Statistics and Visualization Architecture (Task 7)

```mermaid
graph TB
    subgraph "Flutter Charts Interface"
        CHART_WIDGETS[fl_chart Widgets]
        PIE_CHART[Case Type Distribution]
        BAR_CHART[Win/Loss Ratio]
        LINE_CHART[Performance Trends]
        RESPONSIVE[Responsive Design]
    end
    
    subgraph "Statistics Calculation Engine"
        subgraph "Data Aggregation"
            CASE_GROUPING[Group Cases by Type]
            OUTCOME_COUNT[Count Outcomes]
            TIME_SERIES[Time Series Analysis]
        end
        
        subgraph "Calculation Algorithms"
            WIN_RATE_CALC["Win Rate = (Won Cases / Total Cases) * 100"]
            SUCCESS_TREND[Success Trend Calculation]
            PERFORMANCE_METRICS["Performance Metrics:<br/>- Total Cases<br/>- Win Percentage<br/>- Case Types Distribution<br/>- Monthly Performance"]
        end
        
        subgraph "Data Formatting"
            CHART_DATA[Format for fl_chart]
            JSON_RESPONSE[JSON API Response]
            CACHE_RESULTS[Cache Calculated Results]
        end
    end
    
    subgraph "Database Operations"
        CASE_QUERIES[Optimized Case Queries]
        AGGREGATION[SQL Aggregation Functions]
        INDEXING[Performance Indexes]
    end
    
    CHART_WIDGETS --> JSON_RESPONSE
    JSON_RESPONSE --> CHART_DATA
    CHART_DATA --> CASE_GROUPING
    CASE_GROUPING --> CASE_QUERIES
    CASE_QUERIES --> AGGREGATION
    
    OUTCOME_COUNT --> WIN_RATE_CALC
    TIME_SERIES --> SUCCESS_TREND
    WIN_RATE_CALC --> PERFORMANCE_METRICS
    SUCCESS_TREND --> PERFORMANCE_METRICS
    
    PERFORMANCE_METRICS --> CACHE_RESULTS
    CACHE_RESULTS --> PIE_CHART
    CACHE_RESULTS --> BAR_CHART
    CACHE_RESULTS --> LINE_CHART
    
    RESPONSIVE --> CHART_WIDGETS
```

## 7. Admin Dashboard Architecture (Task 11)

```mermaid
graph TB
    subgraph "Flutter Admin Interface"
        ADMIN_NAV[Admin Navigation]
        USER_MGMT[User Management Screen]
        LAWYER_APPROVAL[Lawyer Approval Screen]
        CASE_MONITOR[Case Monitoring Screen]
        BULK_ACTIONS[Bulk Actions Interface]
        REPORTS[Reports & Analytics]
    end
    
    subgraph "Admin API Layer"
        subgraph "User Management APIs"
            LIST_USERS["GET /api/admin/users"]
            UPDATE_USER["PUT /api/admin/users/{id}"]
            DELETE_USER["DELETE /api/admin/users/{id}"]
            BULK_USER_OPS["POST /api/admin/users/bulk"]
        end
        
        subgraph "Lawyer Management APIs"
            PENDING_LAWYERS["GET /api/admin/lawyers/pending"]
            APPROVE_LAWYER["POST /api/admin/lawyers/{id}/approve"]
            REJECT_LAWYER["POST /api/admin/lawyers/{id}/reject"]
            VERIFICATION_LOGS["GET /api/admin/verification-logs"]
        end
        
        subgraph "System Monitoring APIs"
            SYSTEM_STATS["GET /api/admin/stats"]
            CASE_ANALYTICS["GET /api/admin/case-analytics"]
            USER_ACTIVITY["GET /api/admin/user-activity"]
        end
    end
    
    subgraph "Business Logic Layer"
        subgraph "Approval Workflow"
            VALIDATE_DOCS[Validate Documents]
            UPDATE_STATUS[Update Verification Status]
            SEND_NOTIFICATIONS[Send Email Notifications]
            AUDIT_LOG[Create Audit Log]
        end
        
        subgraph "Analytics Engine"
            AGGREGATE_DATA[Aggregate Platform Data]
            GENERATE_REPORTS[Generate Reports]
            TREND_ANALYSIS[Trend Analysis]
        end
    end
    
    ADMIN_NAV --> USER_MGMT
    ADMIN_NAV --> LAWYER_APPROVAL
    ADMIN_NAV --> CASE_MONITOR
    
    USER_MGMT --> LIST_USERS
    USER_MGMT --> BULK_USER_OPS
    LAWYER_APPROVAL --> PENDING_LAWYERS
    LAWYER_APPROVAL --> APPROVE_LAWYER
    CASE_MONITOR --> VERIFICATION_LOGS
    
    APPROVE_LAWYER --> VALIDATE_DOCS
    VALIDATE_DOCS --> UPDATE_STATUS
    UPDATE_STATUS --> SEND_NOTIFICATIONS
    SEND_NOTIFICATIONS --> AUDIT_LOG
    
    REPORTS --> SYSTEM_STATS
    SYSTEM_STATS --> AGGREGATE_DATA
    AGGREGATE_DATA --> GENERATE_REPORTS
    GENERATE_REPORTS --> TREND_ANALYSIS
```

## 8. Database Schema and Relationships (Task 1)

```mermaid
erDiagram
    USERS {
        int id PK
        string username UK
        string email UK
        string first_name
        string last_name
        enum role
        boolean is_active
        datetime date_joined
    }
    
    LAWYERS {
        int id PK
        int user_id FK
        string bar_id UK
        string specialization
        string location
        int experience_years
        boolean is_verified
        datetime verification_date
        text bio
        string contact_phone
    }
    
    CASES {
        int id PK
        int lawyer_id FK
        string title
        text description
        string case_type
        enum outcome
        date date_filed
        date date_resolved
        string court_name
        string case_number
        datetime created_at
    }
    
    VERIFICATION_LOGS {
        int id PK
        int lawyer_id FK
        string verification_method
        enum status
        json extracted_data
        text admin_comments
        text raw_ocr_text
        decimal confidence_score
        datetime created_at
        datetime reviewed_at
    }
    
    AI_PREDICTIONS {
        int id PK
        int user_id FK
        text case_description
        string predicted_outcome
        decimal confidence_score
        json similar_cases
        text suggested_arguments
        datetime created_at
    }
    
    USERS ||--|| LAWYERS : "has profile"
    LAWYERS ||--o{ CASES : "handles"
    LAWYERS ||--o{ VERIFICATION_LOGS : "has logs"
    USERS ||--o{ AI_PREDICTIONS : "makes predictions"
```

## 9. Task Dependencies and Implementation Flow

```mermaid
gantt
    title Implementation Timeline and Dependencies
    dateFormat  X
    axisFormat %d
    
    section Foundation
    Task 1 - Django & Flutter Setup    :t1, 0, 3
    Task 2 - JWT Authentication        :t2, after t1, 4
    
    section Core Features
    Task 3 - Lawyer Profiles          :t3, after t2, 3
    Task 4 - Multi-Method Verification :t4, after t3, 5
    Task 5 - Case Management          :t5, after t3, 3
    Task 6 - Lawyer Search            :t6, after t5, 3
    Task 7 - Data Visualization       :t7, after t5, 3
    
    section AI Components
    Task 8 - AI/NLP Foundation        :t8, after t1, 4
    Task 9 - AI Chatbot               :t9, after t8, 4
    
    section Integration
    Task 10 - Complete REST APIs      :t10, after t6, 3
    Task 11 - Admin Dashboard         :t11, after t10, 4
    Task 12 - Flutter UI/UX           :t12, after t7, 4
    
    section Quality & Deployment
    Task 13 - Form Validation         :t13, after t12, 2
    Task 14 - Security Measures       :t14, after t13, 3
    Task 15 - Performance Optimization :t15, after t14, 2
    Task 16 - Testing Suite           :t16, after t15, 4
    Task 17 - Documentation           :t17, after t16, 2
    Task 18 - Final Integration       :t18, after t17, 3
```

## 10. Technology Stack Integration Map

```mermaid
mindmap
  root((AI Judiciary Platform))
    Frontend
      Flutter
        Material Design
        BLoC State Management
        fl_chart
        HTTP Client (Dio)
        Secure Storage
        WebView/URL Launcher
      Responsive Design
        Mobile First
        Web Compatibility
        Cross Platform
    Backend
      Django
        Django REST Framework
        JWT Authentication
        Custom User Model
        MySQL ORM
      APIs
        RESTful Design
        JSON Responses
        Pagination
        Error Handling
    AI/ML
      NLP
        spaCy Pipeline
        Text Preprocessing
        Tokenization
        Lemmatization
      Machine Learning
        TF-IDF Vectorization
        Cosine Similarity
        Prediction Algorithms
        Confidence Scoring
    Database
      MySQL
        Relational Schema
        Foreign Keys
        Indexes
        Constraints
      Caching
        Redis
        Query Optimization
        Performance
    External Services
      OCR Processing
        Tesseract Engine
        Text Extraction
        Pattern Matching
        Confidence Scoring
      Communication
        Email Service
        SMS Service
        File Storage
    Security
      Authentication
        JWT Tokens
        Role Based Access
        Secure Storage
      Data Protection
        Input Validation
        SQL Injection Prevention
        HTTPS
        Rate Limiting
```

## 11. Simplified System Architecture Flow

```mermaid
graph TB
    subgraph "Flutter Frontend"
        UI[User Interface]
        AUTH[Authentication]
        VERIFY[Lawyer Verification]
        SEARCH[Lawyer Search]
        CHAT[AI Chatbot]
        ADMIN[Admin Panel]
    end
    
    subgraph "Django Backend APIs"
        AUTH_API[Authentication API]
        VERIFY_API[Verification API]
        LAWYER_API[Lawyer API]
        CASE_API[Case API]
        AI_API[AI Prediction API]
        ADMIN_API[Admin API]
    end
    
    subgraph "Core Services"
        OCR_SERVICE[OCR Processing]
        MOCK_DL[Mock DigiLocker]
        NLP_SERVICE[NLP Pipeline]
        SEARCH_SERVICE[Search Engine]
    end
    
    subgraph "External Services"
        TESSERACT[Tesseract OCR]
        EMAIL[Email Service]
        FILE_STORAGE[File Storage]
    end
    
    subgraph "Database"
        MYSQL[(MySQL Database)]
        REDIS[(Redis Cache)]
    end
    
    %% Frontend to API connections
    AUTH --> AUTH_API
    VERIFY --> VERIFY_API
    SEARCH --> LAWYER_API
    CHAT --> AI_API
    ADMIN --> ADMIN_API
    
    %% API to Service connections
    VERIFY_API --> OCR_SERVICE
    VERIFY_API --> MOCK_DL
    AI_API --> NLP_SERVICE
    LAWYER_API --> SEARCH_SERVICE
    
    %% Service to External connections
    OCR_SERVICE --> TESSERACT
    VERIFY_API --> EMAIL
    OCR_SERVICE --> FILE_STORAGE
    
    %% Database connections
    AUTH_API --> MYSQL
    VERIFY_API --> MYSQL
    LAWYER_API --> MYSQL
    CASE_API --> MYSQL
    AI_API --> MYSQL
    SEARCH_SERVICE --> REDIS
```

## 12. Practical Verification Methods Data Flow

```mermaid
sequenceDiagram
    participant U as User (Lawyer)
    participant F as Flutter Frontend
    participant A as Django API
    participant O as OCR Service
    participant T as Tesseract
    participant M as Mock DigiLocker
    participant AD as Admin Dashboard
    participant DB as Database
    participant E as Email Service
    
    Note over U,E: OCR Verification Flow
    U->>F: Select "OCR Verification"
    F->>U: Show file upload interface
    U->>F: Upload Bar Council certificate
    F->>A: POST /api/lawyers/verify-ocr/ (multipart)
    A->>O: Process certificate file
    O->>T: Extract text using OCR
    T->>O: Return extracted text
    O->>O: Parse lawyer details using regex
    O->>A: Return parsed data + confidence
    A->>DB: Create verification record (pending)
    A->>F: Return extracted data for review
    F->>U: Show extracted data + confidence
    U->>F: Confirm/edit extracted data
    F->>A: Submit verification request
    A->>AD: Queue for admin review
    
    Note over U,E: Admin Review Process
    AD->>A: GET /api/admin/pending-verifications/
    A->>DB: Fetch pending verifications
    DB->>A: Return verification list
    A->>AD: Display pending verifications
    AD->>A: POST /api/admin/verify/{id}/approve
    A->>DB: Update verification status
    A->>DB: Update lawyer verified status
    A->>E: Send approval notification
    E->>U: Email: "Verification Approved"
    
    Note over U,E: Mock DigiLocker Flow (Demo)
    U->>F: Select "DigiLocker Demo"
    F->>U: Show demo OAuth interface
    U->>F: Enter basic lawyer details
    F->>A: POST /api/lawyers/verify-mock-digilocker/
    A->>M: Simulate OAuth flow
    M->>A: Return mock certificate data
    A->>DB: Create verification (auto-approved)
    A->>DB: Update lawyer verified status
    A->>F: Return success with demo badge
    F->>U: Show "Verified (Demo Mode)"
    
    Note over U,E: Manual Verification Flow
    U->>F: Select "Manual Verification"
    F->>U: Show manual entry form
    U->>F: Fill lawyer details manually
    F->>A: POST /api/lawyers/verify-manual/
    A->>DB: Create verification record (pending)
    A->>AD: Queue for admin review
    A->>F: Return submission confirmation
    F->>U: Show "Submitted for Review"
```

## 13. AI Prediction System Architecture

```mermaid
graph TB
    subgraph "Input Processing"
        CASE_INPUT[User Case Description]
        INPUT_VALIDATION[Input Validation]
        TEXT_PREPROCESSING[Text Preprocessing]
    end
    
    subgraph "NLP Pipeline"
        TOKENIZATION[spaCy Tokenization]
        LEMMATIZATION[Lemmatization]
        STOP_WORDS[Stop Words Removal]
        NORMALIZATION[Text Normalization]
    end
    
    subgraph "Feature Engineering"
        TFIDF[TF-IDF Vectorization]
        FEATURE_SELECTION[Feature Selection]
        VECTOR_NORM[Vector Normalization]
    end
    
    subgraph "Similarity Matching"
        HISTORICAL_DB[(Historical Cases)]
        COSINE_SIM[Cosine Similarity]
        THRESHOLD[Similarity Threshold]
        TOP_K[Top-K Selection]
    end
    
    subgraph "Prediction"
        OUTCOME_AGG[Outcome Aggregation]
        PROBABILITY[Probability Calculation]
        CONFIDENCE[Confidence Scoring]
    end
    
    subgraph "Response"
        FORMAT[Format Response]
        ARGUMENTS[Legal Arguments]
        DISPLAY[Display Results]
    end
    
    CASE_INPUT --> INPUT_VALIDATION
    INPUT_VALIDATION --> TEXT_PREPROCESSING
    TEXT_PREPROCESSING --> TOKENIZATION
    TOKENIZATION --> LEMMATIZATION
    LEMMATIZATION --> STOP_WORDS
    STOP_WORDS --> NORMALIZATION
    
    NORMALIZATION --> TFIDF
    TFIDF --> FEATURE_SELECTION
    FEATURE_SELECTION --> VECTOR_NORM
    
    VECTOR_NORM --> COSINE_SIM
    HISTORICAL_DB --> COSINE_SIM
    COSINE_SIM --> THRESHOLD
    THRESHOLD --> TOP_K
    
    TOP_K --> OUTCOME_AGG
    OUTCOME_AGG --> PROBABILITY
    PROBABILITY --> CONFIDENCE
    
    CONFIDENCE --> FORMAT
    TOP_K --> ARGUMENTS
    FORMAT --> DISPLAY
    ARGUMENTS --> DISPLAY
```

## 14. Security Architecture Overview

```mermaid
graph TB
    subgraph "Frontend Security"
        INPUT_SANITIZATION[Input Sanitization]
        XSS_PROTECTION[XSS Protection]
        SECURE_STORAGE[Secure Token Storage]
    end
    
    subgraph "API Security"
        JWT_VALIDATION[JWT Validation]
        RATE_LIMITING[Rate Limiting]
        REQUEST_VALIDATION[Request Validation]
    end
    
    subgraph "Data Security"
        ENCRYPTION[Data Encryption]
        FILE_VALIDATION[File Validation]
        AUDIT_LOGGING[Audit Logging]
    end
    
    subgraph "Verification Security"
        OCR_VALIDATION[OCR Result Validation]
        ADMIN_APPROVAL[Admin Approval Required]
        VERIFICATION_AUDIT[Verification Audit Trail]
    end
    
    INPUT_SANITIZATION --> REQUEST_VALIDATION
    XSS_PROTECTION --> JWT_VALIDATION
    SECURE_STORAGE --> RATE_LIMITING
    
    JWT_VALIDATION --> ENCRYPTION
    RATE_LIMITING --> FILE_VALIDATION
    REQUEST_VALIDATION --> AUDIT_LOGGING
    
    FILE_VALIDATION --> OCR_VALIDATION
    OCR_VALIDATION --> ADMIN_APPROVAL
    ADMIN_APPROVAL --> VERIFICATION_AUDIT
```

These comprehensive architecture diagrams provide a complete view of the AI-Enhanced Judiciary Platform with practical verification methods that address real-world deployment constraints while maintaining technical depth and academic value.