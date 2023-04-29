from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .permissions import StaffPermission, UserRemovalPermission, UpdateOwnProfileOrStaff
from .serializers import FlatUserSerializer, StaffUserModelSerializer
from users.models import User
from rest_framework import serializers
from typing import Type


class UserViewSet(ModelViewSet):
    '''Viewset class for managing User model instances'''
    queryset = User.objects.all()
    serializer_class = StaffUserModelSerializer

    def get_permissions(self) -> list:
        # By default, all actions require authentication.
        permission_classes = [IsAuthenticated]

        # For 'update' and 'partial_update' actions, apply custom permission.
        if self.action in ['update', 'partial_update']:
            permission_classes += [UpdateOwnProfileOrStaff]

        # For 'destroy' action, apply custom delete permission.
        if self.action == "destroy":
            permission_classes += [UserRemovalPermission]

        # For 'create' action, only admins or staff members are allowed.
        if self.action == 'create':
            permission_classes += [StaffPermission]

        # Instantiate the permission classes and return the list.
        return [permission() for permission in permission_classes]

    def get_serializer_class(self) -> Type[serializers.Serializer]:
        '''Determines the serializer class based on the current user's role.'''
        # If the user is a staff member or a superuser, use the full UserModelSerializer.

        if self.request.user.is_staff or self.request.user.is_superuser:
            return StaffUserModelSerializer
        else:
            # For other users, return a minimal serializer with limited fields.
            return FlatUserSerializer
