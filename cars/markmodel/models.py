from django.db import models

class CarMark(models.Model):
    name = models.CharField(max_length = 255)

class CarModel(models.Model):
    name = models.CharField(max_length = 255)
    mark = models.ForeignKey(CarMark, on_delete = models.CASCADE)