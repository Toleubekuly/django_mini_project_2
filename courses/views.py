from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Course, Enrollment
from .serializers import CourseSerializer, EnrollmentSerializer
from users.permissions import IsAdminOrTeacher
from django.core.cache import cache
import logging
from analytics.models import PopularCourse

logger = logging.getLogger('app')


class CourseListView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsAdminOrTeacher]

    def list(self, request, *args, **kwargs):
        cache_key = f"courses_{request.user.id}"
        cached_courses = cache.get(cache_key)

        if cached_courses:
            return Response(cached_courses)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60 * 5)
        return response

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)
        cache.delete(f"courses_{self.request.user.id}")

    def perform_update(self, serializer):
        super().perform_update(serializer)
        cache.delete(f"courses_{self.request.user.id}")


class EnrollmentListCreateView(generics.ListCreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrTeacher]

    def perform_create(self, serializer):
        serializer.save()
        logger.info(f"Enrollment created for student {serializer.validated_data['student']} in course {serializer.validated_data['course']}")


class CourseDetailView(APIView):
    def get(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        popular_course, created = PopularCourse.objects.get_or_create(course=course)
        popular_course.views += 1
        popular_course.save()

        serializer = CourseSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)

