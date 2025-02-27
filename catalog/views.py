from django.shortcuts import render


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
