from django.urls import path

from studios.views import StudioInfoView

from studios.views import ListbyDistanceView

app_name = 'studios'

urlpatterns = [
    path('<int:studio_id>/info/', StudioInfoView.as_view(), name='studio_info'),
    path('list/', ListbyDistanceView.as_view(), name='list'),
]
