from django.urls import path

from classes.views import EnrollStudentsView, DropStudentsView, ClassHistoryView, ClassScheduleView

app_name = 'classes'

urlpatterns = [
    path('enroll/', EnrollStudentsView.as_view(), name='enroll_students'),
    path('drop/', DropStudentsView.as_view(), name='drop_students'),
    path('history/', ClassHistoryView.as_view(), name='class_history'),
    path('schedule/', ClassScheduleView.as_view(), name='class_schedule'),
]
