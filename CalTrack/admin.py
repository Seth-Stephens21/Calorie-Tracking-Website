from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import Consumer,meal,meal_time,Food,food_type

admin.site.register(Consumer, UserAdmin)
admin.site.register(meal)
admin.site.register(meal_time)
admin.site.register(Food)
admin.site.register(food_type)