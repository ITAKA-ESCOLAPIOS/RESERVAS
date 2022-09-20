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
    path('mis_reservas/', views.mis_reservas),
    path('eliminar_reserva/<int:p_id>', views.eliminar_reserva, name='eliminar_reserva'),
    path('resultado_reserva/<str:mensaje>', views.resultado_reserva),
    path('register/', views.register_request, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('submit_but/', views.submit_but, name='submit_but'),
    path('submit_que/', views.submit_que, name='submit_que'),
    path('submit_tie/', views.submit_tie, name='submit_tie'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='main/password/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="main/password/password_reset_confirm.html"),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='main/password/password_reset_complete.html'),
         name='password_reset_complete'),
    path("password_reset", views.password_reset_request, name="password_reset"),
]
