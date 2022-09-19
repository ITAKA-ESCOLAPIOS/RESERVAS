from django.contrib import admin
from .models import Usuario, Butanito, Quemador, Tienda, HistoricoReservas, FuturasReservas

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Butanito)
admin.site.register(Quemador)
admin.site.register(Tienda)
admin.site.register(HistoricoReservas)
admin.site.register(FuturasReservas)

