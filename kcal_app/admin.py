from django.contrib import admin

# Register your models here.
from kcal_app.models import Ingredient, Meal, Recipe, Day, Activity, Profile

admin.site.register(Ingredient)
admin.site.register(Meal)
admin.site.register(Recipe)
admin.site.register(Day)
admin.site.register(Activity)
admin.site.register(Profile)

