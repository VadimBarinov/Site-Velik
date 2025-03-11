from django.shortcuts import get_object_or_404, render
from catalog.models import BikeModel, BikeCharacteristic


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
    id_parents = BikeCharacteristic.objects.filter(id_parent=None)
    bike_characteristics = {}
    characteristics_value = bike.bike_model.bike_modification.all()
    char_value = {}

    for char in characteristics_value:
        if char_value.get(id_parents.get(pk=char.bike_characteristic.id_parent).name):
            temp = char_value[id_parents.get(pk=char.bike_characteristic.id_parent).name]
            temp[char.bike_characteristic.name] = char.value
            char_value[id_parents.get(pk=char.bike_characteristic.id_parent).name] = temp
        else:
            char_value[id_parents.get(pk=char.bike_characteristic.id_parent).name] = {
                char.bike_characteristic.name: char.value
                }

    bike_characteristics = char_value
    data = {
        'title': f'{bike.mark.name} {bike.name}',
        'menu': menu,
        'bike_selected': bike,
        'bike_characteristics': bike_characteristics,
    }
    return render(request, 'catalog/bike.html', data)
