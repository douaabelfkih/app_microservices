from django.urls import path
from . import views

urlpatterns = [
    path("", views.main, name="index"),
    path("item/<str:slug>/", views.item, name="item"),

]