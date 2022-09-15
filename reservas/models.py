from django.db import models
from django.core.validators import validate_email, MinLengthValidator


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
    email = models.CharField(validators=[validate_email])
    telefono = models.CharField(max_length=9, validators=[MinLengthValidator(9)])
    objeto_reservado = models.OneToOneField(Objeto, on_delete=models.CASCADE, primary_key=False)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()


class Usuario(models.Model):
    email = models.CharField(validators=[validate_email])
    nombre = models.CharField(max_length=10)
    apellido = models.CharField(max_length=20)
    telefono = models.CharField(max_length=9, validators=[MinLengthValidator(9)])


class Observacion(models.Model):
    id = models.AutoField(primary_key=True)
    objeto = models.OneToOneField(Objeto, on_delete=models.CASCADE, primary_key=False)
    texto = models.TextField(max_length=300)
