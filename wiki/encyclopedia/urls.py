from django.urls import path

from . import views

#always more specific to less specific URLs!!!
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/newEntry/", views.newEntry, name="newEntry"),
    path("wiki/<str:title>/editEntry", views.editEntry, name="editEntry"),
    path("wiki/randomPage", views.randomPage, name = "randomPage"),
    path("wiki/search/", views.search, name="search"),
    path("wiki/<str:title>/", views.entry, name="entry")
]
