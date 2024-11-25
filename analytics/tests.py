from django.test import TestCase
from django.contrib.auth import get_user_model
from analytics.models import APIRequestLog
from courses.models import Course
from analytics.models import PopularCourse
from users.models import CustomUser
from StudentManagementSystem.utils import BaseAPITestCase

User = get_user_model()


class AnalyticsMiddlewareTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_api_request_logging(self):
        self.client.login(username='testuser', password='password')
        self.client.get('/api/some-endpoint/')
        self.assertEqual(APIRequestLog.objects.count(), 1)


class PopularCourseTestCase(BaseAPITestCase):
    def setUp(self):
        self.teacher = CustomUser.objects.create_user(
            username="teacher",
            email="teacher@example.com",
            password="teacherpass",
            role="teacher"
        )
        self.access_token_teacher = self.get_access_token(self.teacher)

        self.course = Course.objects.create(
            name="Test Course",
            description="Description",
            instructor=self.teacher
        )
        self.popular_course = PopularCourse.objects.create(course=self.course, views=0)

    def test_course_views(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token_teacher}')
        response = self.client.get(f'/api/courses/{self.course.id}/')
        self.assertEqual(response.status_code, 200)

        popular_course = PopularCourse.objects.get(course=self.course)
        self.assertEqual(popular_course.views, 1)

