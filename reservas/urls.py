from django.urls import path
from . import views

urlpatterns = [
    path('', views.reserva, name='index'),
    path('', views.catalogo, name='catalogo')
]