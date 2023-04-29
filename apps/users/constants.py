from enum import Enum


class SubscriptionChoices(Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
