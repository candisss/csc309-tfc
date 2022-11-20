from django.template.defaulttags import url
from django.urls import include, path
from rest_framework import routers

from studios.views import StudioInfoView

from studios.views import ListbyDistanceView, StudioSearchFilterView

from studios.models import Studio

app_name = 'studios'

# router = routers.DefaultRouter()
# router.register(r'search', StudioSearchFilterView)

urlpatterns = [
    path('<int:studio_id>/info/', StudioInfoView.as_view(), name='studio_info'),
    path('list/', ListbyDistanceView.as_view(), name='list'),
    path('search/', StudioSearchFilterView.as_view(), name='search'),
]
