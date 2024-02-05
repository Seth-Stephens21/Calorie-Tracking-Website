from django.shortcuts import render
from .models import Consumer,meal,meal_time,Food,food_type
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
from django.contrib.auth import get_user_model
from django.db.models import Sum
# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, "users/login.html", {
                "message1" : "Please Login"
            })
    return render(request, "CalTrack/index.html",{
        "consumer" : request.user,
        "meals" : meal.objects.filter(consumer_id = request.user.id),
        "foods" : Food.objects.filter(meal__consumer_id = request.user.id),
        "meal_time" : meal_time.objects.all(),
        "food_type" : food_type.objects.all(),
    })

def addmeal(request):
    if request.method == "POST": 
        consumer1 = request.user
        date1 = request.POST.get("date")
        meal_time1 = meal_time.objects.get(pk=int(request.POST["meal_time"]))
        meal.objects.create(consumer = consumer1, meal_time = meal_time1, orderdate = date1)
        return render(request, "CalTrack/index.html",{
        "consumer" : request.user,
        "meals" : request.user.meals.all(),
        "meal_time" : meal_time.objects.all(),
        "food_type" : food_type.objects.all(),
    })
        
#def updatemeal(request):
    #if request.method =="PUT":

def addfood(request):
    if request.method == "POST":
        meal1 = meal.objects.get(pk=int(request.POST["meal"]))
        foodtype1 = food_type.objects.filter(name =request.POST["type"]).first()
        Food.objects.create(meal=meal1,food_type=foodtype1,calories=request.POST["calories"])
        return HttpResponseRedirect(reverse("CalTrack:index"))
    
def addfoodtype(request):
    if request.method == "POST":
        foodtypeobject = food_type.objects.create(name = request.POST["Food_Type"].strip().lower()) 
        return HttpResponseRedirect(reverse("CalTrack:index"))
        
def deletemeal(request,meal_id):
    if request.method == "POST":
        meal1 = meal.objects.get(pk=meal_id)
        meal1.delete()
        return HttpResponseRedirect(reverse("CalTrack:index"))

def deletefood(request):
    if request.method == "POST":
        food = Food.objects.get(pk=int(request.POST["foodid"]))
        mealid = food.meal.id
        food.delete()
        return HttpResponseRedirect(reverse("CalTrack:editmealpage",kwargs={"meal_id":mealid}))

def editmealpage(request,meal_id):
    thisdate = meal.objects.get(pk=meal_id).orderdate
    thisdate = thisdate.strftime("%m/%d/%Y")
    return render(request,"CalTrack/editmealpage.html",{
        "id" : meal_id,
        "consumer" : request.user,
        "meals" : request.user.meals.all(),
        "thisMealTime" : meal.objects.get(pk=meal_id).meal_time,
        "thisdate" : thisdate,
        "currfoods" : Food.objects.filter(meal_id=meal_id),
        "meal_time" : meal_time.objects.all(),
        "food_type" : food_type.objects.all(),
        "range" : range(3),

    })
    
def editmeal(request,meal_id):
    if request.method == "POST":
        #meal1 = meal.objects.filter(pk=meal_id).update(orderdate=request.POST["date"], meal_time_id = int(request.POST["meal_time"]))
        #meal_time1 = meal_time.objects.get(pk=int(request.POST["meal_time"]))
        #meal1 = meal.objects.filter(pk=meal_id).update(meal_time = meal_time1)
        
        meal1 = meal.objects.filter(pk=meal_id).first()
        if request.POST["date"]:
            print(request.POST["date"])
            meal1.orderdate = request.POST["date"]
        if request.POST["meal_time"]:
            meal1.meal_time_id = int(request.POST["meal_time"])
        meal1.save()
        for food in Food.objects.filter(meal_id=meal_id):
            foodtype = food_type.objects.filter(name =request.POST[f"{food.id}"]).first()
            food.food_type=foodtype
            food.calories = int(request.POST[f"cal{food.id}"])
            food.save()
        for i in range(3):
            if request.POST[f"food{i}"] and request.POST[f"cal{i}"]:
                foodType = food_type.objects.filter(name =request.POST[f"food{i}"]).first()
                Food.objects.create(meal=meal1,food_type=foodType,calories=request.POST[f"cal{i}"])

        return HttpResponseRedirect(reverse("CalTrack:index"))
    
def stats(request):
    return render(request,"CalTrack/stats.html",{
        "meal_time" : meal_time.objects.all(),
    })

def statsfind(request):
    if request.method == "POST":
        mealcals = []
        meals = []
        Max = 0
        for user in get_user_model().objects.all():
            for meal in user.meals.filter(orderdate = request.POST["date"], meal_time_id=int(request.POST["meal_time"])):
                mealCalSum = meal.foods.aggregate(Sum("calories"))
                mealcals.append(mealCalSum["calories__sum"])
                meals.append(meal)
        if mealcals:
            Max = max(mealcals)
            maxmeal = meals[mealcals.index(Max)]
            consumer = maxmeal.consumer
            message = f"{consumer} ate the most for {meal.meal_time} on {request.POST['date']} with {Max} calories total"
            check = True
        else:
            message = "No Meals Match This Date and Meal Time"
            check = False
        return render(request,"CalTrack/stats.html",{
            "meal_time" : meal_time.objects.all(),
            "message" : message,
            "check" : check
        })


