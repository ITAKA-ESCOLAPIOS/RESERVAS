from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from reservas.forms import NewUserForm


@login_required(login_url='/login')
def reserva_but(request):
    return render(request, 'reserva_but.html')


@login_required(login_url='/login')
def reserva_que(request):
    return render(request, 'reserva_que.html')


@login_required(login_url='/login')
def reserva_tie(request):
    return render(request, 'reserva_tie.html')


@login_required(login_url='/login')
def catalogo(request):
    return render(request, 'catalogo.html')


@login_required(login_url='/login')
def submit_but(request, fecha_inicio, fecha_fin):
    pass


@login_required(login_url='/login')
def submit_que(request, fecha_inicio, fecha_fin):
    pass


@login_required(login_url='/login')
def submit_tie(request, fecha_inicio, fecha_fin):
    pass

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("catalogo")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="main/register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/catalogo/")
            else:
                messages.error(request, "Nombre de usuario o contraseña incorrectos.")
        else:
            messages.error(request, "Nombre de usuario o contraseña incorrectos.")
    form = AuthenticationForm()
    return render(request=request, template_name="main/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/login/")
