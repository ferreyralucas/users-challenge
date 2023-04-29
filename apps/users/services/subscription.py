from django.conf import settings

import requests


class SubscriptionService:

    @classmethod
    def get_subscription(self, user_id) -> dict:
        """
        The function checks if a user is subscribed by making a GET request to a subscription service
        API and returning the subscription information as a dict.
        """
        return requests.get(f"https://subscriptions.fake.service.test/api/v1/users/{user_id}").json()


class SubscriptionServiceMock:

    @classmethod
    def get_subscription(self, user_id) -> dict:
        """
        This function checks if a user is subscribed and returns a dictionary with the value of "ACTIVE".
        """
        subscription_response = {
            "id": user_id,
            "subscription": "active"
        }
        return subscription_response


if settings.SUBSCRIPTION_SERVICE_MOCK:
    SubscriptionService = SubscriptionServiceMock  # noqa
