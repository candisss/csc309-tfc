from django.urls import include, path

from studios.views import StudioInfoView

from studios.views import ListbyDistanceView, StudioSearchFilterView


app_name = 'studios'

urlpatterns = [
    path('<int:studio_id>/info/', StudioInfoView.as_view(), name='studio_info'),
    path('list/', ListbyDistanceView.as_view(), name='list'),
    path('search/', StudioSearchFilterView.as_view(), name='search'),
]
