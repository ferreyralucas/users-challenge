from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .factories import UserFactory


class UserViewSetTests(APITestCase):

    def setUp(self):
        # Create a regular user, a staff user and a superuser.
        self.regular_user = UserFactory()
        self.staff_user = UserFactory(is_staff=True)
        self.superuser = UserFactory(is_superuser=True)

    def get_user_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
