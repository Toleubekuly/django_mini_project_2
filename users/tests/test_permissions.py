from rest_framework.test import APIRequestFactory, APITestCase
from users.models import CustomUser
from users.permissions import IsAdmin


class IsAdminPermissionTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.admin_user = CustomUser.objects.create_user(
            username="admin", email="admin@example.com", password="adminpass", role="admin"
        )
        self.student_user = CustomUser.objects.create_user(
            username="student", email="student@example.com", password="studentpass", role="student"
        )

    def test_admin_has_permission(self):
        request = self.factory.get("/some-endpoint/")
        request.user = self.admin_user
        permission = IsAdmin()
        self.assertTrue(permission.has_permission(request, None))

    def test_student_does_not_have_permission(self):
        request = self.factory.get("/some-endpoint/")
        request.user = self.student_user
        permission = IsAdmin()
        self.assertFalse(permission.has_permission(request, None))
