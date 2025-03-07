from django import template
from catalog.models import BikeModel

# регистрация новых тегов
register = template.Library()


# включающий тег
@register.inclusion_tag('catalog/list_bikes.html')
def show_bikes():
    bikes = BikeModel.objects.all()
    return {'bikes': bikes}


@register.inclusion_tag('catalog/list_bikes.html')
def show_bikes_6():
    bikes = BikeModel.objects.all()[:6]
    return {'bikes': bikes}


@register.inclusion_tag('catalog/carousel.html')
def show_carousel():
    bikes = BikeModel.objects.all()[:3]
    return {'bikes': bikes}
