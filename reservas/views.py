from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'reserva.html')


def catalogo(request):
    return render(request, 'catalogo.html')
