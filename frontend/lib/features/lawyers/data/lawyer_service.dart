import 'package:dio/dio.dart';
import '../../../core/constants/api_constants.dart';
import '../../../core/services/auth_service.dart';

class LawyerService {
  final Dio _dio = Dio();
  final AuthService _authService = AuthService();

  LawyerService() {
    _dio.options.baseUrl = ApiConstants.baseUrl;
    _dio.options.connectTimeout = const Duration(seconds: 30);
    _dio.options.receiveTimeout = const Duration(seconds: 30);
  }

  Future<String?> _getToken() async {
    return await _authService.getAccessToken();
  }

  Future<Map<String, dynamic>> getLawyerProfile() async {
    try {
      String? token = await _getToken();
      Options options = Options(
        headers: {
          if (token != null) 'Authorization': 'Bearer $token',
        },
      );

      Response response = await _dio.get(
        '/api/lawyers/profile/',
        options: options,
      );

      return {
        'success': true,
        'data': response.data,
      };
    } on DioException catch (e) {
      return {
        'success': false,
        'error': _handleDioError(e),
      };
    } catch (e) {
      return {
        'success': false,
        'error': 'Failed to fetch lawyer profile: $e',
      };
    }
  }

  Future<Map<String, dynamic>> updateLawyerProfile(Map<String, dynamic> profileData) async {
    try {
      String? token = await _getToken();
      Options options = Options(
        headers: {
          'Content-Type': 'application/json',
          if (token != null) 'Authorization': 'Bearer $token',
        },
      );

      Response response = await _dio.put(
        '/api/lawyers/profile/update/',
        data: profileData,
        options: options,
      );

      return {
        'success': true,
        'data': response.data,
      };
    } on DioException catch (e) {
      return {
        'success': false,
        'error': _handleDioError(e),
      };
    } catch (e) {
      return {
        'success': false,
        'error': 'Failed to update lawyer profile: $e',
      };
    }
  }

  Future<Map<String, dynamic>> searchLawyers({
    String? name,
    String? specialization,
    String? location,
    int? minExperience,
    int page = 1,
  }) async {
    try {
      Map<String, dynamic> queryParams = {};
      
      if (name != null && name.isNotEmpty) queryParams['name'] = name;
      if (specialization != null && specialization.isNotEmpty) queryParams['specialization'] = specialization;
      if (location != null && location.isNotEmpty) queryParams['location'] = location;
      if (minExperience != null) queryParams['min_experience'] = minExperience;
      queryParams['page'] = page;

      Response response = await _dio.get(
        '/api/lawyers/search/',
        queryParameters: queryParams,
      );

      return {
        'success': true,
        'data': response.data,
      };
    } on DioException catch (e) {
      return {
        'success': false,
        'error': _handleDioError(e),
      };
    } catch (e) {
      return {
        'success': false,
        'error': 'Failed to search lawyers: $e',
      };
    }
  }

  Future<Map<String, dynamic>> getLawyerCases() async {
    try {
      String? token = await _getToken();
      Options options = Options(
        headers: {
          if (token != null) 'Authorization': 'Bearer $token',
        },
      );

      Response response = await _dio.get(
        '/api/cases/',
        options: options,
      );

      return {
        'success': true,
        'data': response.data,
      };
    } on DioException catch (e) {
      return {
        'success': false,
        'error': _handleDioError(e),
      };
    } catch (e) {
      return {
        'success': false,
        'error': 'Failed to fetch cases: $e',
      };
    }
  }

  Future<Map<String, dynamic>> createCase(Map<String, dynamic> caseData) async {
    try {
      String? token = await _getToken();
      Options options = Options(
        headers: {
          'Content-Type': 'application/json',
          if (token != null) 'Authorization': 'Bearer $token',
        },
      );

      Response response = await _dio.post(
        '/api/cases/',
        data: caseData,
        options: options,
      );

      return {
        'success': true,
        'data': response.data,
      };
    } on DioException catch (e) {
      return {
        'success': false,
        'error': _handleDioError(e),
      };
    } catch (e) {
      return {
        'success': false,
        'error': 'Failed to create case: $e',
      };
    }
  }

  Future<Map<String, dynamic>> updateCase(int caseId, Map<String, dynamic> caseData) async {
    try {
      String? token = await _getToken();
      Options options = Options(
        headers: {
          'Content-Type': 'application/json',
          if (token != null) 'Authorization': 'Bearer $token',
        },
      );

      Response response = await _dio.put(
        '/api/cases/$caseId/',
        data: caseData,
        options: options,
      );

      return {
        'success': true,
        'data': response.data,
      };
    } on DioException catch (e) {
      return {
        'success': false,
        'error': _handleDioError(e),
      };
    } catch (e) {
      return {
        'success': false,
        'error': 'Failed to update case: $e',
      };
    }
  }

  Future<Map<String, dynamic>> deleteCase(int caseId) async {
    try {
      String? token = await _getToken();
      Options options = Options(
        headers: {
          if (token != null) 'Authorization': 'Bearer $token',
        },
      );

      Response response = await _dio.delete(
        '/api/cases/$caseId/',
        options: options,
      );

      return {
        'success': true,
        'data': response.data,
      };
    } on DioException catch (e) {
      return {
        'success': false,
        'error': _handleDioError(e),
      };
    } catch (e) {
      return {
        'success': false,
        'error': 'Failed to delete case: $e',
      };
    }
  }

  String _handleDioError(DioException e) {
    switch (e.type) {
      case DioExceptionType.connectionTimeout:
        return 'Connection timeout. Please check your internet connection.';
      case DioExceptionType.sendTimeout:
        return 'Request timeout. Please try again.';
      case DioExceptionType.receiveTimeout:
        return 'Server response timeout. Please try again.';
      case DioExceptionType.badResponse:
        if (e.response?.data != null && e.response?.data is Map) {
          final errorData = e.response!.data as Map<String, dynamic>;
          if (errorData.containsKey('error')) {
            return errorData['error'].toString();
          }
          if (errorData.containsKey('message')) {
            return errorData['message'].toString();
          }
        }
        return 'Server error: ${e.response?.statusCode}';
      case DioExceptionType.cancel:
        return 'Request was cancelled';
      case DioExceptionType.unknown:
        return 'Network error. Please check your connection.';
      default:
        return 'An unexpected error occurred';
    }
  }
}