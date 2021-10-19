import pytest
from django.test import TestCase, Client
from django.urls import reverse


# Create your tests here.

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
        'username': 'bartek1',
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


def test_add_ingredient_no_login(client):
    response = client.get(reverse("add-ingredient"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_ingredient_login(client, user):
    client.force_login(user)
    response = client.get(reverse("add-ingredient"))
    assert response.status_code == 200
