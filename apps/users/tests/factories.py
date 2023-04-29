import uuid
from django.contrib.auth.hashers import make_password
import factory
from factory.django import DjangoModelFactory
from faker import Faker

from users.models import User
from users.constants import SubscriptionChoices

faker = Faker()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    id = factory.LazyFunction(lambda: uuid.uuid4())
    username = factory.Sequence(lambda n: f"user_{n}")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.LazyAttribute(lambda obj: f"{obj.first_name.lower()}.{obj.last_name.lower()}@example.com")
    created = factory.Faker("date_time_this_decade", tzinfo=None)
    updated = factory.LazyAttribute(lambda obj: faker.date_time_between(
        start_date=obj.created, end_date="now", tzinfo=None))
    subscription = factory.Iterator(SubscriptionChoices.choices(), getter=lambda choice: choice[0])
    password = factory.LazyAttribute(lambda _: make_password("regular_password"))
