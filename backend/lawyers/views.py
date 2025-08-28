from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_http_methods

from .models import Lawyer, LawyerVerification, Case
from .services import OCRVerificationService, MockDigiLockerService, ManualVerificationService
from .serializers import LawyerSerializer, VerificationSerializer, CaseSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_lawyer_ocr(request):
    """
    OCR-based lawyer verification endpoint
    """
    try:
        # Get or create lawyer profile
        lawyer, created = Lawyer.objects.get_or_create(
            user=request.user,
            defaults={'specialization': 'General Practice'}
        )
        
        # Check if certificate file is provided
        if 'certificate' not in request.FILES:
            return Response({
                'error': 'Certificate file is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        certificate_file = request.FILES['certificate']
        
        # Process certificate using OCR service
        ocr_service = OCRVerificationService()
        result = ocr_service.process_certificate(certificate_file, lawyer)
        
        if result['success']:
            return Response({
                'message': result['message'],
                'verification_id': result['verification_id'],
                'extracted_data': result['extracted_data'],
                'confidence': result['confidence'],
                'requires_admin_review': True
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': result['error'],
                'message': result.get('message', 'Processing failed')
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'error': str(e),
            'message': 'An unexpected error occurred'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_lawyer_mock_digilocker(request):
    """
    Mock DigiLocker verification endpoint for demonstration
    """
    try:
        # Get or create lawyer profile
        lawyer, created = Lawyer.objects.get_or_create(
            user=request.user,
            defaults={'specialization': 'General Practice'}
        )
        
        lawyer_data = request.data
        
        # Validate required fields
        required_fields = ['name', 'bar_id']
        for field in required_fields:
            if not lawyer_data.get(field):
                return Response({
                    'error': f'Missing required field: {field}'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Process using mock DigiLocker service
        mock_service = MockDigiLockerService()
        result = mock_service.simulate_verification(lawyer_data, lawyer)
        
        if result['success']:
            return Response({
                'message': result['message'],
                'verification_id': result['verification_id'],
                'extracted_data': result['extracted_data'],
                'demo_mode': result['demo_mode'],
                'requires_admin_review': False  # Auto-approved for demo
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': result['error'],
                'message': result.get('message', 'Mock verification failed')
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'error': str(e),
            'message': 'An unexpected error occurred'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_lawyer_manual(request):
    """
    Manual lawyer verification endpoint
    """
    try:
        # Get or create lawyer profile
        lawyer, created = Lawyer.objects.get_or_create(
            user=request.user,
            defaults={'specialization': 'General Practice'}
        )
        
        lawyer_data = request.data
        
        # Process using manual verification service
        manual_service = ManualVerificationService()
        result = manual_service.create_manual_verification(lawyer_data, lawyer)
        
        if result['success']:
            return Response({
                'message': result['message'],
                'verification_id': result['verification_id'],
                'extracted_data': result['extracted_data'],
                'requires_admin_review': True
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': result['error'],
                'message': result.get('message', 'Manual verification failed')
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'error': str(e),
            'message': 'An unexpected error occurred'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_verification_status(request):
    """
    Get current user's verification status
    """
    try:
        lawyer = get_object_or_404(Lawyer, user=request.user)
        
        # Get latest verification attempts
        verifications = LawyerVerification.objects.filter(
            lawyer=lawyer
        ).order_by('-created_at')[:5]
        
        verification_data = []
        for verification in verifications:
            verification_data.append({
                'id': verification.id,
                'method': verification.get_method_display(),
                'status': verification.get_status_display(),
                'confidence': verification.confidence_score,
                'created_at': verification.created_at,
                'admin_comments': verification.admin_comments,
                'extracted_data': verification.extracted_data
            })
        
        return Response({
            'is_verified': lawyer.is_verified,
            'verification_date': lawyer.verification_date,
            'bar_id': lawyer.bar_id,
            'recent_verifications': verification_data
        }, status=status.HTTP_200_OK)
        
    except Lawyer.DoesNotExist:
        return Response({
            'is_verified': False,
            'recent_verifications': []
        }, status=status.HTTP_200_OK)


# Admin Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_pending_verifications(request):
    """
    Get all pending lawyer verifications for admin review
    """
    if not request.user.is_staff and request.user.role != 'admin':
        return Response({
            'error': 'Admin access required'
        }, status=status.HTTP_403_FORBIDDEN)
    
    verifications = LawyerVerification.objects.filter(
        status='pending'
    ).select_related('lawyer__user').order_by('-created_at')
    
    verification_data = []
    for verification in verifications:
        verification_data.append({
            'id': verification.id,
            'lawyer_name': verification.lawyer.user.get_full_name(),
            'lawyer_email': verification.lawyer.user.email,
            'method': verification.get_method_display(),
            'confidence': verification.confidence_score,
            'extracted_data': verification.extracted_data,
            'created_at': verification.created_at,
            'uploaded_document': verification.uploaded_document.url if verification.uploaded_document else None
        })
    
    return Response({
        'pending_verifications': verification_data,
        'total_count': len(verification_data)
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def review_verification(request, verification_id):
    """
    Approve or reject lawyer verification
    """
    if not request.user.is_staff and request.user.role != 'admin':
        return Response({
            'error': 'Admin access required'
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        verification = get_object_or_404(LawyerVerification, id=verification_id)
        
        action = request.data.get('action')  # 'approve' or 'reject'
        comments = request.data.get('comments', '')
        
        if action not in ['approve', 'reject']:
            return Response({
                'error': 'Invalid action. Must be "approve" or "reject"'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if action == 'approve':
            verification.approve(request.user, comments)
            message = 'Verification approved successfully'
        else:
            verification.reject(request.user, comments)
            message = 'Verification rejected'
        
        # TODO: Send email notification to lawyer
        # send_verification_notification(verification)
        
        return Response({
            'message': message,
            'verification_id': verification.id,
            'status': verification.status
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': str(e),
            'message': 'Failed to process verification review'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_lawyer_profile(request):
    """
    Get current user's lawyer profile
    """
    try:
        lawyer = get_object_or_404(Lawyer, user=request.user)
        serializer = LawyerSerializer(lawyer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Lawyer.DoesNotExist:
        return Response({
            'error': 'Lawyer profile not found'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_lawyer_profile(request):
    """
    Update current user's lawyer profile
    """
    try:
        lawyer = get_object_or_404(Lawyer, user=request.user)
        serializer = LawyerSerializer(lawyer, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    except Lawyer.DoesNotExist:
        return Response({
            'error': 'Lawyer profile not found'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def search_lawyers(request):
    """
    Search for verified lawyers with filters
    """
    # Get query parameters
    name = request.GET.get('name', '')
    specialization = request.GET.get('specialization', '')
    location = request.GET.get('location', '')
    min_experience = request.GET.get('min_experience', 0)
    
    # Build query
    lawyers = Lawyer.objects.filter(is_verified=True)
    
    if name:
        lawyers = lawyers.filter(user__first_name__icontains=name) | lawyers.filter(user__last_name__icontains=name)
    
    if specialization:
        lawyers = lawyers.filter(specialization__icontains=specialization)
    
    if location:
        lawyers = lawyers.filter(location__icontains=location)
    
    if min_experience:
        lawyers = lawyers.filter(experience_years__gte=int(min_experience))
    
    # Serialize results
    serializer = LawyerSerializer(lawyers, many=True)
    
    return Response({
        'lawyers': serializer.data,
        'total_count': lawyers.count()
    }, status=status.HTTP_200_OK)