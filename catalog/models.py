from django.db import models
from django.urls import reverse


class BikeMark(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class BikeModel(models.Model):
    mark = models.ForeignKey(
        'BikeMark', on_delete=models.PROTECT, related_name='mark'
        )
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    img_url = models.ImageField(
        upload_to="bikes/%Y/%m/%d/",
        default=None,
        blank=True,
        null=True
        )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('bike', kwargs={'bike_slug': self.slug})


class BikeModification(models.Model):
    bike_model = models.OneToOneField(
        'BikeModel', on_delete=models.PROTECT, related_name='bike_model'
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class BikeCharacteristic(models.Model):
    name = models.CharField(max_length=255)
    id_parent = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class BikeCharacteristicValue(models.Model):
    value = models.CharField(max_length=255)
    bike_characteristic = models.ForeignKey(
        'BikeCharacteristic',
        on_delete=models.PROTECT,
        related_name='bike_characteristic'
    )
    bike_modification = models.ForeignKey(
        'BikeModification',
        on_delete=models.PROTECT,
        related_name='bike_modification'
    )

    def __str__(self):
        return str(self.pk)

    def get_bike_characteristics(bike):
        id_parents = BikeCharacteristic.objects.filter(id_parent=None)
        bike_characteristics = {}
        characteristics_value = bike.bike_model.bike_modification.all()

        for char in characteristics_value:
            if bike_characteristics.get(id_parents.get(pk=char.bike_characteristic.id_parent).name):
                temp = bike_characteristics[id_parents.get(pk=char.bike_characteristic.id_parent).name]
                temp[char.bike_characteristic.name] = char.value
                bike_characteristics[id_parents.get(pk=char.bike_characteristic.id_parent).name] = temp
            else:
                bike_characteristics[id_parents.get(pk=char.bike_characteristic.id_parent).name] = {
                    char.bike_characteristic.name: char.value
                    }
        return bike_characteristics
