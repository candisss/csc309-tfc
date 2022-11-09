from django.urls import path

from tfc.accounts.views import LoginView, RegisterView, UserView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserView.as_view(), name='profile')
]
