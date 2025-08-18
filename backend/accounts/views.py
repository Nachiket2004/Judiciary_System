from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import JsonResponse


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Simple health check endpoint for testing
    """
    return Response({
        'status': 'healthy',
        'message': 'Django backend is running successfully!',
        'version': '1.0.0'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def test_endpoint(request):
    """
    Test endpoint to verify API is working
    """
    return JsonResponse({
        'message': 'API is working correctly',
        'method': request.method,
        'path': request.path,
        'user_authenticated': request.user.is_authenticated,
    })