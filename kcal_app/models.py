from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Ingredient(models.Model):
    name = models.CharField(max_length=128)
    fat = models.IntegerField()
    carbs = models.IntegerField()
    proteins = models.IntegerField()
    weight = models.IntegerField()

    def __str__(self):
        return self.name


class Meal(models.Model):
    options = (
        ('breakfast','breakfast'),
        ('lunch', 'lunch'),
        ('dinner', 'dinner'),
        ('other', 'other')
    )
    ingredients = models.ManyToManyField(Ingredient)
    name = models.TextField(choices=options)

    def __str__(self):
        return self.name


class Day(models.Model):
    date = models.DateField()
    meals = models.ManyToManyField(Meal)
    activity = models.ManyToManyField('Activity')


class Activity(models.Model):
    name = models.CharField(max_length=128)
    burned_kcal = models.IntegerField()

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=200,null=True)
    age = models.IntegerField(null=True)
    weight = models.IntegerField(null=True)



class Recipe(models.Model):
    meal = models.OneToOneField(Meal, on_delete=models.CASCADE)
    details = models.TextField()



