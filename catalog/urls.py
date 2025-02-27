from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name='home'),
    path("catalog/", views.show_catalog, name='catalog'),
    path("favourites/", views.show_favourites, name='favourites'),
    path("about/", views.show_about, name='about'),
]
