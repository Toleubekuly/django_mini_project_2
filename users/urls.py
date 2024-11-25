from django.urls import path, include
from .views import UserRoleUpdateView, UserCreateView, UserDeleteView

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('users/<int:pk>/role/', UserRoleUpdateView.as_view(), name='update-role'),
    path('users/', UserCreateView.as_view(), name='create-user'),
    path('users/<int:pk>/', UserDeleteView.as_view(), name='delete-user'),
]
