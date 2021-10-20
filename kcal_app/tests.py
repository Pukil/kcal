import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, Client
from django.urls import reverse

# Create your tests here.
from kcal_app.models import Profile, Ingredient, Meal, MealIngredientWeight, Activity


########## LOGIN ##########
def test_login(client):
    response = client.get(reverse('login'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_post(client):
    data_signup = {
        'username': 'bartek12',
        'password': 'bartek1',
        'confirm_password': 'bartek1'
    }
    response_data_signup = client.post(reverse('signup'), data=data_signup)
    assert response_data_signup.status_code == 302
    data = {
        'username': "bartek12",
        'password': "bartek1"
    }
    response = client.post(reverse('login'), data=data)
    assert response.status_code == 302


########## LOGOUT ##########
@pytest.mark.django_db
def test_logout_get(client, user):
    client.force_login(user)
    response = client.get(reverse('logout'))
    assert response.status_code == 302


def test_logout_get_no_login(client):
    response = client.get(reverse('logout'))
    assert response.status_code == 302


########## SIGNUP ##########
def test_signup_get(client):
    response = client.get(reverse('signup'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_signup_post(client, profile):
    data = {
        'username': 'bartek1231',
        'password': 'bartek1',
        'confirm_password': 'bartek1'
    }
    response = client.post(reverse('signup'), data=data)
    assert response.status_code == 302


########## LANDING PAGE ##########
def test_landing_page_get_no_login(client):
    response = client.get(reverse("main-page"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_landing_page_get_login(client, user):
    client.force_login(user)
    response = client.get(reverse("main-page"))
    assert response.status_code == 200


########## EDIT PROFILE ##########
@pytest.mark.django_db
def test_edit_profile_get_login(client, user, profile):
    client.force_login(user)
    response = client.get(reverse("edit-profile", kwargs={'pk': profile.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_profile_get_no_login(client, profile):
    response = client.get(reverse("edit-profile", kwargs={'pk': profile.pk}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_edit_profile_post(client, profile):
    data = {
        'age': 12,
        'weight': 60,
        'height': 160
    }
    response = client.post(reverse('edit-profile', kwargs={'pk': profile.pk}), data=data)
    assert response.status_code == 302


@pytest.mark.django_db
def test_edit_profile_post_changes(client, profile):
    client.force_login(profile.user)
    data = {
        'age': 12,
        'weight': 60,
        'height': 160
    }
    response = client.post(reverse('edit-profile', kwargs={'pk': profile.pk}), data=data)
    assert response.status_code == 302
    Profile.objects.get(age=12)


########## DASHBOARD ##########
def test_dashboard_get_no_login(client):
    response = client.get(reverse("profile-page"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_dashboard_get_login(client, user, profile):
    client.force_login(user)
    response = client.get(reverse("profile-page"))
    assert response.status_code == 200


########## INGREDIENTS ##########
def test_get_ingredients_list_no_login(client):
    response = client.get(reverse('ingredients'))
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_ingredients_list_login(client, user):
    client.force_login(user)
    response = client.get(reverse('ingredients'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_ingredients_list_login_not_empty(client, user, ingredients):
    client.force_login(user)
    response = client.get(reverse('ingredients'))
    assert response.status_code == 200
    ingredient_list = response.context['object_list']
    assert ingredient_list.count() == len(ingredients)


@pytest.mark.django_db
def test_get_ingredients_list_login_not_empty_all_ingredients_in_list(client, user, ingredients):
    client.force_login(user)
    response = client.get(reverse('ingredients'))
    assert response.status_code == 200
    ingredient_list = response.context['object_list']
    assert ingredient_list.count() == len(ingredients)
    for ingredient in ingredients:
        assert ingredient in ingredient_list


########## ADD INGREDIENT ##########
def test_add_ingredient_no_login(client):
    response = client.get(reverse("add-ingredient"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_ingredient_login(client, user):
    client.force_login(user)
    response = client.get(reverse("add-ingredient"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_ingredient_login_post(client, user):
    client.force_login(user)
    data = {
        'name': 'jajko',
        'fat': 60.2,
        'carbs': 160.3,
        'proteins': 25.3,
    }
    response = client.post(reverse("add-ingredient"), data=data)
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_ingredient_post_login_check_existing(client, user):
    client.force_login(user)
    data = {
        'name': "abcdefghjkl",
        'fat': 60,
        'carbs': 160,
        'proteins': 25
    }
    response = client.post(reverse("add-ingredient"), data=data)
    assert response.status_code == 302
    Ingredient.objects.get(**data)


########## EDIT INGREDIENT ##########
@pytest.mark.django_db
def test_edit_ingredient_no_login(client, ingredient):
    response = client.get(reverse("edit-ingredient", kwargs={'pk': ingredient.pk}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_edit_ingredient_login(client, ingredient, user):
    client.force_login(user)
    response = client.get(reverse("edit-ingredient", kwargs={'pk': ingredient.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_ingredient_login_post(client, ingredient, user):
    client.force_login(user)
    data = {
        "name": "jablko1",
        "fat": 1,
        "carbs": 2,
        "proteins": 12
    }
    response = client.post(reverse("edit-ingredient", kwargs={'pk': ingredient.pk}), data=data)
    assert response.status_code == 302


@pytest.mark.django_db
def test_edit_ingredient_login_post_changes(client, ingredient, user):
    client.force_login(user)
    data = {
        "name": "jablko1",
        "fat": 1,
        "carbs": 2,
        "proteins": 12
    }
    response = client.post(reverse("edit-ingredient", kwargs={'pk': ingredient.pk}), data=data)
    assert response.status_code == 302
    Ingredient.objects.get(**data)


########## DELETE INGREDIENT #########
@pytest.mark.django_db
def test_delete_ingredient_login(client, ingredient, user):
    client.force_login(user)
    response = client.get(reverse("delete-ingredient", kwargs={'pk': ingredient.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_ingredient_no_login(client, ingredient):
    response = client.get(reverse("delete-ingredient", kwargs={'pk': ingredient.pk}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_delete_ingredient_login_post(client, ingredient, user):
    client.force_login(user)
    response = client.post(reverse("delete-ingredient", kwargs={'pk': ingredient.pk}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_delete_ingredient_login_post_deleted(client, ingredient, user):
    client.force_login(user)
    response = client.post(reverse("delete-ingredient", kwargs={'pk': ingredient.pk}))
    assert response.status_code == 302
    with pytest.raises(ObjectDoesNotExist):
        Ingredient.objects.get(pk=ingredient.pk)


########## ADD MEAL ##########
def test_add_meal_get_no_login(client):
    response = client.get(reverse("add-meal"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_meal_get_login(client, user):
    client.force_login(user)
    response = client.get(reverse("add-meal"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_meal_post_login(client, user):
    client.force_login(user)
    data = {
        'name': "random_posilek"
    }
    response = client.post(reverse("add-meal"), data=data)
    assert response.status_code == 302


########## ADD TO MEAL ##########
@pytest.mark.django_db
def test_add_to_meal_get_no_login(client, meal):
    response = client.get(reverse("add-to-meal", kwargs={'id': meal.id}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_to_meal_get_login(client, meal):
    client.force_login(meal.user)
    response = client.get(reverse("add-to-meal", kwargs={'id': meal.id}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_to_meal_post_login(client, meal, ingredient):
    client.force_login(meal.user)
    data = {
        'meal': meal.id,
        'ingredient': ingredient.id,
        'weight': 20
    }
    response = client.post(reverse("add-to-meal", kwargs={'id': meal.id}), data=data)
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_to_meal_post_login_check_if_exist(client, meal, ingredient):
    client.force_login(meal.user)
    data = {
        'meal': meal.id,
        'ingredient': ingredient.id,
        'weight': 20
    }
    response = client.post(reverse("add-to-meal", kwargs={'id': meal.id}), data=data)
    assert response.status_code == 302
    MealIngredientWeight.objects.get(**data)


########## EDIT MEAL ##########
@pytest.mark.django_db
def test_edit_meal_get_no_login(client, meal):
    response = client.get(reverse('edit-meal', kwargs={'pk': meal.pk}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_edit_meal_get_login(client, meal):
    client.force_login(meal.user)
    response = client.get(reverse('edit-meal', kwargs={'pk': meal.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_meal_post_login(client, meal):
    client.force_login(meal.user)
    data = {
        'ingredients': meal.ingredients.all(),
        'name': 'newname'
    }
    response = client.post(reverse('edit-meal', kwargs={'pk': meal.pk}), data=data)
    assert response.status_code == 302


@pytest.mark.django_db
def test_edit_meal_post_login_change(client, meal):
    client.force_login(meal.user)
    data = {
        'ingredients': meal.ingredients.all(),
        'name': 'newname'
    }
    response = client.post(reverse('edit-meal', kwargs={'pk': meal.pk}), data=data)
    assert response.status_code == 302
    assert Meal.objects.get(name='newname').ingredients.count() == len(meal.ingredients.all())


########## DELETE MEAL ##########
@pytest.mark.django_db
def test_delete_meal_get_login(client, meal, user):
    client.force_login(user)
    response = client.get(reverse("delete-meal", kwargs={'pk': meal.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_meal_get_no_login(client, meal, user):
    response = client.get(reverse("delete-meal", kwargs={'pk': meal.pk}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_delete_meal_login_post(client, meal, user):
    client.force_login(user)
    response = client.post(reverse("delete-meal", kwargs={'pk': meal.pk}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_delete_meal_login_post_deleted(client, meal, user):
    client.force_login(user)
    response = client.post(reverse("delete-meal", kwargs={'pk': meal.pk}))
    assert response.status_code == 302
    with pytest.raises(ObjectDoesNotExist):
        Meal.objects.get(pk=meal.pk)


########## EDIT WEIGHT ##########
@pytest.mark.django_db
def test_edit_weight_get_no_login(client, weight):
    response = client.get(reverse('edit-weight', kwargs={'pk': weight.pk}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_edit_weight_get_login(client, weight):
    client.force_login(weight.meal.user)
    response = client.get(reverse('edit-weight', kwargs={'pk': weight.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_weight_post_login(client, weight):
    client.force_login(weight.meal.user)
    data = {
        'meal': weight.meal.id,
        'ingredient': weight.ingredient.id,
        'weight': 999
    }
    response = client.post(reverse('edit-weight', kwargs={'pk': weight.pk}), data=data)
    assert response.status_code == 302


@pytest.mark.django_db
def test_edit_weight_post_login_change(client, weight):
    client.force_login(weight.meal.user)
    data = {
        'meal': weight.meal.id,
        'ingredient': weight.ingredient.id,
        'weight': 999
    }
    response = client.post(reverse('edit-weight', kwargs={'pk': weight.pk}), data=data)
    assert response.status_code == 302
    MealIngredientWeight.objects.get(**data)


########## DELETE WEIGHT ##########
@pytest.mark.django_db
def test_delete_weight_get_no_login(client, weight):
    response = client.get(reverse('delete-weight', kwargs={'pk': weight.pk}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_delete_weight_get_login(client, weight):
    client.force_login(weight.meal.user)
    response = client.get(reverse('delete-weight', kwargs={'pk': weight.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_weight_post_login(client, weight):
    client.force_login(weight.meal.user)
    response = client.post(reverse('delete-weight', kwargs={'pk': weight.pk}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_delete_weight_post_login_deleted(client, weight):
    client.force_login(weight.meal.user)
    response = client.post(reverse('delete-weight', kwargs={'pk': weight.pk}))
    assert response.status_code == 302
    with pytest.raises(ObjectDoesNotExist):
        MealIngredientWeight.objects.get(pk=weight.pk)


########## ACTIVITIES ##########
def test_get_activities_list_no_login(client):
    response = client.get(reverse('activities'))
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_activities_list_login(client, user):
    client.force_login(user)
    response = client.get(reverse('activities'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_activities_list_login_not_empty(client, user, activities):
    client.force_login(user)
    response = client.get(reverse('activities'))
    assert response.status_code == 200
    activity_list = response.context['object_list']
    assert activity_list.count() == len(activities)


@pytest.mark.django_db
def test_get_activities_list_login_not_empty_all_activities_in_list(client, user, activities):
    client.force_login(user)
    response = client.get(reverse('activities'))
    assert response.status_code == 200
    activities_list = response.context['object_list']
    assert activities_list.count() == len(activities)
    for activity in activities:
        assert activity in activities_list


########## ADD ACTIVITY ##########
def test_add_activity_get_no_login(client):
    response = client.get(reverse("add-activity"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_activity_get_login(client, user):
    client.force_login(user)
    response = client.get(reverse("add-activity"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_activity_post_login(client, user):
    client.force_login(user)
    data = {
        'name': "abcd",
        'burned_kcal': 997
    }
    response = client.post(reverse("add-activity"), data=data)
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_activity_post_login_check_existing(client, user):
    client.force_login(user)
    data = {
        'name': "abcd",
        'burned_kcal': 997
    }
    response = client.post(reverse("add-activity"), data=data)
    assert response.status_code == 302
    Activity.objects.get(**data)


########## ACTIVITY DELETE ##########
@pytest.mark.django_db
def test_delete_activity_login(client, activities, user):
    client.force_login(user)
    response = client.get(reverse("delete-activity", kwargs={'pk': activities[0].pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_activity_no_login(client, activities):
    response = client.get(reverse("delete-activity", kwargs={'pk': activities[0].pk}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_delete_activity_login_post(client, activities, user):
    client.force_login(user)
    response = client.post(reverse("delete-activity", kwargs={'pk': activities[0].pk}))
    assert response.status_code == 302


@pytest.mark.django_db
def test_delete_ingredient_login_post_deleted(client, activities, user):
    client.force_login(user)
    response = client.post(reverse("delete-activity", kwargs={'pk': activities[0].pk}))
    assert response.status_code == 302
    with pytest.raises(ObjectDoesNotExist):
        Activity.objects.get(pk=activities[0].pk)