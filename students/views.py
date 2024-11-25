from django.core.cache import cache
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Student
from .serializers import StudentSerializer


class StudentListView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'email']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return Student.objects.filter(email=user.email)
        return super().get_queryset()

    def list(self, request, *args, **kwargs):
        cache_key = f"students_list_{request.user.id}_{request.GET.urlencode()}"
        cached_students = cache.get(cache_key)

        if cached_students:
            return Response(cached_students)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60 * 5)
        return response

    def retrieve(self, request, *args, **kwargs):
        cache_key = f"student_{request.user.id}"
        cached_profile = cache.get(cache_key)

        if cached_profile:
            return Response(cached_profile)

        response = super().retrieve(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60 * 5)
        return response
