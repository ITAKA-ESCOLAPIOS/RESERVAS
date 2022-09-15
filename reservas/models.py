import django.conf.global_settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import validate_email, MinLengthValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# Create your models here.

class Objeto(models.Model):
    id_obj = models.CharField(max_length=3, validators=[MinLengthValidator(3)], primary_key=True)
    descripcion = models.CharField(max_length=200)

    class Meta:
        abstract = True


class Butanito(Objeto):
    pass


class Quemador(Objeto):
    pass


class Tienda(Objeto):
    nombre = models.CharField(max_length=20)


class Reserva(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=10)
    apellido = models.CharField(max_length=20)
    email = models.CharField(max_length=100, validators=[validate_email])
    telefono = models.CharField(max_length=9, validators=[MinLengthValidator(9)])
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=3, validators=[MinLengthValidator(3)])
    content_object = GenericForeignKey('content_type', 'object_id')


class Usuario(AbstractUser):
    telefono = models.CharField(max_length=9, validators=[MinLengthValidator(9)])


class Observacion(models.Model):
    id = models.AutoField(primary_key=True)
    texto = models.TextField(max_length=300)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
