"""kcal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from kcal_app.views import LandingPageView, AddIngredientView, AddMealView, DashboardView, LoginView, LogoutView, \
    SignUp, AddActivity, IngredientsListView, ActivityListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("login/", LoginView.as_view(), name='login'),
    path("logout/", LogoutView.as_view(), name='logout'),
    path("signup/", SignUp.as_view(), name='signup'),
    path('', LandingPageView.as_view(), name="main-page"),
    path('add_ingredient/', AddIngredientView.as_view(), name="add-ingredient"),
    path('add_meal/', AddMealView.as_view(), name="add-meal"),
    path('dashboard/', DashboardView.as_view(), name="profile-page"),
    path('add_activity/', AddActivity.as_view(), name="add-activity"),
    path('ingredients/', IngredientsListView.as_view(), name="ingredients"),
    path('activities/',ActivityListView.as_view(), name="activities")
]
