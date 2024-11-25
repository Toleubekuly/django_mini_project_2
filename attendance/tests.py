from rest_framework.test import APITestCase
from rest_framework import status
from users.models import CustomUser
from courses.models import Course
from students.models import Student
from .models import Attendance
from StudentManagementSystem.utils import BaseAPITestCase


class AttendanceAPITestCase(BaseAPITestCase):

    def setUp(self):
        self.teacher_user = CustomUser.objects.create_user(
            username="teacher", email="teacher@example.com", password="teacherpass", role="teacher"
        )
        self.student = Student.objects.create(name="John Doe", email="student@example.com", dob="2000-01-01")
        self.course = Course.objects.create(name="Math", description="Math Course", instructor=self.teacher_user)
        self.attendance = Attendance.objects.create(student=self.student, course=self.course, status="present")
        self.access_token = self.get_access_token(self.teacher_user)

    def test_teacher_can_mark_attendance(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        response = self.client.post("/api/attendance/", {
            "student": self.student.id,
            "course": self.course.id,
            "status": "late"
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Attendance.objects.count(), 2)

