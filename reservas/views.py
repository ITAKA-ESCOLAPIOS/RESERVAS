from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from datetime import datetime

from reservas.forms import NewUserForm
from reservas.models import Butanito, FuturasReservas, HistoricoReservas, Observacion, Tienda, Usuario


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
def submit_but(request):
    p_fecha_inicio = request.POST.get('date-desde')
    p_fecha_inicio = datetime.strptime(p_fecha_inicio, '%Y-%m-%d')
    p_fecha_inicio = p_fecha_inicio.date()
    p_fecha_fin = request.POST.get('date-hasta')
    p_fecha_fin = datetime.strptime(p_fecha_fin, '%Y-%m-%d')
    p_fecha_fin = p_fecha_fin.date()
    for butanito in Butanito.objects.all():
        print("Chequeando id...")
        current_id = butanito.id_obj
        print(current_id)
        encontrado = False
        for reserva in FuturasReservas.objects.filter(object_id=current_id):
            # Si no se solapan las fechas entra en el if
            print(reserva.fecha_inicio)
            if not ((reserva.fecha_inicio <= p_fecha_inicio <= reserva.fecha_fin) or
                    (reserva.fecha_inicio <= p_fecha_fin <= reserva.fecha_fin) or
                    (reserva.fecha_inicio <= p_fecha_inicio <= p_fecha_fin < reserva.fecha_fin) or
                    (p_fecha_inicio <= reserva.fecha_inicio <= reserva.fecha_fin <= p_fecha_fin)):
                phone = Usuario.objects.get(username=request.user.username).telefono
                r = FuturasReservas(nombre=request.user.username,
                                    apellido=request.user.last_name, email=request.user.email, telefono=phone,
                                    fecha_inicio=p_fecha_inicio, fecha_fin=p_fecha_fin,
                                    content_type_id=ContentType.objects.get_for_model(Butanito).id,
                                    object_id=current_id)
                r.save()
                print("Reserva guardada")
                encontrado = True
                break
            else:
                print("Se solapan fechas")
        if not encontrado:
            print("No hay ninguno disponible para reservar :(")

    return redirect('/catalogo/')


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
            return redirect("/catalogo")
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


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = Usuario.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "main/password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="main/password/password_reset.html",
                  context={"password_reset_form": password_reset_form})
