import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, Client
from django.urls import reverse

# Create your tests here.
# TODO:
# 1.  Sprawdzanie czy profil sie zedytowal
########## LOGIN ##########
from kcal_app.models import Profile, Ingredient


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
        'name': "abcd",
        'fat': 60,
        'carbs': 160,
        'protein': 25
    }
    response = client.post(reverse("add-ingredient"), data=data)
    assert response.status_code == 200


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

