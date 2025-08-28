import os
import re
import uuid
import tempfile
from typing import Dict, Optional, Tuple
from PIL import Image
import pytesseract
from django.core.files.uploadedfile import UploadedFile
from django.conf import settings
from django.utils import timezone
from .models import LawyerVerification


class OCRVerificationService:
    """
    Service for processing lawyer certificates using OCR
    """
    
    def __init__(self):
        # Configure tesseract path if specified in settings
        if hasattr(settings, 'TESSERACT_CMD'):
            pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD
    
    def process_certificate(self, uploaded_file: UploadedFile, lawyer) -> Dict:
        """
        Process uploaded certificate and extract lawyer information
        """
        try:
            # Validate file
            validation_result = self._validate_file(uploaded_file)
            if not validation_result['valid']:
                return {
                    'success': False,
                    'error': validation_result['error']
                }
            
            # Save file temporarily
            temp_path = self._save_temp_file(uploaded_file)
            
            try:
                # Extract text using OCR
                extracted_text = self._extract_text_from_image(temp_path)
                
                # Parse lawyer information
                parsed_info = self._parse_certificate_text(extracted_text)
                
                # Create verification record
                verification = LawyerVerification.objects.create(
                    lawyer=lawyer,
                    method='ocr',
                    status='pending',
                    extracted_data=parsed_info,
                    raw_ocr_text=extracted_text,
                    confidence_score=parsed_info.get('confidence', 'medium')
                )
                
                # Save uploaded document
                verification.uploaded_document.save(
                    f"cert_{lawyer.id}_{uuid.uuid4().hex[:8]}.{uploaded_file.name.split('.')[-1]}",
                    uploaded_file,
                    save=True
                )
                
                return {
                    'success': True,
                    'verification_id': verification.id,
                    'extracted_data': parsed_info,
                    'raw_text': extracted_text,
                    'confidence': parsed_info.get('confidence', 'medium'),
                    'message': 'Certificate processed successfully. Pending admin review.'
                }
                
            finally:
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                    
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to process certificate. Please try again or use manual verification.'
            }
    
    def _validate_file(self, uploaded_file: UploadedFile) -> Dict:
        """Validate uploaded file type and size"""
        # Check file size (10MB limit)
        max_size = 10 * 1024 * 1024  # 10MB
        if uploaded_file.size > max_size:
            return {'valid': False, 'error': 'File size exceeds 10MB limit'}
        
        # Check file type
        allowed_types = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png']
        if uploaded_file.content_type not in allowed_types:
            return {'valid': False, 'error': 'Invalid file type. Please upload PDF, JPG, or PNG files.'}
        
        # Check file extension
        allowed_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        if file_extension not in allowed_extensions:
            return {'valid': False, 'error': 'Invalid file extension'}
        
        return {'valid': True}
    
    def _save_temp_file(self, uploaded_file: UploadedFile) -> str:
        """Save uploaded file to temporary location"""
        # Create temporary file
        temp_fd, temp_path = tempfile.mkstemp(suffix=f".{uploaded_file.name.split('.')[-1]}")
        
        try:
            with os.fdopen(temp_fd, 'wb') as temp_file:
                for chunk in uploaded_file.chunks():
                    temp_file.write(chunk)
        except:
            os.close(temp_fd)
            raise
        
        return temp_path
    
    def _extract_text_from_image(self, image_path: str) -> str:
        """Extract text from image using OCR"""
        try:
            # Handle PDF files (convert first page to image)
            if image_path.lower().endswith('.pdf'):
                # For PDF files, you might want to use pdf2image library
                # For now, we'll assume it's an image file
                pass
            
            # Open and preprocess image
            image = Image.open(image_path)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Enhance image quality for better OCR
            # You can add image preprocessing here (resize, contrast, etc.)
            
            # Extract text using tesseract
            custom_config = r'--oem 3 --psm 6'  # OCR Engine Mode 3, Page Segmentation Mode 6
            text = pytesseract.image_to_string(image, lang='eng', config=custom_config)
            
            return text.strip()
            
        except Exception as e:
            raise Exception(f"OCR processing failed: {str(e)}")
    
    def _parse_certificate_text(self, text: str) -> Dict:
        """Parse lawyer information from extracted certificate text"""
        parsed_info = {
            'confidence': 'low'
        }
        
        # Patterns for extracting information
        patterns = {
            'name': [
                r'Name\\s*:?\\s*([A-Za-z\\s\\.]+?)(?:\\n|$)',
                r'Advocate\\s+([A-Za-z\\s\\.]+?)(?:\\n|$)',
                r'Mr\\.?\\s*([A-Za-z\\s\\.]+?)(?:\\n|$)',
                r'Ms\\.?\\s*([A-Za-z\\s\\.]+?)(?:\\n|$)',
                r'Shri\\s+([A-Za-z\\s\\.]+?)(?:\\n|$)',
                r'Smt\\.?\\s*([A-Za-z\\s\\.]+?)(?:\\n|$)'
            ],
            'bar_id': [
                r'Bar\\s+(?:Council\\s+)?(?:Registration\\s+)?(?:No\\.?|Number)\\s*:?\\s*([A-Z0-9\\/\\-]+)',
                r'Registration\\s+(?:No\\.?|Number)\\s*:?\\s*([A-Z0-9\\/\\-]+)',
                r'Enrolment\\s+(?:No\\.?|Number)\\s*:?\\s*([A-Z0-9\\/\\-]+)',
                r'Enrollment\\s+(?:No\\.?|Number)\\s*:?\\s*([A-Z0-9\\/\\-]+)',
                r'(?:BAR|Bar)\\s*[/\\-]?\\s*([A-Z0-9\\/\\-]+)',
            ],
            'registration_date': [
                r'Date\\s+of\\s+(?:Registration|Enrolment|Enrollment)\\s*:?\\s*(\\d{1,2}[\\-\\/]\\d{1,2}[\\-\\/]\\d{2,4})',
                r'Registered\\s+on\\s*:?\\s*(\\d{1,2}[\\-\\/]\\d{1,2}[\\-\\/]\\d{2,4})',
                r'(?:Registration|Enrolment|Enrollment)\\s+Date\\s*:?\\s*(\\d{1,2}[\\-\\/]\\d{1,2}[\\-\\/]\\d{2,4})'
            ],
            'state_bar_council': [
                r'([A-Za-z\\s]+)\\s+Bar\\s+Council',
                r'State\\s*:?\\s*([A-Za-z\\s]+)',
                r'Bar\\s+Council\\s+of\\s+([A-Za-z\\s]+)'
            ]
        }
        
        confidence_score = 0
        total_fields = len(patterns)
        
        # Extract information using patterns
        for field, field_patterns in patterns.items():
            for pattern in field_patterns:
                match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
                if match:
                    extracted_value = match.group(1).strip()
                    # Clean up extracted value
                    extracted_value = re.sub(r'\\s+', ' ', extracted_value)
                    extracted_value = extracted_value.strip('.,;:')
                    
                    if extracted_value and len(extracted_value) > 1:
                        parsed_info[field] = extracted_value
                        confidence_score += 1
                        break
        
        # Calculate confidence based on extracted fields
        confidence_ratio = confidence_score / total_fields
        if confidence_ratio >= 0.75:
            parsed_info['confidence'] = 'high'
        elif confidence_ratio >= 0.5:
            parsed_info['confidence'] = 'medium'
        else:
            parsed_info['confidence'] = 'low'
        
        # Add extraction metadata
        parsed_info['extraction_timestamp'] = timezone.now().isoformat()
        parsed_info['fields_extracted'] = confidence_score
        parsed_info['total_fields'] = total_fields
        
        return parsed_info
    
    def validate_extracted_data(self, extracted_data: Dict) -> Tuple[bool, str]:
        """Validate extracted lawyer data"""
        required_fields = ['name', 'bar_id']
        missing_fields = []
        
        for field in required_fields:
            if not extracted_data.get(field):
                missing_fields.append(field)
        
        if missing_fields:
            return False, f"Missing required fields: {', '.join(missing_fields)}"
        
        # Validate Bar ID format (basic validation)
        bar_id = extracted_data.get('bar_id', '')
        if not re.match(r'^[A-Z0-9\\/\\-]+$', bar_id):
            return False, "Invalid Bar ID format"
        
        # Validate name (should contain only letters, spaces, and dots)
        name = extracted_data.get('name', '')
        if not re.match(r'^[A-Za-z\\s\\.]+$', name):
            return False, "Invalid name format"
        
        return True, "Validation successful"


class MockDigiLockerService:
    """
    Mock DigiLocker service for demonstration purposes
    """
    
    def simulate_verification(self, lawyer_data: Dict, lawyer) -> Dict:
        """Simulate DigiLocker verification process"""
        try:
            # Simulate processing delay
            import time
            time.sleep(1)  # Simulate API call delay
            
            # Generate mock certificate data
            mock_data = {
                'name': lawyer_data.get('name', 'Demo Lawyer'),
                'bar_id': f"BAR/{lawyer_data.get('bar_id', '12345')}/2023",
                'registration_date': '2020-01-15',
                'state_bar_council': lawyer_data.get('state', 'Delhi') + ' Bar Council',
                'status': 'Active',
                'specialization': lawyer_data.get('specialization', 'General Practice'),
                'confidence': 'high',
                'demo_mode': True
            }
            
            # Create verification record (auto-approved for demo)
            verification = LawyerVerification.objects.create(
                lawyer=lawyer,
                method='mock_digilocker',
                status='approved',  # Auto-approve for demo
                extracted_data=mock_data,
                confidence_score='high',
                reviewed_at=timezone.now()
            )
            
            # Update lawyer profile immediately for demo
            lawyer.is_verified = True
            lawyer.verification_date = timezone.now()
            lawyer.bar_id = mock_data['bar_id']
            if 'specialization' in mock_data:
                lawyer.specialization = mock_data['specialization']
            lawyer.save()
            
            return {
                'success': True,
                'verification_id': verification.id,
                'extracted_data': mock_data,
                'message': 'DigiLocker verification successful (Demo Mode)',
                'demo_mode': True
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Mock DigiLocker verification failed'
            }


class ManualVerificationService:
    """
    Service for manual lawyer verification
    """
    
    def create_manual_verification(self, lawyer_data: Dict, lawyer) -> Dict:
        """Create manual verification request"""
        try:
            # Validate required fields
            required_fields = ['name', 'bar_id']
            for field in required_fields:
                if not lawyer_data.get(field):
                    return {
                        'success': False,
                        'error': f'Missing required field: {field}'
                    }
            
            # Create verification record
            verification = LawyerVerification.objects.create(
                lawyer=lawyer,
                method='manual',
                status='pending',
                extracted_data=lawyer_data,
                confidence_score='medium'  # Manual entries get medium confidence
            )
            
            return {
                'success': True,
                'verification_id': verification.id,
                'extracted_data': lawyer_data,
                'message': 'Manual verification submitted. Admin will review within 24-48 hours.'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to submit manual verification'
            }