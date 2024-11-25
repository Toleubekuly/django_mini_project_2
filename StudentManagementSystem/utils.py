from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase


class BaseAPITestCase(APITestCase):

    def get_access_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
