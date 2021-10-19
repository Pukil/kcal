import datetime

from django import forms
from django.contrib.auth.models import User

from kcal_app.models import Day, Ingredient, Meal, MealIngredientWeight, ActivityDayTime


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class AddUserAndProfileForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    name = forms.CharField(max_length=64, required=False)
    age = forms.IntegerField(min_value=1, required=False)
    weight = forms.IntegerField(min_value=1, required=False)
    height = forms.IntegerField(min_value=1, required=False)


class AddDayForm(forms.ModelForm):
    class Meta:
        model = Day
        fields = ['date']
        widgets = {
            'date': forms.SelectDateWidget()
        }


class AddIngredientToMealForm(forms.ModelForm):
    class Meta:
        model = MealIngredientWeight
        exclude = ['meal']


class ActivityTimeForm(forms.ModelForm):
    class Meta:
        model = ActivityDayTime
        # fields = "__all__"
        exclude = ['day']


class EditDayForm(forms.ModelForm):

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        meals = Meal.objects.filter(user=user)
        self.fields['meals'].queryset = meals
        self.fields['day_weight'].initial = Day.day_weight

    class Meta:
        model = Day
        exclude = ['profile', 'date', 'base_kcal']
        widgets = {
            'meals': forms.CheckboxSelectMultiple,
            'activity': forms.CheckboxSelectMultiple,
        }


class AddMealForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddMealForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Meal
        exclude = ['user', 'ingredients']


class EditMealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['ingredients', 'name']
        widgets = {
            'ingredients': forms.CheckboxSelectMultiple
        }
