from django.test import TestCase
from users.models import CustomUser


# class CustomUserModelTestCase(TestCase):
#     def setUp(self):
#         self.admin_user = CustomUser.objects.create_user(
#             username="admin", email="admin@example.com", password="adminpass", role="admin"
#         )
#         self.student_user = CustomUser.objects.create_user(
#             username="student", email="student@example.com", password="studentpass", role="student"
#         )
#
#     def test_user_creation(self):
#         self.assertEqual(self.admin_user.username, "admin")
#         self.assertEqual(self.admin_user.role, "admin")
#         self.assertEqual(self.student_user.role, "student")
#
#     def test_str_representation(self):
#         self.assertEqual(str(self.admin_user), "admin")
