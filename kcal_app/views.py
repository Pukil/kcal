from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
# Create your views here.
from django.views.generic import CreateView, ListView
from kcal_app.forms import LoginForm, AddUserAndProfileForm
from kcal_app.models import Ingredient, Meal, Profile, Activity


class LandingPageView(View):
    def get(self, request):
        return render(request, 'mainpage.html')


class AddIngredientView(CreateView):
    model = Ingredient
    fields = "__all__"
    success_url = "/"


class AddMealView(CreateView):
    model = Meal
    fields = "__all__"
    success_url = "/"

class AddActivity(CreateView):
    model = Activity
    fields = "__all__"
    success_url = "/"

class IngredientsListView(ListView):
    model = Ingredient


class ActivityListView(ListView):
    model = Activity


class DashboardView(View):
    def get(self, request):
        ctx = {
#do kontekstu trzeba przekazac obiekt zawierający profil i to co w tym profilu bylo dodane
            # ProfileDay.objects.filter(profile=profile).filter(name=breakfast)?          #################################
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
        return render(request, 'form.html', {'form':form})

    def post(self, request):
        form = AddUserAndProfileForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['username'] not in User.objects.filter(username=form.cleaned_data['username']):
                if form.cleaned_data['password'] == form.cleaned_data['confirm_password']:
                    new_user = User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                    profile = Profile.objects.create(user=new_user, name=form.cleaned_data['name'], age=form.cleaned_data['age'], weight=form.cleaned_data['weight'])
                    return redirect('/login')
                else:
                    return render(request, 'form.html', {'form':form})
