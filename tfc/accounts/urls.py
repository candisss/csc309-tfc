from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.views import RegisterView, EditProfileView

app_name = 'accounts'

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    path('edit/<int:pk>/', EditProfileView.as_view(), name='edit_profile'),
    # path('profile/', UserView.as_view(), name='profile'),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
