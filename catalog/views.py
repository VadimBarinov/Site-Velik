from django.shortcuts import get_object_or_404, render
from catalog.models import BikeModel


menu = [
    {
        'title': 'Главная',
        'url': 'home',
    },
    {
        'title': 'Каталог',
        'url': 'catalog',
    },
    {
        'title': 'Избранное',
        'url': 'favourites',
    },
    {
        'title': 'О нас',
        'url': 'about',
    },
]


def index(request):
    data = {
        'title': 'Главная',
        'menu': menu,
    }
    return render(request, 'catalog/index.html', data)


def show_catalog(request):
    data = {
        'title': 'Каталог',
        'menu': menu,
    }
    return render(request, 'catalog/catalog.html', data)


def show_favourites(request):
    data = {
        'title': 'Избранное',
        'menu': menu,
    }
    return render(request, 'catalog/favourites.html', data)


def show_about(request):
    data = {
        'title': 'О нас',
        'menu': menu,
    }
    return render(request, 'catalog/favourites.html', data)


def show_bike(request, bike_slug):
    bike = get_object_or_404(BikeModel, slug=bike_slug)
    data = {
        'title': f'{bike.mark.name} {bike.name}',
        'menu': menu,
        'bike_selected': bike
    }
    return render(request, 'catalog/bike.html', data)
