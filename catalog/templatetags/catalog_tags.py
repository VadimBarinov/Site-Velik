from django import template
from catalog.models import BikeModel, BikeCharacteristic


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
    id_parents = BikeCharacteristic.objects.filter(id_parent=None)
    bikes_characteristics = {}

    for item in bikes:
        characteristics_value = item.bike_model.bike_modification.all()
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

        bikes_characteristics[item.slug] = char_value

    return {'bikes': bikes, 'bikes_characteristics': bikes_characteristics}


@register.filter
def get_value_from_dict(dict_data, key):
    return dict_data.get(key)
