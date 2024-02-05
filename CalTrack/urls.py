from django.urls import path

from . import views

app_name = "CalTrack"
urlpatterns = [
    path("", views.index, name="index"),
    path("addmeal", views.addmeal, name="addmeal"),
    path("addfood", views.addfood, name="addfood"),
    path("addfoodtype", views.addfoodtype, name="addfoodtype"),
    path("<int:meal_id>", views.deletemeal, name="deletemeal"),
    path("edit/<int:meal_id>", views.editmealpage, name="editmealpage"),
    path("editor/<int:meal_id>", views.editmeal, name="editmeal"),
    path("stats/", views.stats, name="stats"),
    path("statsfind/", views.statsfind, name="statsfind"),
    path("delete/", views.deletefood, name="deletefood"),
]