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
from django.urls import path, include, re_path

from kcal_app.views import LandingPageView, AddIngredientView, AddMealView, DashboardView, LoginView, LogoutView, \
    SignUp, AddActivity, IngredientsListView, ActivityListView, AddDayView, AddIngredientToMealView, EditMealView, \
    DeleteMealView, EditIngredientView, DeleteIngredientView, EditActivityView, DeleteActivityView, EditDayView, \
    DeleteDayView, CreatePlanView, EditPlanView, DeletePlanView, ShowAllPlans, DayInfoView, ActivityTimeView, \
    EditActivityTime, EditProfileView, DeleteActivityTime, EditIngredientWeight, DeleteIngredientWeight

urlpatterns = [
    path('admin/', admin.site.urls),
    path("login/", LoginView.as_view(), name='login'),
    path("logout/", LogoutView.as_view(), name='logout'),
    path("signup/", SignUp.as_view(), name='signup'),
    path('', LandingPageView.as_view(), name="main-page"),
    path('edit_profile/<int:pk>/', EditProfileView.as_view(), name="edit-profile"),
    ### ingredient urls
    path('add_ingredient/', AddIngredientView.as_view(), name="add-ingredient"),
    path('edit_ingredient/<int:pk>/', EditIngredientView.as_view(), name="edit-ingredient"),
    path('delete_ingredient/<int:pk>/', DeleteIngredientView.as_view(), name="delete-ingredient"),
    path('add_meal/', AddMealView.as_view(), name="add-meal"),
    path(r'dashboard/', DashboardView.as_view(), name="profile-page"),
    path('add_activity/', AddActivity.as_view(), name="add-activity"),
    path('ingredients/', IngredientsListView.as_view(), name="ingredients"),
    path('edit_weight/<int:pk>/', EditIngredientWeight.as_view(), name="edit-weight"),
    path('delete_weight/<int:pk>/', DeleteIngredientWeight.as_view(), name="delete-weight"),
    ### activity urls
    path('activities/',ActivityListView.as_view(), name="activities"),
    path('activity_edit/<int:pk>/', EditActivityView.as_view(), name="edit-activity"),
    path('activity_delete/<int:pk>/', DeleteActivityView.as_view(), name="delete-activity"),
    path('activity_time/<int:id>/<int:pk>/', ActivityTimeView.as_view(), name="activity-time"),
    path('edit_activity_time/<int:pk>/', EditActivityTime.as_view(), name="edit-time"),
    path('delete_activity_time/<int:pk>/', DeleteActivityTime.as_view(), name="delete-time"),
    path('add_day/', AddDayView.as_view(), name="add-day"),
    path('edit_day/<int:pk>/', EditDayView.as_view(), name="edit-day"),
    path('delete_day/<int:pk>/', DeleteDayView.as_view(), name='delete-day'),
    path('add_to_meal/<int:id>/', AddIngredientToMealView.as_view(), name="add-to-meal"),
    path('edit_meal/<int:pk>/', EditMealView.as_view(), name="edit-meal"),
    path('delete_meal/<int:pk>/', DeleteMealView.as_view(), name="delete-meal"),
    path('add_plan/', CreatePlanView.as_view(), name="create-plan"),
    path('edit_plan/<int:pk>/', EditPlanView.as_view(), name="edit-plan"),
    path('delete_plan/<int:pk>/', DeletePlanView.as_view(), name="delete-plan"),
    path('show_plans/', ShowAllPlans.as_view(), name="plan-list"),
    path('date/<int:pk>/', DayInfoView.as_view(), name="day-info")
]
