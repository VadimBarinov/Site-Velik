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
    img_url = models.CharField(max_length=511)

    def __str__(self):
        return self().name

    def get_absolute_url(self):
        return reverse('bike', kwargs={'bike_slug': self.slug})


class BikeModification(models.Model):
    bike_model = models.ForeignKey(
        'BikeModel', on_delete=models.PROTECT, related_name='bike_model'
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class BikeCharacteristic(models.Model):
    name = models.CharField(max_length=255)
    id_parent = models.IntegerField(null=True)

    def __str__(self):
        return [self.name, self.id_parent]


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
        return [self.value, self.bike_characteristic, self.bike_modification]
