from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Consumer(AbstractUser):
    weight = models.CharField(max_length=64)
    dob = models.DateField(null=True)
    is_superuser = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.username.capitalize()}"
    
    
#meal_time can be breakfast, lunch, etc.
class meal_time(models.Model):
    typeofmeal = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.typeofmeal}"
    
class meal(models.Model):
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE, related_name="meals")
    meal_time = models.ForeignKey(meal_time, on_delete=models.CASCADE, related_name="time")
    orderdate = models.DateField(null=True)
    
    def __str__(self):
        return f"meal {self.id}"
    
class food_type(models.Model):
    name = models.CharField(max_length=64)
    

    def __str__(self):
        return f"{self.name}"

class Food(models.Model):
    food_type = models.ForeignKey(food_type, on_delete=models.CASCADE , related_name="main")
    meal = models.ForeignKey(meal, on_delete=models.CASCADE, related_name="foods")
    calories = models.IntegerField()

    def __str__(self):
        return f"{self.food_type}"

