from django.urls import path
from .views import AttendanceListView

urlpatterns = [
    path('attendance/', AttendanceListView.as_view(), name='attendance-list'),
]
