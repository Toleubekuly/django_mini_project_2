from rest_framework import status
from users.models import CustomUser
from courses.models import Course, Enrollment
from students.models import Student
from django.core.cache import cache
from StudentManagementSystem.utils import BaseAPITestCase


class CourseAPITestCase(BaseAPITestCase):
    def setUp(self):
        self.teacher_user = CustomUser.objects.create_user(
            username="teacher", email="diwer79549@merotx.com", password="teacherpass", role="teacher"
        )
        self.student_user = CustomUser.objects.create_user(
            username="student", email="diwer79549@merotx.com", password="studentpass", role="student"
        )

        self.access_token_teacher = self.get_access_token(self.teacher_user)
        self.access_token_student = self.get_access_token(self.student_user)

        self.course = Course.objects.create(
            name="Math",
            description="Math Course",
            instructor=self.teacher_user
        )

    def test_teacher_can_create_course(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token_teacher}')
        response = self.client.post("/api/courses/", {
            "name": "Science",
            "description": "Science Course",
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_non_teacher_cannot_create_course(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token_student}')
        response = self.client.post("/api/courses/", {
            "name": "Science",
            "description": "Science Course",
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_teacher_can_update_course(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token_teacher}')
        response = self.client.patch(f"/api/courses/{self.course.id}/", {
            "description": "Updated Math Course",
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(self.course.description, "Updated Math Course")

    def test_non_teacher_cannot_update_course(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token_student}')
        response = self.client.patch(f"/api/courses/{self.course.id}/", {
            "description": "Updated Math Course",
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_teacher_can_delete_course(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token_teacher}')
        response = self.client.delete(f"/api/courses/{self.course.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Course.objects.filter(id=self.course.id).exists())

    def test_non_teacher_cannot_delete_course(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token_student}')
        response = self.client.delete(f"/api/courses/{self.course.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_caching_for_course_list(self):
        cache_key = f"courses_{self.teacher_user.id}"
        cache.clear()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token_teacher}')
        response = self.client.get("/api/courses/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(cache.get(cache_key))
        response = self.client.get("/api/courses/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class EnrowllmentAPITestCase(BaseAPITestCase):
    def setUp(self):
        self.teacher_user = CustomUser.objects.create_user(
            username="teacher", email="teacher@example.com", password="teacherpass", role="teacher"
        )
        self.student_user = CustomUser.objects.create_user(
            username="student", email="student@example.com", password="studentpass", role="student"
        )
        self.access_token_teacher = self.get_access_token(self.teacher_user)
        self.access_token_student = self.get_access_token(self.student_user)

        self.student = Student.objects.create(
            name="John Doe",
            email="student@example.com",
            dob="2000-01-01"
        )

        self.course = Course.objects.create(
            name="Math",
            description="Math Course",
            instructor=self.teacher_user
        )

    def test_teacher_can_create_enrollment(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token_teacher}')
        response = self.client.post("/api/enrollments/", {
            "student": self.student.id,
            "course": self.course.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Enrollment.objects.count(), 1)

    def test_student_cannot_create_enrollment(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token_student}')
        response = self.client.post("/api/enrollments/", {
            "student": self.student.id,
            "course": self.course.id
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_teacher_cannot_duplicate_enrollment(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token_teacher}')
        Enrollment.objects.create(student=self.student, course=self.course)
        response = self.client.post("/api/enrollments/", {
            "student": self.student.id,
            "course": self.course.id
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_enrollment_list_retrieval(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token_teacher}')
        Enrollment.objects.create(student=self.student, course=self.course)
        response = self.client.get("/api/enrollments/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

