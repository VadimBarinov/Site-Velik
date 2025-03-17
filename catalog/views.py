from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView, DetailView
from catalog.models import BikeModel, BikeCharacteristicValue
from catalog.utils import DataMixin


class HomePage(DataMixin, TemplateView):
    template_name = 'catalog/index.html'
    title_page = 'Главная'


class ShowCatalog(DataMixin, TemplateView):
    template_name = 'catalog/catalog.html'
    title_page = 'Каталог'


class ShowFavourites(DataMixin, TemplateView):
    template_name = 'catalog/favourites.html'
    title_page = 'Избранное'


class ShowAbout(DataMixin, TemplateView):
    template_name = 'catalog/about.html'
    title_page = 'О нас'


class ShowBike(DataMixin, DetailView):
    model = BikeModel
    template_name = 'catalog/bike.html'
    slug_url_kwarg = 'bike_slug'
    context_object_name = 'bike_selected'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = context['bike_selected'].mark.name + ' ' + context['bike_selected'].name
        bike_characteristics = BikeCharacteristicValue.get_bike_characteristics(context['bike_selected'])
        return self.get_mixin_context(context, title=title, bike_characteristics=bike_characteristics)
