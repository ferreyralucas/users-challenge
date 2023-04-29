import uuid

from django.contrib.auth import password_validation
from django.contrib.auth.models import Group

from rest_framework import serializers

from .services.subscription import SubscriptionService
from django.core.exceptions import ValidationError
from .models import User


class UserModelSerializer(serializers.ModelSerializer):
    """
    Base serializer for the User model, handling common fields and validations.
    """
    repeat_password = serializers.CharField(write_only=True, max_length=128, required=False)
    password = serializers.CharField(write_only=True, max_length=128, required=False)

    def handle_password(self, instance, validated_data) -> None:
        """
        Sets the password for an instance if it is provided in the validated data.
        """
        password = validated_data.get("password")
        if password:
            instance.set_password(password)

    def create(self, data) -> User:
        """
        Creates a new user with a unique ID and subscription status based on the input data.
        """
        id = uuid.uuid4()
        data.pop('repeat_password', None)
        subscription = SubscriptionService.get_subscription(id)["subscription"]
        user = User(subscription=subscription, id=id, **data)

        # Call handle_password() to set the password correctly
        self.handle_password(user, data)

        # Save the user after setting the password
        user.save()

        return user

    def update(self, instance, validated_data) -> User:
        """
        Updates the attributes of an instance and sets a new password if provided.
        """
        for attr in ('username', 'first_name', 'last_name', 'email'):
            setattr(instance, attr, validated_data.get(attr, getattr(instance, attr)))

        self.handle_password(instance, validated_data)

        instance.save()
        return instance

    def validate(self, data) -> dict:
        """
        Validates a password and checks if it matches the repeated password.
        """
        password = data.get('password')
        repeat_password = data.get('repeat_password')

        if password and repeat_password and password != repeat_password:
            raise serializers.ValidationError("Passwords do not match")

        if password:

            try:
                password_validation.validate_password(password)
            except ValidationError as e:
                raise serializers.ValidationError({"password": e.messages})

        return data

    def to_representation(self, instance):
        # Determine if the user is staff or is requesting their own information
        is_staff_or_own_user = (
            self.context['request'].user.is_staff or self.context['request'].user.is_superuser
            or self.context['request'].user == instance
        )

        # Obtain the original data dictionary
        data = super().to_representation(instance)

        # If the user is not staff or is not requesting their own information, remove the email field.
        if not is_staff_or_own_user:
            data.pop('email')

        return data

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "repeat_password",
        ]


class GroupList(serializers.ListField):
    """
    Custom list field to handle group names.
    """

    def to_representation(self, value):
        return value.values_list("name", flat=True)


class StaffUserModelSerializer(UserModelSerializer):
    """
    Serializer to handle user data for staff or superuser, includes group management.
    """
    groups = GroupList(
        child=serializers.CharField(min_length=1, max_length=150)
    )

    def _manage_groups(self, user, group_names) -> None:
        """
        This function clears a user's current group memberships and adds them to new groups based on a list
        of group names.
        """
        user.groups.clear()

        for group_name in group_names:
            group, created = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)

    def create(self, validated_data) -> User:
        group_names = validated_data.pop('groups', [])

        # Call the create method of the parent class (UserModelSerializer)
        user = super().create(validated_data)

        # Assign the user to the specified groups
        self._manage_groups(user, group_names)

        return user

    def update(self, instance, validated_data) -> User:
        group_names = validated_data.pop("groups", [])

        # Call the update method of the parent class (UserModelSerializer)
        instance = super().update(instance, validated_data)

        # Update the user's groups only if the groups field was provided
        if group_names:
            self._manage_groups(instance, group_names)

        return instance

    class Meta:
        model = User
        fields = UserModelSerializer.Meta.fields + [
            "groups",
            "created",
            "subscription",
            "updated",
            "password",
        ]
        extra_kwargs = {'password': {'write_only': True}}


class FlatUserSerializer(UserModelSerializer):
    """
    Serializer to handle user data for non-staff users.
    """
    old_password = serializers.CharField(write_only=True, max_length=128, required=False)

    def validate_old_password(self, old_password) -> None:
        """
        This function validates if the old password provided matches the current password.
        """
        if not self.instance.check_password(old_password):
            raise serializers.ValidationError("The old password is incorrect.")

    def validate(self, data) -> dict:
        """
        This function validates whether the old password is provided when updating the password.
        """

        if data.get("password"):
            old_password = data.get("old_password")
            if old_password:
                self.validate_old_password(old_password)
            else:
                raise serializers.ValidationError("Old password is required when updating password.")

        return super().validate(data)

    class Meta:
        model = User
        fields = UserModelSerializer.Meta.fields + ["old_password"]
