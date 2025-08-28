from django.urls import path
from . import views

app_name = 'lawyers'

urlpatterns = [
    # Verification endpoints
    path('verify/ocr/', views.verify_lawyer_ocr, name='verify_ocr'),
    path('verify/mock-digilocker/', views.verify_lawyer_mock_digilocker, name='verify_mock_digilocker'),
    path('verify/manual/', views.verify_lawyer_manual, name='verify_manual'),
    path('verification/status/', views.get_verification_status, name='verification_status'),
    
    # Admin verification management
    path('admin/verifications/pending/', views.get_pending_verifications, name='pending_verifications'),
    path('admin/verifications/<int:verification_id>/review/', views.review_verification, name='review_verification'),
    
    # Lawyer profile management
    path('profile/', views.get_lawyer_profile, name='get_profile'),
    path('profile/update/', views.update_lawyer_profile, name='update_profile'),
    
    # Public lawyer search
    path('search/', views.search_lawyers, name='search_lawyers'),
]