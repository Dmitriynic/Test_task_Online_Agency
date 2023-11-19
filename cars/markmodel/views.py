from rest_framework import viewsets
from django.shortcuts import render
from .models import CarModel, CarMark
from .serializers import CarModelSerializer, CarMarkSerializer

class CarMarkViewSet(viewsets.ModelViewSet):
    queryset = CarMark.objects.all()
    serializer_class = CarMarkSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CarMarkSerializer(queryset, many=True)
        context = {'marks': serializer.data}
        return render(request, 'markmodel/cars.html', context)

class CarModelViewSet(viewsets.ModelViewSet):
    serializer_class = CarModelSerializer
    queryset = CarModel.objects.all()

    def get_queryset(self):
        mark_id = self.request.query_params.get('mark_id')
        if mark_id:
            queryset = CarModel.objects.filter(mark_id=mark_id)
        else:
            queryset = CarModel.objects.all()
        return queryset