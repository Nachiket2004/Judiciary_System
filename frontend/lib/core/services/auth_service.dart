import 'dart:convert';
import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../constants/api_constants.dart';

class AuthService {
  final Dio _dio = Dio();
  final FlutterSecureStorage _secureStorage = const FlutterSecureStorage();
  
  // Storage keys
  static const String _accessTokenKey = 'access_token';
  static const String _refreshTokenKey = 'refresh_token';
  static const String _userDataKey = 'user_data';

  AuthService() {
    _dio.options.baseUrl = ApiConstants.baseUrl;
    _dio.options.connectTimeout = const Duration(seconds: 30);
    _dio.options.receiveTimeout = const Duration(seconds: 30);
    
    // Add interceptor for automatic token refresh
    _dio.interceptors.add(InterceptorsWrapper(
      onRequest: (options, handler) async {
        // Add access token to requests
        String? token = await getAccessToken();
        if (token != null) {
          options.headers['Authorization'] = 'Bearer $token';
        }
        handler.next(options);
      },
      onError: (error, handler) async {
        // Handle token refresh on 401 errors
        if (error.response?.statusCode == 401) {
          bool refreshed = await _refreshToken();
          if (refreshed) {
            // Retry the original request
            String? newToken = await getAccessToken();
            if (newToken != null) {
              error.requestOptions.headers['Authorization'] = 'Bearer $newToken';
              final response = await _dio.fetch(error.requestOptions);
              handler.resolve(response);
              return;
            }
          }
          // If refresh failed, logout user
          await logout();
        }
        handler.next(error);
      },
    ));
  }

  Future<Map<String, dynamic>> register({
    required String username,
    required String email,
    required String firstName,
    required String lastName,
    required String password,
    required String passwordConfirm,
    String role = 'user',
    String? phoneNumber,
  }) async {
    try {
      Response response = await _dio.post(
        '/api/auth/register/',
        data: {
          'username': username,
          'email': email,
          'first_name': firstName,
          'last_name': lastName,
          'password': password,
          'password_confirm': passwordConfirm,
          'role': role,
          if (phoneNumber != null) 'phone_number': phoneNumber,
        },
      );

      if (response.statusCode == 201) {
        // Store tokens and user data
        await _storeAuthData(response.data);
        
        return {
          'success': true,
          'message': response.data['message'],
          'user': response.data['user'],
        };
      } else {
        return {
          'success': false,
          'error': 'Registration failed',
        };
      }
    } on DioException catch (e) {
      return {
        'success': false,
        'error': _handleDioError(e),
      };
    } catch (e) {
      return {
        'success': false,
        'error': 'Registration failed: $e',
      };
    }
  }

  Future<Map<String, dynamic>> login({
    required String email,
    required String password,
  }) async {
    try {
      Response response = await _dio.post(
        '/api/auth/login/',
        data: {
          'email': email,
          'password': password,
        },
      );

      if (response.statusCode == 200) {
        // Store tokens and user data
        await _storeAuthData(response.data);
        
        return {
          'success': true,
          'message': response.data['message'],
          'user': response.data['user'],
        };
      } else {
        return {
          'success': false,
          'error': 'Login failed',
        };
      }
    } on DioException catch (e) {
      return {
        'success': false,
        'error': _handleDioError(e),
      };
    } catch (e) {
      return {
        'success': false,
        'error': 'Login failed: $e',
      };
    }
  }

  Future<bool> logout() async {
    try {
      String? refreshToken = await getRefreshToken();
      
      if (refreshToken != null) {
        await _dio.post(
          '/api/auth/logout/',
          data: {'refresh_token': refreshToken},
        );
      }
    } catch (e) {
      // Continue with logout even if API call fails
      print('Logout API call failed: $e');
    }
    
    // Clear stored data
    await _clearAuthData();
    return true;
  }

  Future<Map<String, dynamic>> getUserProfile() async {
    try {
      Response response = await _dio.get('/api/auth/profile/');
      
      if (response.statusCode == 200) {
        return {
          'success': true,
          'user': response.data['user'],
        };
      } else {
        return {
          'success': false,
          'error': 'Failed to fetch user profile',
        };
      }
    } on DioException catch (e) {
      return {
        'success': false,
        'error': _handleDioError(e),
      };
    } catch (e) {
      return {
        'success': false,
        'error': 'Failed to fetch user profile: $e',
      };
    }
  }

  Future<Map<String, dynamic>> updateUserProfile(Map<String, dynamic> userData) async {
    try {
      Response response = await _dio.put(
        '/api/auth/profile/update/',
        data: userData,
      );
      
      if (response.statusCode == 200) {
        // Update stored user data
        await _secureStorage.write(
          key: _userDataKey,
          value: jsonEncode(response.data['user']),
        );
        
        return {
          'success': true,
          'message': response.data['message'],
          'user': response.data['user'],
        };
      } else {
        return {
          'success': false,
          'error': 'Failed to update profile',
        };
      }
    } on DioException catch (e) {
      return {
        'success': false,
        'error': _handleDioError(e),
      };
    } catch (e) {
      return {
        'success': false,
        'error': 'Failed to update profile: $e',
      };
    }
  }

  // Token management methods
  Future<String?> getAccessToken() async {
    return await _secureStorage.read(key: _accessTokenKey);
  }

  Future<String?> getRefreshToken() async {
    return await _secureStorage.read(key: _refreshTokenKey);
  }

  Future<Map<String, dynamic>?> getCurrentUser() async {
    String? userDataString = await _secureStorage.read(key: _userDataKey);
    if (userDataString != null) {
      return jsonDecode(userDataString);
    }
    return null;
  }

  Future<bool> isLoggedIn() async {
    String? token = await getAccessToken();
    return token != null;
  }

  Future<bool> _refreshToken() async {
    try {
      String? refreshToken = await getRefreshToken();
      if (refreshToken == null) return false;

      Response response = await _dio.post(
        '/api/auth/token/refresh/',
        data: {'refresh': refreshToken},
      );

      if (response.statusCode == 200) {
        String newAccessToken = response.data['access'];
        await _secureStorage.write(key: _accessTokenKey, value: newAccessToken);
        return true;
      }
    } catch (e) {
      print('Token refresh failed: $e');
    }
    return false;
  }

  Future<void> _storeAuthData(Map<String, dynamic> authData) async {
    // Store tokens
    await _secureStorage.write(
      key: _accessTokenKey,
      value: authData['tokens']['access'],
    );
    await _secureStorage.write(
      key: _refreshTokenKey,
      value: authData['tokens']['refresh'],
    );
    
    // Store user data
    await _secureStorage.write(
      key: _userDataKey,
      value: jsonEncode(authData['user']),
    );
  }

  Future<void> _clearAuthData() async {
    await _secureStorage.delete(key: _accessTokenKey);
    await _secureStorage.delete(key: _refreshTokenKey);
    await _secureStorage.delete(key: _userDataKey);
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
          if (errorData.containsKey('details')) {
            // Handle validation errors
            final details = errorData['details'];
            if (details is Map) {
              List<String> errors = [];
              details.forEach((key, value) {
                if (value is List) {
                  errors.addAll(value.map((e) => '$key: $e'));
                } else {
                  errors.add('$key: $value');
                }
              });
              return errors.join(', ');
            }
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