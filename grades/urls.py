from django.urls import path
from .views import GradeListView, GradeDetailView

urlpatterns = [
    path('grades/', GradeListView.as_view(), name='grade-list'),
    path('grades/<int:pk>/', GradeDetailView.as_view(), name='grade-detail'),
]
