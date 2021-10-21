import datetime

import pytest
from django.contrib.auth.models import User
from django.test import Client

from kcal_app.models import Profile, Ingredient, Meal, MealIngredientWeight, Activity, Day, ActivityDayTime, Plan


@pytest.fixture
def user():
    user = User.objects.create_user(username='bartek1', password='bartek1')
    return user


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def profile(user, plan):
    profile = Profile.objects.create(user=user, weight=75, height=180, age=25, plan=plan)
    return profile

@pytest.fixture
def ingredient():
    ingredient = Ingredient.objects.create(name="jablko", fat=12, carbs=13, proteins=14)
    return ingredient


@pytest.fixture
def ingredients():
    ingredients = []
    for x in range(10):
        ingredients.append(Ingredient.objects.create(name=f"jablko {x}", fat=x, carbs=x, proteins=x))
    return ingredients

@pytest.fixture
def meal(user):
    meal = Meal.objects.create(name="random posilek do testow", user=user)
    return meal

@pytest.fixture
def weight(meal, ingredient):
    weight = MealIngredientWeight.objects.create(meal=meal, ingredient=ingredient, weight=123)
    return weight

@pytest.fixture
def activities():
    activities = []
    for x in range(10):
        activities.append(Activity.objects.create(name=f"activity_number_{x+1}", burned_kcal=x*20))
    return activities


@pytest.fixture
def day(meal, profile, activities):
    day = Day.objects.get(date=datetime.datetime.today(), profile=profile)
    return day


@pytest.fixture
def time(activities, day):
    time = ActivityDayTime.objects.create(activity=activities[0], day=day, time_in_minutes=123)
    return time

@pytest.fixture
def plan():
    plan = Plan.objects.create(name="testplan1", description="testplan1desc", kcal_diff=300)
    return plan