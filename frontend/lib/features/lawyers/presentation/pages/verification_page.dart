import 'dart:io';
import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import '../../data/verification_service.dart';

class LawyerVerificationPage extends StatefulWidget {
  const LawyerVerificationPage({super.key});

  @override
  State<LawyerVerificationPage> createState() => _LawyerVerificationPageState();
}

class _LawyerVerificationPageState extends State<LawyerVerificationPage> {
  final VerificationService _verificationService = VerificationService();
  final _formKey = GlobalKey<FormState>();
  
  // Controllers
  final _nameController = TextEditingController();
  final _barIdController = TextEditingController();
  final _experienceController = TextEditingController();
  final _specializationController = TextEditingController();
  final _stateController = TextEditingController();

  // State variables
  String _selectedMethod = 'ocr';
  File? _selectedFile;
  bool _isProcessing = false;
  Map<String, dynamic>? _verificationResult;
  String? _errorMessage;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Lawyer Verification'),
        backgroundColor: Theme.of(context).primaryColor,
        foregroundColor: Colors.white,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildHeader(),
            const SizedBox(height: 24),
            _buildMethodSelection(),
            const SizedBox(height: 24),
            _buildMethodContent(),
            const SizedBox(height: 24),
            _buildSubmitButton(),
            if (_verificationResult != null) ...[
              const SizedBox(height: 24),
              _buildResultDisplay(),
            ],
            if (_errorMessage != null) ...[
              const SizedBox(height: 24),
              _buildErrorDisplay(),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildHeader() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(Icons.verified_user, 
                     color: Theme.of(context).primaryColor, size: 28),
                const SizedBox(width: 12),
                Text(
                  'Lawyer Verification',
                  style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            Text(
              'Verify your lawyer credentials to access lawyer-specific features and build trust with potential clients.',
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                color: Colors.grey[600],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildMethodSelection() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Choose Verification Method:',
              style: Theme.of(context).textTheme.titleMedium?.copyWith(
                fontWeight: FontWeight.w600,
              ),
            ),
            const SizedBox(height: 16),
            
            // OCR Method
            RadioListTile<String>(
              title: const Text('Document Upload (OCR)'),
              subtitle: const Text('Upload Bar Council certificate for automatic processing'),
              value: 'ocr',
              groupValue: _selectedMethod,
              onChanged: (value) => setState(() {
                _selectedMethod = value!;
                _clearResults();
              }),
              secondary: const Icon(Icons.upload_file, color: Colors.blue),
            ),
            
            // Mock DigiLocker Method
            RadioListTile<String>(
              title: Row(
                children: [
                  const Text('DigiLocker Integration'),
                  const SizedBox(width: 8),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                    decoration: BoxDecoration(
                      color: Colors.orange,
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: const Text(
                      'DEMO',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 10,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                ],
              ),
              subtitle: const Text('Simulated DigiLocker verification for demonstration'),
              value: 'mock_digilocker',
              groupValue: _selectedMethod,
              onChanged: (value) => setState(() {
                _selectedMethod = value!;
                _clearResults();
              }),
              secondary: const Icon(Icons.account_balance, color: Colors.green),
            ),
            
            // Manual Method
            RadioListTile<String>(
              title: const Text('Manual Verification'),
              subtitle: const Text('Submit details for admin review'),
              value: 'manual',
              groupValue: _selectedMethod,
              onChanged: (value) => setState(() {
                _selectedMethod = value!;
                _clearResults();
              }),
              secondary: const Icon(Icons.person_add, color: Colors.purple),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildMethodContent() {
    switch (_selectedMethod) {
      case 'ocr':
        return _buildOCRUpload();
      case 'mock_digilocker':
        return _buildMockDigiLocker();
      case 'manual':
        return _buildManualForm();
      default:
        return const SizedBox.shrink();
    }
  }

  Widget _buildOCRUpload() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Upload Bar Council Certificate',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 16),
            
            GestureDetector(
              onTap: _pickFile,
              child: Container(
                width: double.infinity,
                padding: const EdgeInsets.all(24),
                decoration: BoxDecoration(
                  border: Border.all(
                    color: _selectedFile != null ? Colors.green : Colors.grey.shade300,
                    width: 2,
                  ),
                  borderRadius: BorderRadius.circular(12),
                  color: _selectedFile != null ? Colors.green.shade50 : Colors.grey.shade50,
                ),
                child: Column(
                  children: [
                    Icon(
                      _selectedFile != null ? Icons.check_circle : Icons.cloud_upload_outlined,
                      size: 48,
                      color: _selectedFile != null ? Colors.green : Colors.grey.shade600,
                    ),
                    const SizedBox(height: 12),
                    Text(
                      _selectedFile != null
                          ? 'Selected: ${_selectedFile!.path.split('/').last}'
                          : 'Click to upload certificate (PDF, JPG, PNG)',
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        color: _selectedFile != null ? Colors.green.shade800 : Colors.grey.shade700,
                        fontWeight: _selectedFile != null ? FontWeight.w500 : FontWeight.normal,
                      ),
                    ),
                    const SizedBox(height: 12),
                    ElevatedButton.icon(
                      onPressed: _pickFile,
                      icon: const Icon(Icons.attach_file),
                      label: Text(_selectedFile != null ? 'Change File' : 'Choose File'),
                    ),
                  ],
                ),
              ),
            ),
            
            if (_selectedFile != null) ...[
              const SizedBox(height: 16),
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.blue.shade50,
                  border: Border.all(color: Colors.blue.shade200),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Row(
                  children: [
                    Icon(Icons.info_outline, color: Colors.blue.shade600),
                    const SizedBox(width: 8),
                    Expanded(
                      child: Text(
                        'File selected successfully. Click "Process Certificate" to extract information using OCR.',
                        style: TextStyle(color: Colors.blue.shade800),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildMockDigiLocker() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.blue.shade50,
                border: Border.all(color: Colors.blue.shade200),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Column(
                children: [
                  Row(
                    children: [
                      Icon(Icons.info_outline, color: Colors.blue.shade700),
                      const SizedBox(width: 8),
                      Expanded(
                        child: Text(
                          'DigiLocker Demo Mode',
                          style: TextStyle(
                            fontWeight: FontWeight.bold,
                            color: Colors.blue.shade800,
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  Text(
                    'This demonstrates the DigiLocker integration workflow. In production, this would redirect to the official DigiLocker portal for OAuth authentication and certificate retrieval.',
                    style: TextStyle(color: Colors.blue.shade700),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 16),
            
            Form(
              key: _formKey,
              child: Column(
                children: [
                  TextFormField(
                    controller: _nameController,
                    decoration: const InputDecoration(
                      labelText: 'Full Name',
                      hintText: 'Enter your full name as per Bar Council',
                      prefixIcon: Icon(Icons.person),
                    ),
                    validator: (value) => value?.isEmpty == true ? 'Name is required' : null,
                  ),
                  const SizedBox(height: 16),
                  TextFormField(
                    controller: _barIdController,
                    decoration: const InputDecoration(
                      labelText: 'Bar Council Registration Number',
                      hintText: 'e.g., BAR/12345/2023',
                      prefixIcon: Icon(Icons.badge),
                    ),
                    validator: (value) => value?.isEmpty == true ? 'Bar ID is required' : null,
                  ),
                  const SizedBox(height: 16),
                  TextFormField(
                    controller: _stateController,
                    decoration: const InputDecoration(
                      labelText: 'State',
                      hintText: 'e.g., Delhi, Maharashtra',
                      prefixIcon: Icon(Icons.location_on),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildManualForm() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              TextFormField(
                controller: _nameController,
                decoration: const InputDecoration(
                  labelText: 'Full Name *',
                  hintText: 'Enter your full name as per Bar Council',
                  prefixIcon: Icon(Icons.person),
                ),
                validator: (value) => value?.isEmpty == true ? 'Name is required' : null,
              ),
              const SizedBox(height: 16),
              
              TextFormField(
                controller: _barIdController,
                decoration: const InputDecoration(
                  labelText: 'Bar Council Registration Number *',
                  hintText: 'e.g., BAR/12345/2023',
                  prefixIcon: Icon(Icons.badge),
                ),
                validator: (value) => value?.isEmpty == true ? 'Bar ID is required' : null,
              ),
              const SizedBox(height: 16),
              
              TextFormField(
                controller: _experienceController,
                decoration: const InputDecoration(
                  labelText: 'Years of Experience',
                  hintText: 'Enter years of practice',
                  prefixIcon: Icon(Icons.work),
                ),
                keyboardType: TextInputType.number,
              ),
              const SizedBox(height: 16),
              
              TextFormField(
                controller: _specializationController,
                decoration: const InputDecoration(
                  labelText: 'Specialization',
                  hintText: 'e.g., Criminal Law, Civil Law, Corporate Law',
                  prefixIcon: Icon(Icons.gavel),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildSubmitButton() {
    return SizedBox(
      width: double.infinity,
      child: ElevatedButton(
        onPressed: _isProcessing ? null : _submitVerification,
        style: ElevatedButton.styleFrom(
          padding: const EdgeInsets.symmetric(vertical: 16),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
        ),
        child: _isProcessing
            ? const Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  SizedBox(
                    width: 20,
                    height: 20,
                    child: CircularProgressIndicator(strokeWidth: 2),
                  ),
                  SizedBox(width: 10),
                  Text('Processing...'),
                ],
              )
            : Text(_getSubmitButtonText()),
      ),
    );
  }

  Widget _buildResultDisplay() {
    final result = _verificationResult!;
    final isSuccess = result['success'] == true;
    
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(
                  isSuccess ? Icons.check_circle : Icons.error,
                  color: isSuccess ? Colors.green : Colors.red,
                ),
                const SizedBox(width: 8),
                Text(
                  isSuccess ? 'Verification Submitted' : 'Verification Failed',
                  style: TextStyle(
                    fontWeight: FontWeight.bold,
                    color: isSuccess ? Colors.green.shade800 : Colors.red.shade800,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 8),
            Text(
              result['data']?['message'] ?? 'Verification processed',
              style: TextStyle(
                color: isSuccess ? Colors.green.shade700 : Colors.red.shade700,
              ),
            ),
            
            if (isSuccess && result['data']?['extracted_data'] != null) ...[
              const SizedBox(height: 16),
              const Text('Extracted Information:', 
                         style: TextStyle(fontWeight: FontWeight.bold)),
              const SizedBox(height: 8),
              _buildExtractedDataDisplay(result['data']['extracted_data']),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildExtractedDataDisplay(Map<String, dynamic> data) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.grey.shade50,
        border: Border.all(color: Colors.grey.shade300),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: data.entries.map((entry) {
          if (entry.key == 'confidence' || entry.key == 'demo_mode') {
            return const SizedBox.shrink();
          }
          return Padding(
            padding: const EdgeInsets.symmetric(vertical: 2),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                SizedBox(
                  width: 120,
                  child: Text(
                    '${entry.key.replaceAll('_', ' ').toUpperCase()}:',
                    style: const TextStyle(fontWeight: FontWeight.w500),
                  ),
                ),
                Expanded(
                  child: Text(entry.value?.toString() ?? 'N/A'),
                ),
              ],
            ),
          );
        }).toList(),
      ),
    );
  }

  Widget _buildErrorDisplay() {
    return Card(
      color: Colors.red.shade50,
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Row(
          children: [
            Icon(Icons.error_outline, color: Colors.red.shade600),
            const SizedBox(width: 8),
            Expanded(
              child: Text(
                _errorMessage!,
                style: TextStyle(color: Colors.red.shade800),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Future<void> _pickFile() async {
    try {
      FilePickerResult? result = await FilePicker.platform.pickFiles(
        type: FileType.custom,
        allowedExtensions: ['pdf', 'jpg', 'jpeg', 'png'],
        allowMultiple: false,
      );

      if (result != null && result.files.isNotEmpty) {
        setState(() {
          _selectedFile = File(result.files.first.path!);
          _clearResults();
        });
      }
    } catch (e) {
      _showSnackBar('Error picking file: $e');
    }
  }

  Future<void> _submitVerification() async {
    setState(() {
      _isProcessing = true;
      _clearResults();
    });

    try {
      Map<String, dynamic> result;

      switch (_selectedMethod) {
        case 'ocr':
          result = await _submitOCRVerification();
          break;
        case 'mock_digilocker':
          result = await _submitMockDigiLocker();
          break;
        case 'manual':
          result = await _submitManualVerification();
          break;
        default:
          result = {'success': false, 'error': 'Invalid verification method'};
      }

      setState(() {
        if (result['success']) {
          _verificationResult = result;
          _errorMessage = null;
        } else {
          _errorMessage = result['error'];
          _verificationResult = null;
        }
      });

    } finally {
      setState(() {
        _isProcessing = false;
      });
    }
  }

  Future<Map<String, dynamic>> _submitOCRVerification() async {
    if (_selectedFile == null) {
      return {'success': false, 'error': 'Please select a certificate file'};
    }

    return await _verificationService.verifyWithOCR(_selectedFile!);
  }

  Future<Map<String, dynamic>> _submitMockDigiLocker() async {
    if (_selectedMethod == 'mock_digilocker' && !_formKey.currentState!.validate()) {
      return {'success': false, 'error': 'Please fill in required fields'};
    }

    final lawyerData = {
      'name': _nameController.text,
      'bar_id': _barIdController.text,
      'state': _stateController.text,
    };

    return await _verificationService.verifyWithMockDigiLocker(lawyerData);
  }

  Future<Map<String, dynamic>> _submitManualVerification() async {
    if (!_formKey.currentState!.validate()) {
      return {'success': false, 'error': 'Please fill in required fields'};
    }

    final lawyerData = {
      'name': _nameController.text,
      'bar_id': _barIdController.text,
      'experience_years': _experienceController.text.isNotEmpty 
          ? int.tryParse(_experienceController.text) ?? 0 
          : 0,
      'specialization': _specializationController.text,
    };

    return await _verificationService.verifyManually(lawyerData);
  }

  String _getSubmitButtonText() {
    switch (_selectedMethod) {
      case 'ocr':
        return 'Process Certificate';
      case 'mock_digilocker':
        return 'Verify with DigiLocker (Demo)';
      case 'manual':
        return 'Submit for Review';
      default:
        return 'Submit Verification';
    }
  }

  void _clearResults() {
    setState(() {
      _verificationResult = null;
      _errorMessage = null;
    });
  }

  void _showSnackBar(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(message)),
    );
  }

  @override
  void dispose() {
    _nameController.dispose();
    _barIdController.dispose();
    _experienceController.dispose();
    _specializationController.dispose();
    _stateController.dispose();
    super.dispose();
  }
}