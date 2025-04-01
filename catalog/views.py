from django.http import JsonResponse
from django.views.generic import TemplateView, DetailView, ListView
from catalog.models import BikeModel, BikeCharacteristicValue, BikeFavourites, BikeStars
from catalog.utils import DataMixin
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin


def add_del_favourites(current_user, current_bike):
    if current_user.is_authenticated:
        found_favourite = BikeFavourites.objects.filter(
            Q(user__pk=current_user.pk) & Q(bike__pk=current_bike)
        )
        if found_favourite.exists():
            found_favourite.delete()
            return JsonResponse(
                {
                    'is_taken': True,
                    'is_added': False,
                    'bike_selected': current_bike,
                }
            )

        else:
            save_favourite = BikeFavourites(
                user=current_user,
                bike=BikeModel.objects.get(pk=current_bike)
            )
            save_favourite.save()
            return JsonResponse(
                {
                    'is_taken': True,
                    'is_added': True,
                    'bike_selected': current_bike,
                }
            )
    else:
        return JsonResponse(
                {
                    'is_taken': False,
                }
            )


def delete_star(current_user, current_bike):
    if current_user.is_authenticated:
        found_star = BikeStars.objects.filter(
            Q(user__pk=current_user.pk) & Q(bike__pk=current_bike)
        )
        if found_star.exists():
            found_star.get().delete()

        star_bike = BikeModel.objects.get(pk=current_bike).star
        return JsonResponse(
            {
                'is_taken': True,
                'star_bike': star_bike,
            }
        )
    else:
        return JsonResponse(
            {
                'is_taken': False,
            }
        )


def add_star(current_user, current_bike, current_star):
    if current_user.is_authenticated:
        found_star = BikeStars.objects.filter(
            Q(user__pk=current_user.pk) & Q(bike__pk=current_bike)
        )
        if found_star.exists():
            found_star.get().delete()

        save_star = BikeStars(
                user=current_user,
                bike=BikeModel.objects.get(pk=current_bike),
                star=current_star,
        )
        save_star.save()
        star_bike = BikeModel.objects.get(pk=current_bike).star
        return JsonResponse(
            {
                'is_taken': True,
                'star_value': current_star,
                'star_bike': star_bike,
            }
        )
    else:
        return JsonResponse(
                {
                    'is_taken': False,
                }
            )


class HomePage(DataMixin, ListView):
    model = BikeModel
    template_name = 'catalog/index.html'
    context_object_name = 'bikes'
    title_page = 'Главная'

    def get_queryset(self):
        return BikeModel.objects.all()[:3]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        context['bike_favourites'] = []
        if current_user:
            context['bike_favourites'] = [
                bike.bike.pk for bike in BikeFavourites.objects.filter(user__pk=current_user.pk)
            ]
        return context

    def post(self, *args, **kwargs):
        current_user = self.request.user
        current_bike = self.request.POST.get('bike_selected')
        favourite_or_star = self.request.POST.get('favourite_or_star')
        if favourite_or_star == 'favourite':
            return add_del_favourites(current_user, current_bike)


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
        current_user = self.request.user
        context['bike_favourites'] = []
        if current_user:
            context['bike_favourites'] = [
                bike.bike.pk for bike in BikeFavourites.objects.filter(user__pk=current_user.pk)
            ]
        return context

    def post(self, *args, **kwargs):
        current_user = self.request.user
        current_bike = self.request.POST.get('bike_selected')
        favourite_or_star = self.request.POST.get('favourite_or_star')
        if favourite_or_star == 'favourite':
            return add_del_favourites(current_user, current_bike)


class ShowFavourites(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'catalog/favourites.html'
    title_page = 'Избранное'
    context_object_name = 'bikes'
    paginate_by = 15

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            object_list = BikeModel.objects.filter(
                pk__in=[bike.bike.pk for bike in BikeFavourites.objects.filter(user__pk=self.request.user.pk)]
            ).filter(Q(mark__name__icontains=query) | Q(name__icontains=query))
            return object_list
        return BikeModel.objects.filter(
            pk__in=[bike.bike.pk for bike in BikeFavourites.objects.filter(user__pk=self.request.user.pk)]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['input_value'] = self.request.GET.get('query')
        context['bike_favourites'] = [
            bike.pk for bike in context['bikes']
            ]
        return context

    def post(self, *args, **kwargs):
        current_user = self.request.user
        current_bike = self.request.POST.get('bike_selected')
        favourite_or_star = self.request.POST.get('favourite_or_star')
        if favourite_or_star == 'favourite':
            return add_del_favourites(current_user, current_bike)


class ShowStars(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'catalog/stars.html'
    title_page = 'Мои оценки'
    context_object_name = 'bikes'
    paginate_by = 15

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            object_list = BikeModel.objects.filter(
                pk__in=[bike.bike.pk for bike in BikeStars.objects.filter(user__pk=self.request.user.pk)]
            ).filter(Q(mark__name__icontains=query) | Q(name__icontains=query))
            return object_list
        return BikeModel.objects.filter(
            pk__in=[bike.bike.pk for bike in BikeStars.objects.filter(user__pk=self.request.user.pk)]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['input_value'] = self.request.GET.get('query')
        context['bike_favourites'] = [
            bike.pk for bike in context['bikes']
            ]
        return context

    def post(self, *args, **kwargs):
        current_user = self.request.user
        current_bike = self.request.POST.get('bike_selected')
        favourite_or_star = self.request.POST.get('favourite_or_star')
        if favourite_or_star == 'favourite':
            return add_del_favourites(current_user, current_bike)


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
        bike_favourites = BikeFavourites.objects.filter(Q(user__pk=self.request.user.pk) & Q(bike__pk=context['bike_selected'].pk)).exists()
        bike_star = BikeStars.objects.filter(Q(user__pk=self.request.user.pk) & Q(bike__pk=context['bike_selected'].pk))
        if bike_star.exists():
            bike_star = bike_star.get().star
        else:
            bike_star = False
        return self.get_mixin_context(
            context,
            title=title,
            bike_characteristics=bike_characteristics,
            bike_favourites=bike_favourites,
            bike_star=bike_star,
        )

    def post(self, *args, **kwargs):
        current_user = self.request.user
        current_bike = self.request.POST.get('bike_selected')
        current_star = self.request.POST.get('count_stars')
        favourite_or_star = self.request.POST.get('favourite_or_star')
        if favourite_or_star == 'favourite':
            return add_del_favourites(current_user, current_bike)
        elif favourite_or_star == 'delete_star':
            return delete_star(current_user, current_bike)
        elif favourite_or_star == 'add_star':
            return add_star(current_user, current_bike, current_star)
