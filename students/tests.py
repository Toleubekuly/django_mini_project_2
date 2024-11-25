from rest_framework.test import APITestCase
from rest_framework import status
from users.models import CustomUser
from .models import Student
from StudentManagementSystem.utils import BaseAPITestCase


class StudentAPITestCase(BaseAPITestCase):

    def setUp(self):
        self.student_user = CustomUser.objects.create_user(
            username="student", email="student@example.com", password="studentpass", role="student"
        )
        self.teacher_user = CustomUser.objects.create_user(
            username="teacher", email="teacher@example.com", password="teacherpass", role="teacher"
        )
        self.student = Student.objects.create(name="John Doe", email="student@example.com", dob="2000-01-01")

        self.access_token_student = self.get_access_token(self.student_user)
        self.access_token_teacher = self.get_access_token(self.teacher_user)

    def test_student_can_view_own_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token_student}')
        response = self.client.get("/api/students/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)  # Проверяем количество записей в 'results'
        self.assertEqual(response.data["results"][0]["email"], "student@example.com")

    def test_teacher_can_view_all_students(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token_teacher}')
        response = self.client.get("/api/students/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)


class StudentFilterAndPaginationTest(BaseAPITestCase):

    def setUp(self):
        self.admin_user = CustomUser.objects.create_user(
            username="admin", email="admin@example.com", password="adminpass", role="admin"
        )
        for i in range(15):
            Student.objects.create(name=f"Student {i}", email=f"student{i}@example.com", dob="2000-01-01")

        self.access_token_admin = self.get_access_token(self.admin_user)

    def test_pagination(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token_admin}')
        response = self.client.get("/api/students/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)  # Default PAGE_SIZE

    def test_filtering(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token_admin}')
        response = self.client.get("/api/students/?name=Student 1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "Student 1")
