from django.urls import reverse

from rest_framework import status

from .factories import UserFactory
from .test_base_user_view import UserViewSetTests


class DeleteUserViewSetTests(UserViewSetTests):
    """
    This class tests the delete conditions for the UserViewSet specified in the challenge.
    """

    def test_delete_user_as_regular_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.get_user_token(self.regular_user)}')
        user_to_delete = UserFactory()
        url = reverse('users-detail', kwargs={'pk': user_to_delete.pk})
        response = self.client.delete(url)

        # Regular users should not be allowed to use this endpoint.
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user_as_staff_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.get_user_token(self.staff_user)}')
        non_staff_user_to_delete = UserFactory()
        url = reverse('users-detail', kwargs={'pk': non_staff_user_to_delete.pk})
        response = self.client.delete(url)

        # Staff users can delete any other non-staff user.
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_staff_user_as_staff_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.get_user_token(self.staff_user)}')
        staff_user_to_delete = UserFactory(is_staff=True)
        url = reverse('users-detail', kwargs={'pk': staff_user_to_delete.pk})
        response = self.client.delete(url)

        # Staff users cannot delete other staff users.
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user_as_superuser(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.get_user_token(self.superuser)}')
        user_to_delete = UserFactory()
        url = reverse('users-detail', kwargs={'pk': user_to_delete.pk})
        response = self.client.delete(url)

        # Admins can delete any user.
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_staff_user_as_superuser(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.get_user_token(self.superuser)}')
        staff_user_to_delete = UserFactory(is_staff=True)
        url = reverse('users-detail', kwargs={'pk': staff_user_to_delete.pk})
        response = self.client.delete(url)

        # Admins can delete any user, including staff users.
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
