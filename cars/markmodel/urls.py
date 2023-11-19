from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.shortcuts import redirect
from .views import CarMarkViewSet, CarModelViewSet

router = DefaultRouter()
router.register(r'marks', CarMarkViewSet, basename='carmark')
router.register(r'models', CarModelViewSet, basename='carmodel')

urlpatterns = [
    path('', lambda request: redirect('carmark-list'), name='home'),  # Перенаправление на список марок
    path('', include(router.urls)),
]