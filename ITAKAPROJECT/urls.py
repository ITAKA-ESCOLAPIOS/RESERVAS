"""ITAKAPROJECT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path, register_converter
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from reservas import views
from reservas.converters import DateConverter

register_converter(DateConverter, 'date')

urlpatterns = [
    path('reserva_but/', views.reserva_but),
    path('reserva_que/', views.reserva_que),
    path('reserva_tie/', views.reserva_tie),
    path('catalogo/', views.catalogo),
    path('admin/', admin.site.urls),
    path('register/', views.register_request, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('reserva_but/<date:fecha_inicio>/<date:fecha_fin>', views.submit_but, name='submit_but'),
    path('reserva_que/<date:fecha_inicio>/<date:fecha_fin>', views.submit_que, name='submit_que'),
    path('reserva_tie/<date:fecha_inicio>/<date:fecha_fin>', views.submit_tie, name='submit_tie'),

]
