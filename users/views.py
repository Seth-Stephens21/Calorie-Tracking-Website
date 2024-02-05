from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "users/user.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                 return HttpResponseRedirect(reverse("CalTrack:stats"))
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "users/login.html", {
                "message" : "Invalid credentials"
            })
    return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    return render(request, "users/login.html",{
        "message" : "Logged Out."
    })

def registerpage(request):
    return render(request, "users/registerpage.html",{
        "message": "Please enter your information"
    })

def register(request):
    username = request.POST["username"]
    email = request.POST["email"]
    password = request.POST["password"]
    weight = request.POST["weight"]
    dob = request.POST["dob"]
    NewConsumer = get_user_model().objects.create_user(username=username,email=email, password=password,
        weight=weight, dob=dob)                                               
    return render(request, "users/login.html",{
        "message" : "Please Login"
    })