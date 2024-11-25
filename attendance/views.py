from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Attendance
from .serializers import AttendanceSerializer
from users.permissions import IsAdminOrTeacher
import logging

logger = logging.getLogger('app')

class AttendanceListView(generics.ListCreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated, IsAdminOrTeacher]

    def perform_create(self, serializer):
        instance = serializer.save()
        logger.info(f"Attendance created: Student {instance.student.name}, Course {instance.course.name}, Status {instance.status}")

    def perform_update(self, serializer):
        instance = serializer.save()
        logger.info(f"Attendance updated: Student {instance.student.name}, Course {instance.course.name}, Status {instance.status}")
