from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.views import RegisterView, EditProfileView, PasswordResetView

app_name = 'accounts'

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('edit/<int:pk>/', EditProfileView.as_view(), name='edit_profile'),
    path('password/<int:pk>/', PasswordResetView.as_view(), name='reset_password')
]
