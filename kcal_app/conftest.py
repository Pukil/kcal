import pytest
from django.contrib.auth.models import User
from django.test import Client

from kcal_app.models import Profile, Ingredient


@pytest.fixture
def user():
    user = User.objects.create_user(username='bartek1', password='bartek1')
    return user


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def profile(user):
    profile = Profile.objects.create(user=user)
    return profile

@pytest.fixture
def ingredient():
    ingredient = Ingredient.objects.create(name="jablko", fat=12, carbs=13, proteins=14)
    return ingredient
