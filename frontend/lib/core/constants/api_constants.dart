class ApiConstants {
  // Base URLs
  static const String baseUrl = 'http://localhost:8000/api';
  static const String authBaseUrl = '$baseUrl/auth';
  static const String lawyersBaseUrl = '$baseUrl/lawyers';
  static const String casesBaseUrl = '$baseUrl/cases';
  static const String aiBaseUrl = '$baseUrl/ai';
  static const String adminBaseUrl = '$baseUrl/admin';
  
  // Auth endpoints
  static const String login = '$authBaseUrl/login/';
  static const String register = '$authBaseUrl/register/';
  static const String logout = '$authBaseUrl/logout/';
  static const String refreshToken = '$authBaseUrl/token/refresh/';
  static const String profile = '$authBaseUrl/profile/';
  static const String changePassword = '$authBaseUrl/change-password/';
  
  // Lawyer endpoints
  static const String lawyerProfile = '$lawyersBaseUrl/profile/';
  static const String lawyerSearch = '$lawyersBaseUrl/search/';
  static const String lawyerVerification = '$lawyersBaseUrl/verify/';
  static const String lawyerStats = '$lawyersBaseUrl/stats/';
  
  // Case endpoints
  static const String cases = '$casesBaseUrl/';
  static const String caseStats = '$casesBaseUrl/stats/';
  
  // AI endpoints
  static const String aiPredict = '$aiBaseUrl/predict/';
  static const String aiHistory = '$aiBaseUrl/history/';
  
  // Admin endpoints
  static const String adminUsers = '$adminBaseUrl/users/';
  static const String adminLawyers = '$adminBaseUrl/lawyers/';
  static const String adminStats = '$adminBaseUrl/stats/';
  
  // Headers
  static const Map<String, String> defaultHeaders = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  };
  
  // Timeouts
  static const int connectTimeout = 30000; // 30 seconds
  static const int receiveTimeout = 30000; // 30 seconds
  static const int sendTimeout = 30000; // 30 seconds
}