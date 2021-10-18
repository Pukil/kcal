import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, request, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
# Create your views here.
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from kcal_app.forms import LoginForm, AddUserAndProfileForm, AddDayForm, AddIngredientToMealForm, \
    EditDayForm, AddMealForm
from kcal_app.models import Ingredient, Meal, Profile, Activity, Day, Plan


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

class DayInfoView(LoginRequiredMixin, View):

    def get(self, request, date):
        return render(request, 'day_info.html', {'day': Day.objects.get(profile=request.user, date=date)})



class EditDayView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'next'
    model = Day
    form_class = EditDayForm
    template_name = 'kcal_app/ingredient_update_form.html'
    success_url = "/dashboard/"


    def get_form(self, form_class=None):
        super().get_form()
        form_class = self.get_form_class()
        return form_class(user=self.request.user, **self.get_form_kwargs())



class DeleteDayView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    redirect_field_name = 'next'
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
    login_url = '/login/'
    redirect_field_name = 'next'
    model = Ingredient
    fields = "__all__"
    template_name_suffix = '_update_form'
    success_url = reverse_lazy("ingredients")


class DeleteIngredientView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    redirect_field_name = 'next'
    model = Ingredient
    success_url = reverse_lazy("ingredients")


########### MEAL #############
class AddMealView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'next'
    model = Meal
    form_class = AddMealForm
    success_url = "/dashboard/"



    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    # def form_invalid(self, form):
    #     errors = []
    #     for error in form.errors:
    #         errors.append(error)
    #     return HttpResponse(errors)


class AddIngredientToMealView(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = 'next'

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


class EditMealView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'next'
    model = Meal
    fields = "__all__"
    template_name_suffix = '_update_form'
    success_url = "/dashboard/"


class DeleteMealView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    redirect_field_name = 'next'
    model = Meal
    success_url = "/dashboard/"



########### PLAN #############
class CreatePlanView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'next'
    model = Plan
    fields = "__all__"
    success_url = reverse_lazy("profile-page")
    template_name = "kcal_app/ingredient_form.html"


class ShowAllPlans(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'next'
    model = Plan


class EditPlanView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'next'
    model = Plan
    fields = "__all__"
    success_url = reverse_lazy("profile-page")
    template_name = "kcal_app/ingredient_form.html"


class DeletePlanView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    redirect_field_name = 'next'
    model = Plan



class AddActivity(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'next'
    model = Activity
    fields = "__all__"
    success_url = reverse_lazy("activities")


class EditActivityView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'next'
    model = Activity
    fields = "__all__"
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("activities")


class DeleteActivityView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    redirect_field_name = 'next'
    model = Activity
    success_url = reverse_lazy("activities")


class IngredientsListView(ListView):
    model = Ingredient


class ActivityListView(ListView):
    model = Activity


class DashboardView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request, date=datetime.datetime.today()):
        days = Day.objects.filter(profile=Profile.objects.get(user=request.user)).order_by('-date')
        # day =Day.objects.get(user=request.user, date=datetime(2021, 10,18).date())
        # meals = day.meals.all()
        meals = Meal.objects.filter(user=request.user)
        ingredients = []
        ctx = {
            'total_kcal': 0,
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