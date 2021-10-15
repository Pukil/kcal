import datetime

from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Ingredient(models.Model):
    name = models.CharField(max_length=128)
    fat = models.IntegerField()
    carbs = models.IntegerField()
    proteins = models.IntegerField()

    def __str__(self):
        return self.name


class Meal(models.Model):
    ingredients = models.ManyToManyField(Ingredient, through='MealIngredientWeight')
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class MealIngredientWeight(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    weight = models.IntegerField()


class Day(models.Model):
    date = models.DateField()
    meals = models.ManyToManyField(Meal)
    activity = models.ManyToManyField('Activity', blank=True)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('date', 'profile')


class Activity(models.Model):
    name = models.CharField(max_length=128)
    burned_kcal = models.IntegerField()

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    age = models.IntegerField(null=True)
    weight = models.IntegerField(null=True)

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
