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
            DIGILOCKER[DigiLocker OAuth Integration]
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
        DIGILOCKER_API[DigiLocker Sandbox API]
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
    
    DIGILOCKER --> DIGILOCKER_API
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

## 4. DigiLocker Integration Architecture (Task 4)

```mermaid
graph TB
    subgraph "Flutter App"
        VERIFY_BTN[Verify Credentials Button]
        WEBVIEW[WebView/URL Launcher]
        STATUS_UI[Verification Status UI]
    end
    
    subgraph "Django Backend"
        subgraph "OAuth Flow"
            AUTH_INIT[Initialize OAuth]
            STATE_GEN[Generate State Parameter]
            CALLBACK[OAuth Callback Handler]
            TOKEN_EXCHANGE[Authorization Code Exchange]
        end
        
        subgraph "Certificate Processing"
            CERT_FETCH[Fetch Bar Council Certificate]
            CERT_PARSE[Parse Certificate Data]
            EXTRACT_INFO[Extract Lawyer Details]
            VALIDATE[Validate Certificate]
        end
        
        subgraph "Verification Logic"
            UPDATE_STATUS[Update Lawyer Status]
            LOG_ATTEMPT[Log Verification Attempt]
            NOTIFY_ADMIN[Notify Admin if Failed]
        end
    end
    
    subgraph "DigiLocker API"
        OAUTH_SERVER[OAuth Authorization Server]
        DOCUMENT_API[Document Fetch API]
        CERTIFICATE_STORE[Certificate Repository]
    end
    
    subgraph "Database"
        LAWYER_TABLE[(Lawyers Table)]
        VERIFICATION_LOG[(Verification Logs)]
    end
    
    VERIFY_BTN --> AUTH_INIT
    AUTH_INIT --> STATE_GEN
    STATE_GEN --> WEBVIEW
    WEBVIEW --> OAUTH_SERVER
    OAUTH_SERVER --> CALLBACK
    CALLBACK --> TOKEN_EXCHANGE
    TOKEN_EXCHANGE --> CERT_FETCH
    CERT_FETCH --> DOCUMENT_API
    DOCUMENT_API --> CERTIFICATE_STORE
    CERTIFICATE_STORE --> CERT_PARSE
    CERT_PARSE --> EXTRACT_INFO
    EXTRACT_INFO --> VALIDATE
    VALIDATE --> UPDATE_STATUS
    UPDATE_STATUS --> LAWYER_TABLE
    VALIDATE --> LOG_ATTEMPT
    LOG_ATTEMPT --> VERIFICATION_LOG
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
        string verification_type
        enum status
        json digilocker_response
        text error_message
        datetime created_at
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
    Task 4 - DigiLocker Integration   :t4, after t3, 5
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
      DigiLocker
        OAuth 2.0
        Certificate Validation
        Document Fetching
        Sandbox Environment
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

These architecture diagrams provide a comprehensive view of how each task integrates with the overall system, the specific algorithms used, and the technology stack implementation. Each diagram maps directly to the implementation tasks and shows the technical details needed for development.