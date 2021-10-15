from django import forms

from kcal_app.models import Day, Ingredient, Meal, MealIngredientWeight


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class AddUserAndProfileForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    name = forms.CharField(max_length=64)
    age = forms.IntegerField(min_value=1)
    weight = forms.IntegerField(min_value=1)

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




