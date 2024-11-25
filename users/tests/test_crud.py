from rest_framework import status
from users.models import CustomUser
from StudentManagementSystem.utils import BaseAPITestCase


class UserCRUDTestCase(BaseAPITestCase):
    def setUp(self):
        self.admin_user = CustomUser.objects.create_user(
            username="admin", email="admin@example.com", password="adminpass", role="admin"
        )
        self.access_token_admin = self.get_access_token(self.admin_user)

    def test_admin_can_create_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token_admin}')
        response = self.client.post("/api/users/", {
            "username": "new_user",
            "email": "newuser@example.com",
            "password": "newuserpass",
            "role": "student"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.filter(username="new_user").count(), 1)

    def test_admin_can_delete_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token_admin}')
        student_user = CustomUser.objects.create_user(
            username="student", email="student@example.com", password="studentpass", role="student"
        )
        response = self.client.delete(f"/api/users/{student_user.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CustomUser.objects.filter(id=student_user.id).count(), 0)
