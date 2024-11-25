from rest_framework.test import APITestCase
from rest_framework import status
from users.models import CustomUser
from courses.models import Course
from students.models import Student
from .models import Grade
from StudentManagementSystem.utils import BaseAPITestCase


class GradeAPITestCase(BaseAPITestCase):

    def setUp(self):
        self.teacher_user = CustomUser.objects.create_user(
            username="teacher", email="teacher@example.com", password="teacherpass", role="teacher"
        )
        self.student = Student.objects.create(name="John Doe", email="student@example.com", dob="2000-01-01")
        self.course = Course.objects.create(name="Math", description="Math Course", instructor=self.teacher_user)
        self.grade = Grade.objects.create(student=self.student, course=self.course, grade=90, teacher=self.teacher_user)

        self.access_token_teacher = self.get_access_token(self.teacher_user)

    def test_teacher_can_add_grade(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token_teacher}')
        response = self.client.post("/api/grades/", {
            "student": self.student.id,
            "course": self.course.id,
            "grade": 85
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Grade.objects.count(), 2)

    def test_update_grade(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token_teacher}')
        response = self.client.patch(f"/api/grades/{self.grade.id}/", {
            "grade": 95
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.grade.refresh_from_db()
        self.assertEqual(self.grade.grade, 95)
