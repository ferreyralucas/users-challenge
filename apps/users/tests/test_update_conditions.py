from django.urls import reverse

from rest_framework import status

from .test_base_user_view import UserViewSetTests


class UpdateUserViewSetTests(UserViewSetTests):
    """
    This class tests the update conditions for the UserViewSet specified in the challenge.
    """

    def test_update_user_as_self(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.get_user_token(self.regular_user)}')
        url = reverse('users-detail', kwargs={'pk': self.regular_user.id})
        data = {
            "username": "updated_user",
            "email": "updated_user@example.com",
        }
        response = self.client.put(url, data)

        # Users should be able to update their own information.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'updated_user')
        self.assertEqual(response.data['email'], 'updated_user@example.com')

    def test_update_user_as_staff_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.get_user_token(self.staff_user)}')
        url = reverse('users-detail', kwargs={'pk': self.regular_user.id})
        data = {
            "username": "updated_user_2",
            "email": "updated_user_2@example.com",
            "groups": "regular_user",
        }
        response = self.client.put(url, data)

        # Staff users should be able to update other users' information.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'updated_user_2')
        self.assertEqual(response.data['email'], 'updated_user_2@example.com')

    def test_update_user_password_as_self_with_old_password(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.get_user_token(self.regular_user)}')
        url = reverse('users-detail', kwargs={'pk': self.regular_user.pk})

        data = {
            'username': self.regular_user.username,
            'email': self.regular_user.email,
            'old_password': 'regular_password',
            'new_password': 'new_password',
        }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Users should be able to update their own password if they provide the old password.
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_password_as_self_without_old_password(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.get_user_token(self.regular_user)}')
        url = reverse('users-detail', kwargs={'pk': self.regular_user.id})
        data = {
            "password": "Anew_password_!1",
        }
        response = self.client.put(url, data)

        # Users should not be able to update their own password without providing the old password.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user_password_as_staff_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.get_user_token(self.staff_user)}')
        url = reverse('users-detail', kwargs={'pk': self.regular_user.id})
        data = {
            "email": self.regular_user.email,
            "username": self.regular_user.username,
            "password": "Anew_password_!1",
            "groups": "regular_user",
        }
        response = self.client.put(url, data)

        # Staff users should be able to update other users' passwords without knowing their previous password.
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_user_as_self(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.get_user_token(self.regular_user)}')
        url = reverse('users-detail', kwargs={'pk': self.regular_user.id})
        data = {
            "username": "partial_updated_user",
        }
        response = self.client.patch(url, data)

        # Users should be able to partially update their own information.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'partial_updated_user')

    def test_partial_update_user_as_staff_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.get_user_token(self.staff_user)}')
        url = reverse('users-detail', kwargs={'pk': self.regular_user.id})
        data = {
            "username": "partial_updated_user_2",
        }
        response = self.client.patch(url, data)

        # Staff users should be able to partially update other users' information.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'partial_updated_user_2')

    def test_partial_update_user_password_as_self_without_old_password(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.get_user_token(self.regular_user)}')
        url = reverse('users-detail', kwargs={'pk': self.regular_user.id})
        data = {
            "password": "Anew_password_!1",
        }
        response = self.client.patch(url, data)

        # Users should not be able to partially update their own password without providing the old password.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_update_user_password_as_staff_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.get_user_token(self.staff_user)}')
        url = reverse('users-detail', kwargs={'pk': self.regular_user.id})
        data = {
            "password": "Anew_password_!1",
        }
        response = self.client.patch(url, data)

        # Staff users should be able to partially update other users' passwords without knowing their previous password.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
