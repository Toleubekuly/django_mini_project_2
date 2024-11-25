from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Grade
from .serializers import GradeSerializer
from users.permissions import IsAdminOrTeacher
from notifications.tasks import notify_grade_update
import logging

logger = logging.getLogger('app')


class GradeListView(generics.ListCreateAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated, IsAdminOrTeacher]

    def perform_create(self, serializer):
        instance = serializer.save(teacher=self.request.user)
        logger.info(f"Grade created: Student {instance.student.name}, Course {instance.course.name}, Grade {instance.grade}, Teacher {self.request.user.username}")
        notify_grade_update.delay(instance.student.id, instance.course.name, instance.grade)


class GradeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated, IsAdminOrTeacher]

    def perform_update(self, serializer):
        instance = serializer.save()
        logger.info(f"Grade updated: Student {instance.student.name}, Course {instance.course.name}, Grade {instance.grade}, Teacher {instance.teacher.username}")
        notify_grade_update.delay(instance.student.id, instance.course.name, instance.grade)
