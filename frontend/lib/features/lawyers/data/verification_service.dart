import 'dart:io';
import 'package:dio/dio.dart';
import '../../../core/constants/api_constants.dart';

class VerificationService {
  final Dio _dio = Dio();

  VerificationService() {
    _dio.options.baseUrl = ApiConstants.baseUrl;
    _dio.options.connectTimeout = const Duration(seconds: 30);
    _dio.options.receiveTimeout = const Duration(seconds: 30);
  }

  Future<String?> _getToken() async {
    // TODO: Implement token retrieval from secure storage
    // For now, return null (will be implemented with authentication)
    return null;
  }

  Future<Map<String, dynamic>> verifyWithOCR(File certificateFile) async {
    try {
      String fileName = certificateFile.path.split('/').last;
      
      FormData formData = FormData.fromMap({
        'certificate': await MultipartFile.fromFile(
          certificateFile.path,
          filename: fileName,
        ),
      });

      String? token = await _getToken();
      Options options = Options(
        headers: {
          'Content-Type': 'multipart/form-data',
          if (token != null) 'Authorization': 'Bearer $token',
        },
      );

      Response response = await _dio.post(
        '/api/lawyers/verify/ocr/',
        data: formData,
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
        'error': 'OCR verification failed: $e',
      };
    }
  }

  Future<Map<String, dynamic>> verifyWithMockDigiLocker(
      Map<String, dynamic> lawyerData) async {
    try {
      String? token = await _getToken();
      Options options = Options(
        headers: {
          'Content-Type': 'application/json',
          if (token != null) 'Authorization': 'Bearer $token',
        },
      );

      Response response = await _dio.post(
        '/api/lawyers/verify/mock-digilocker/',
        data: lawyerData,
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
        'error': 'Mock DigiLocker verification failed: $e',
      };
    }
  }

  Future<Map<String, dynamic>> verifyManually(
      Map<String, dynamic> lawyerData) async {
    try {
      String? token = await _getToken();
      Options options = Options(
        headers: {
          'Content-Type': 'application/json',
          if (token != null) 'Authorization': 'Bearer $token',
        },
      );

      Response response = await _dio.post(
        '/api/lawyers/verify/manual/',
        data: lawyerData,
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
        'error': 'Manual verification failed: $e',
      };
    }
  }

  Future<Map<String, dynamic>> getVerificationStatus() async {
    try {
      String? token = await _getToken();
      Options options = Options(
        headers: {
          if (token != null) 'Authorization': 'Bearer $token',
        },
      );

      Response response = await _dio.get(
        '/api/lawyers/verification/status/',
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
        'error': 'Failed to fetch verification status: $e',
      };
    }
  }

  Future<Map<String, dynamic>> getPendingVerifications() async {
    try {
      String? token = await _getToken();
      Options options = Options(
        headers: {
          if (token != null) 'Authorization': 'Bearer $token',
        },
      );

      Response response = await _dio.get(
        '/api/lawyers/admin/verifications/pending/',
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
        'error': 'Failed to fetch pending verifications: $e',
      };
    }
  }

  Future<Map<String, dynamic>> reviewVerification(
      int verificationId, String action, String comments) async {
    try {
      String? token = await _getToken();
      Options options = Options(
        headers: {
          'Content-Type': 'application/json',
          if (token != null) 'Authorization': 'Bearer $token',
        },
      );

      Response response = await _dio.post(
        '/api/lawyers/admin/verifications/$verificationId/review/',
        data: {
          'action': action,
          'comments': comments,
        },
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
        'error': 'Failed to review verification: $e',
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