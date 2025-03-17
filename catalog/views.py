from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView, DetailView
from catalog.models import BikeModel, BikeCharacteristicValue


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


class HomePage(TemplateView):
    template_name = 'catalog/index.html'
    extra_context = {
        'title': 'Главная',
        'menu': menu,
    }


class ShowCatalog(TemplateView):
    template_name = 'catalog/catalog.html'
    extra_context = {
        'title': 'Каталог',
        'menu': menu,
    }


class ShowFavourites(TemplateView):
    template_name = 'catalog/favourites.html'
    extra_context = {
        'title': 'Избранное',
        'menu': menu,
    }


class ShowAbout(TemplateView):
    template_name = 'catalog/about.html'
    extra_context = {
        'title': 'О нас',
        'menu': menu,
    }


class ShowBike(DetailView):
    model = BikeModel
    template_name = 'catalog/bike.html'
    slug_url_kwarg = 'bike_slug'
    context_object_name = 'bike_selected'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{context['bike_selected'].mark.name} {context['bike_selected'].name}'
        context['menu'] = menu
        context['bike_characteristics'] = BikeCharacteristicValue.get_bike_characteristics(context['bike_selected'])
        return context
