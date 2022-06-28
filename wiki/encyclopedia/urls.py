from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/create-new", views.createnew, name="createnew"),
    path("wiki/edit/<str:title>", views.edit, name="edit"),
    path("wiki/search", views.search, name="search"),
    path("wiki/random", views.random, name="random"),
    path("wiki/<str:title>", views.entry, name="entry")    
]

