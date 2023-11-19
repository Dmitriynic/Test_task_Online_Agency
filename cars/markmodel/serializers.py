from rest_framework import serializers
from .models import CarMark, CarModel

class CarMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarMark
        fields = ['id', 'name']

class CarModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CarModel
        fields = ['id', 'name', 'mark_id']