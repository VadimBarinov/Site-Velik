from django.views.generic import TemplateView, DetailView, ListView
from catalog.models import BikeModel, BikeCharacteristicValue
from catalog.utils import DataMixin
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from velik import settings


class HomePage(DataMixin, ListView):
    model = BikeModel
    template_name = 'catalog/index.html'
    context_object_name = 'bikes'
    title_page = 'Главная'

    def get_queryset(self):
        return BikeModel.objects.all()[:3]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['default_img'] = settings.DEFAULT_BIKE_IMAGE
        return context


class ShowCatalog(DataMixin, ListView):
    model = BikeModel
    template_name = 'catalog/catalog.html'
    title_page = 'Каталог'
    context_object_name = 'bikes'
    paginate_by = 15

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            object_list = BikeModel.objects.filter(
                Q(mark__name__icontains=query) | Q(name__icontains=query)
            )
            return object_list
        return BikeModel.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['input_value'] = self.request.GET.get('query')
        context['default_img'] = settings.DEFAULT_BIKE_IMAGE
        return context


class ShowFavourites(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'catalog/favourites.html'
    title_page = 'Избранное'
    context_object_name = 'bikes'
    paginate_by = 15

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            object_list = BikeModel.objects.filter(
                Q(mark__name__icontains=query) | Q(name__icontains=query)
            )
            return object_list
        return BikeModel.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['input_value'] = self.request.GET.get('query')
        context['default_img'] = settings.DEFAULT_BIKE_IMAGE
        return context


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
        context['default_img'] = settings.DEFAULT_BIKE_IMAGE
        title = context['bike_selected'].mark.name + ' ' + context['bike_selected'].name
        bike_characteristics = BikeCharacteristicValue.get_bike_characteristics(context['bike_selected'])
        return self.get_mixin_context(context, title=title, bike_characteristics=bike_characteristics)
