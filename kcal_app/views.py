import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
# Create your views here.
from django.views.generic import CreateView, ListView, FormView, UpdateView, DeleteView
from kcal_app.forms import LoginForm, AddUserAndProfileForm, AddDayForm, AddIngredientToMealForm
from kcal_app.models import Ingredient, Meal, Profile, Activity, Day, MealIngredientWeight


class LandingPageView(View):
    def get(self, request):
        return render(request, 'mainpage.html')

########### DAY #############
class AddDayView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        form = AddDayForm(initial={'date': datetime.datetime.today()})
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        try:
            form = AddDayForm(request.POST)

            if form.is_valid():
                day = form.save(commit=False)
                day.profile = request.user.profile
                day.save()
                form.save_m2m()
                return redirect('/dashboard/')
            else:
                return render(request, 'form.html', {'form': form})
        except:
            ctx = {
                'error_message': "Given day already exists for your profile"
            }
            return render(request, "form.html", ctx)


class EditDayView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'next'
    model = Day
    fields = ['date', 'meals', 'activity']
    template_name = 'kcal_app/ingredient_update_form.html'
    success_url = "/dashboard/"


class DeleteDayView(LoginRequiredMixin, DeleteView):
    model = Day
    success_url = reverse_lazy("profile-page")
    template_name = 'kcal_app/ingredient_confirm_delete.html'


########### INGREDIENT #############
class AddIngredientView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'next'

    model = Ingredient
    fields = "__all__"
    success_url = "/dashboard"


class EditIngredientView(LoginRequiredMixin, UpdateView):
    model = Ingredient
    fields = "__all__"
    template_name_suffix = '_update_form'
    success_url = reverse_lazy("ingredients")


class DeleteIngredientView(LoginRequiredMixin, DeleteView):
    model = Ingredient
    success_url = reverse_lazy("ingredients")

########### MEAL #############
class AddMealView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'next'
    model = Meal
    fields = ['name']
    success_url = "/dashboard/"


class AddIngredientToMealView(LoginRequiredMixin, View):
    def get(self, request, id):
        form = AddIngredientToMealForm()
        return render(request, 'add_to_meal.html', {'form': form})

    def post(self, request, id):
        form = AddIngredientToMealForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.meal_id = id
            item.save()
            return redirect('/dashboard/')
        else:
            return HttpResponse("błąd")


class EditMealView(UpdateView):
    model = Meal
    fields = "__all__"
    template_name_suffix = '_update_form'
    success_url = "/dashboard/"


class DeleteMealView(DeleteView):
    model = Meal
    success_url = "/dashboard/"



class AddActivity(CreateView):
    model = Activity
    fields = "__all__"
    success_url = reverse_lazy("activities")


class EditActivityView(UpdateView):
    model = Activity
    fields = "__all__"
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("activities")


class DeleteActivityView(DeleteView):
    model = Activity
    success_url = reverse_lazy("activities")


class IngredientsListView(ListView):
    model = Ingredient


class ActivityListView(ListView):
    model = Activity


class DashboardView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        days = Day.objects.filter(profile=Profile.objects.get(user=request.user)).order_by('-date')
        meals = []
        ingredients = []
        for day in days:
            for meal in day.meals.all():
                meals.append(meal)
        for meal in meals:
            for ingredient in meal.ingredients.all():
                ingredients.append(ingredient)
        total_kcal = 0
        for ingredient in ingredients:
            total_kcal += ingredient.proteins * 4 + ingredient.fat * 9 + ingredient.carbs * 4 #+ MealIngredientWeight.objects.filter(ingredient__name=ingredient.name).weight/100
        ctx = {
            'total_kcal': total_kcal,
            'days': days,
            'meals': meals,
            'ingredients': ingredients
        }
        return render(request, 'dashboard.html', ctx)


class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        next_url = request.GET.get('next', '/dashboard/')
        if form.is_valid():
            user = authenticate(request, **form.cleaned_data)
            if user is not None:
                login(request, user)
                return redirect(next_url)
            else:
                return HttpResponse("Błędne dane logowania")
        return render(request, 'form.html', {'form': form})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect("/")


class SignUp(View):
    def get(self, request):
        form = AddUserAndProfileForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = AddUserAndProfileForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['username'] not in User.objects.filter(username=form.cleaned_data['username']):
                if form.cleaned_data['password'] == form.cleaned_data['confirm_password']:
                    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                                        password=form.cleaned_data['password'])
                    profile = Profile.objects.create(user=new_user, name=form.cleaned_data['name'],
                                                     age=form.cleaned_data['age'], weight=form.cleaned_data['weight'])
                    return redirect('/login')
                else:
                    return render(request, 'form.html', {'form': form})
