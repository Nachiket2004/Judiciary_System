import 'package:flutter/material.dart';
import 'package:dio/dio.dart';
import '../../../../core/constants/api_constants.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  String _apiStatus = 'Testing...';
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _testApiConnection();
  }

  Future<void> _testApiConnection() async {
    try {
      final dio = Dio();
      final response = await dio.get('${ApiConstants.baseUrl}/auth/health/');
      
      if (response.statusCode == 200) {
        setState(() {
          _apiStatus = 'API Connection Successful!\n${response.data['message']}';
          _isLoading = false;
        });
      }
    } catch (e) {
      setState(() {
        _apiStatus = 'API Connection Failed:\n$e';
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('AI-Enhanced Judiciary Platform'),
        centerTitle: true,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Welcome to the AI-Enhanced Judiciary Platform',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 20),
            const Text(
              'This is a comprehensive platform connecting users with verified lawyers and providing AI-powered case prediction services.',
              style: TextStyle(fontSize: 16),
            ),
            const SizedBox(height: 30),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Backend API Status:',
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 10),
                    if (_isLoading)
                      const Row(
                        children: [
                          CircularProgressIndicator(),
                          SizedBox(width: 16),
                          Text('Testing API connection...'),
                        ],
                      )
                    else
                      Text(
                        _apiStatus,
                        style: TextStyle(
                          fontSize: 14,
                          color: _apiStatus.contains('Successful') 
                              ? Colors.green 
                              : Colors.red,
                        ),
                      ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 20),
            const Card(
              child: Padding(
                padding: EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Features to be implemented:',
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    SizedBox(height: 10),
                    Text('✅ Project Setup (Task 1)'),
                    Text('⏳ JWT Authentication (Task 2)'),
                    Text('⏳ Lawyer Profiles (Task 3)'),
                    Text('⏳ DigiLocker Integration (Task 4)'),
                    Text('⏳ Case Management (Task 5)'),
                    Text('⏳ Lawyer Search (Task 6)'),
                    Text('⏳ Data Visualization (Task 7)'),
                    Text('⏳ AI/NLP Foundation (Task 8)'),
                    Text('⏳ AI Chatbot (Task 9)'),
                    Text('⏳ Complete REST APIs (Task 10)'),
                    Text('⏳ Admin Dashboard (Task 11)'),
                    Text('⏳ Flutter UI/UX (Task 12)'),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}