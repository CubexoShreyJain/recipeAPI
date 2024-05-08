from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Add any additional fields you want
    pass


class Recipe(models.Model):
    title = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    ingredients = models.TextField()
    preparation_steps = models.TextField()
    cooking_time = models.PositiveIntegerField()  # in minutes
    serving_size = models.PositiveIntegerField()
    category = models.CharField(max_length=50)  # New field for category
    owner = models.ForeignKey('recipes.CustomUser', related_name='recipes', on_delete=models.CASCADE)

    def __str__(self):
        return self.title