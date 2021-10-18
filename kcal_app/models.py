import datetime

from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Ingredient(models.Model):
    name = models.CharField(max_length=128)
    fat = models.FloatField()
    carbs = models.FloatField()
    proteins = models.FloatField()

    def __str__(self):
        return self.name

    def calculate_calories_per_1_gram(self):
        return self.proteins * 4 + self.fat * 9 + self.carbs * 4


class Meal(models.Model):
    ingredients = models.ManyToManyField(Ingredient, through='MealIngredientWeight', blank=True)
    name = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def total_kcal(self):
        tot_kcal = 0
        ings = MealIngredientWeight.objects.filter(meal=self)
        for ing in ings:
            tot_kcal += ing.get_cal()
        return round(tot_kcal)


class MealIngredientWeight(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    weight = models.IntegerField()

    def get_cal(self):
        return self.weight * self.ingredient.calculate_calories_per_1_gram()



class Day(models.Model):
    date = models.DateField()
    meals = models.ManyToManyField(Meal)
    activity = models.ManyToManyField('Activity', blank=True)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    base_kcal = models.IntegerField(default=2000)

    class Meta:
        unique_together = ('date', 'profile')

    def daily_kcal(self):
        daily_kcal = 0
        for meal in self.meals.all():
            daily_kcal += meal.total_kcal()
        return daily_kcal

    def __str__(self):
        return str(self.date)


class Activity(models.Model):
    name = models.CharField(max_length=128)
    burned_kcal = models.IntegerField()

    def __str__(self):
        return self.name


class ActivityDayTime(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    time_in_minutes = models.IntegerField()

    def kcal_burned(self):
        return round(self.activity.burned_kcal * self.time_in_minutes)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    age = models.IntegerField(null=True)
    weight = models.IntegerField(null=True)
    plan = models.ForeignKey('Plan', on_delete=models.CASCADE, default=None, null=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.id is None:
            created = True
        else:
            created = False
        super().save(force_insert, force_update, using,
                     update_fields)
        if created:
            day = Day()
            day.date = datetime.datetime.now().date()
            day.profile = self
            day.save()


class Recipe(models.Model):
    meal = models.OneToOneField(Meal, on_delete=models.CASCADE)
    details = models.TextField()


class Plan(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    kcal_diff = models.IntegerField()

    def __str__(self):
        return self.name
