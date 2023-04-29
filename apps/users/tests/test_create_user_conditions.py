from django.urls import reverse
from rest_framework import status
from .test_base_user_view import UserViewSetTests
from unittest import mock


class CreateUserViewSetTests(UserViewSetTests):
    """
    This class tests the create conditions for the UserViewSet specified in the challenge.
    """

    def test_create_user_as_regular_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.get_user_token(self.regular_user)}')
        url = reverse('users-list')
        data = {
            "username": "new_user",
            "email": "new_user@example.com",
            "password": "strong_password",
            "repeat_password": "strong_password",
        }
        response = self.client.post(url, data)

        # Regular users should not be able to create new users.
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_as_staff_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.get_user_token(self.staff_user)}')
        url = reverse('users-list')
        data = {
            "username": "new_user_2",
            "email": "new_user_2@example.com",
            "password": "Astrong_password_!1",
            "repeat_password": "Astrong_password_!1",
            "groups": "regular_user",
        }
        response = self.client.post(url, data)

        # Staff users should be able to create new users.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_as_superuser(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.get_user_token(self.superuser)}')
        url = reverse('users-list')
        data = {
            "username": "new_user_2",
            "email": "new_user_2@example.com",
            "password": "Astrong_password_!1",
            "repeat_password": "Astrong_password_!1",
            "groups": "regular_user",
        }
        response = self.client.post(url, data)

        # Superusers should be able to create new users.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_with_mismatched_passwords(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.get_user_token(self.staff_user)}')
        url = reverse('users-list')
        data = {
            "username": "new_user_3",
            "email": "new_user_3@example.com",
            "password": "Astrong_password_!1",
            "repeat_password": "Astrong_password_!2",
        }
        response = self.client.post(url, data)

        # Make sure both passwords match (or 400 BAD REQUEST).
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_weak_password(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.get_user_token(self.staff_user)}')
        url = reverse('users-list')
        data = {
            "username": "new_user_4",
            "email": "new_user_4@example.com",
            "password": "weakpass",
            "repeat_password": "weakpass",
        }
        response = self.client.post(url, data)

        # Password must include lowercase and uppercase letters, digits, and symbols. At least 8 chars (or 400 BAD REQUEST).
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @mock.patch('apps.users.services.subscription.SubscriptionService')
    def test_create_user_with_groups_and_mocked_subscription(self, mock_subscription_service):
        mock_subscription_service.get_subscription.return_value = {'subscription': 'active'}

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.get_user_token(self.staff_user)}')
        url = reverse('users-list')
        data = {
            "username": "new_user_5",
            "email": "new_user_5@example.com",
            "password": "Astrong_password_!1",
            "repeat_password": "Astrong_password_!1",
            "groups": [
                "sales",
                "support",
            ]
        }

        response = self.client.post(url, data)

        # Successful response must return the serialized user.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('subscription', response.data)
        self.assertEqual(response.data['subscription'], 'active')
        self.assertIn('groups', response.data)
        self.assertEqual(len(response.data['groups']), 2)
