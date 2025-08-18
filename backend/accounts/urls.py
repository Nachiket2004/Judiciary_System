from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Test endpoints
    path('health/', views.health_check, name='health_check'),
    path('test/', views.test_endpoint, name='test_endpoint'),
    
    # Authentication endpoints (will be implemented in Task 2)
    # path('register/', views.RegisterView.as_view(), name='register'),
    # path('login/', views.LoginView.as_view(), name='login'),
    # path('logout/', views.LogoutView.as_view(), name='logout'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('profile/', views.ProfileView.as_view(), name='profile'),
    # path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
]