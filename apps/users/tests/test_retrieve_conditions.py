from django.urls import reverse

from rest_framework import status

from .factories import UserFactory
from .test_base_user_view import UserViewSetTests


class RetrieveUserViewSetTests(UserViewSetTests):
    """
    This class tests the retrieve conditions for the UserViewSet specified in the challenge.
    """

    def test_retrieve_own_user_as_regular_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.get_user_token(self.regular_user)}')
        url = reverse('users-detail', kwargs={'pk': self.regular_user.pk})
        response = self.client.get(url)

        # Regular users should be able to retrieve their own data with full information.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('email', response.data)

    def test_retrieve_other_user_as_regular_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.get_user_token(self.regular_user)}')
        other_user = UserFactory()
        url = reverse('users-detail', kwargs={'pk': other_user.pk})
        response = self.client.get(url)

        # Non-staff users requesting someone else's uuid will only see limited information.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('email', response.data)

    def test_retrieve_own_user_as_staff_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.get_user_token(self.staff_user)}')
        url = reverse('users-detail', kwargs={'pk': self.staff_user.pk})
        response = self.client.get(url)

        # Staff users should be able to retrieve their own data with full information.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('email', response.data)

    def test_retrieve_other_user_as_staff_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.get_user_token(self.staff_user)}')
        other_user = UserFactory()
        url = reverse('users-detail', kwargs={'pk': other_user.pk})
        response = self.client.get(url)

        # Staff users should be able to retrieve other user's data with full information.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('email', response.data)

    def test_retrieve_other_user_as_superuser(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.get_user_token(self.superuser)}')
        other_user = UserFactory()
        url = reverse('users-detail', kwargs={'pk': other_user.pk})
        response = self.client.get(url)

        # Superusers should be able to retrieve other user's data with full information.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('email', response.data)

    def test_list_users_as_staff_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.get_user_token(self.staff_user)}')
        url = reverse('users-list')
        response = self.client.get(url)

        # Staff users should be able to list all users.
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_users_as_superuser(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.get_user_token(self.superuser)}')
        url = reverse('users-list')
        response = self.client.get(url)

        # Superusers should be able to list all users.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
