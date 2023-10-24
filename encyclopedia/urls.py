from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create_entry, name="create"),
    path("random/", views.random_entry, name="random"),
    path("search/", views.search, name="search"),
    path("wiki/<str:title>/", views.entry_preview, name="entry"),
    path("edit/<str:title>/", views.edit_entry, name="edit")
]
