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
from django.conf import settings

from datetime import datetime

from reservas.forms import NewUserForm
from reservas.models import Butanito, FuturasReservas, HistoricoReservas, Observacion, Tienda, Usuario, Quemador


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
    butanito_count = Butanito.objects.count()
    quemador_count = Quemador.objects.count()
    tienda_count = Tienda.objects.count()
    # Cada vez que se carga el catálogo se aprovecha para filtrar las reservas futuras y pasarlas a históricas si ya
    # han pasado.
    for reservaFutura in FuturasReservas.objects.all():
        p_fecha_fin = datetime.strptime(str(reservaFutura.fecha_fin), '%Y-%m-%d')
        p_fecha_fin = p_fecha_fin.date()
        if p_fecha_fin < datetime.date(datetime.today()):
            r_pasada = HistoricoReservas(id=reservaFutura.id,
                                         nombre=reservaFutura.nombre,
                                         apellido=reservaFutura.apellido,
                                         email=reservaFutura.email, telefono=reservaFutura.telefono,
                                         fecha_inicio=reservaFutura.fecha_inicio,
                                         fecha_fin=reservaFutura.fecha_fin,
                                         content_type=reservaFutura.content_type_id,
                                         object_id=reservaFutura.object_id)
            r_pasada.save()
            reservaFutura.delete()
    return render(request, 'catalogo.html', context={"butanito_count": butanito_count, "quemador_count": quemador_count,
                                                     "tienda_count": tienda_count})


@login_required(login_url='/login')
def submit_but(request):
    p_fecha_inicio, p_fecha_fin = __parse_datetime_to_date(request)
    reserva_es_posible = False

    # Iterar los butanitos del sistema a ver si está alguno libre en esas fechas
    for butanito in Butanito.objects.all():
        print("Chequeando id...")
        current_id = butanito.id_obj
        print(current_id)
        reserva_es_posible = True
        reservas_futuras = FuturasReservas.objects.filter(object_id=current_id)
        if not reservas_futuras:
            p_id, context_fecha_inicio, context_fecha_fin = __hacer_reserva(request, p_fecha_inicio, p_fecha_fin,
                                                                            current_id, "butanito", request.user)
            mensaje = "La reserva se ha completado satisfactoriamente. Se te ha asignado el butanito " + \
                      str(p_id) + " del " + str(context_fecha_inicio) + " al " + str(context_fecha_fin)
            break
        else:
            for reserva in reservas_futuras:
                # Si no se solapan las fechas entra en el if
                if __avaiable(reserva, p_fecha_inicio, p_fecha_fin):
                    pass
                # Si se solapan las fechas
                else:
                    reserva_es_posible = False
                    print("Se solapan fechas, buscando otro butanito...")
                    break
        if reserva_es_posible:
            p_id, context_fecha_inicio, context_fecha_fin = __hacer_reserva(request, p_fecha_inicio, p_fecha_fin,
                                                                            current_id, "butanito", request.user)
            mensaje = "La reserva se ha completado satisfactoriamente. Se te ha asignado el butanito " + \
                      str(p_id) + " del " + str(context_fecha_inicio) + " al " + str(context_fecha_fin)
    if not reserva_es_posible:
        mensaje = "No hay ningún butanito disponible en esas fechas. No se ha completado la reserva :("

    return redirect('/resultado_reserva/' + mensaje)


@login_required(login_url='/login')
def submit_que(request):
    p_fecha_inicio, p_fecha_fin = __parse_datetime_to_date(request)
    reserva_es_posible = False

    # Iterar los quemadores del sistema a ver si está alguno libre en esas fechas
    for quemador in Quemador.objects.all():
        print("Chequeando id...")
        current_id = quemador.id_obj
        print(current_id)
        reserva_es_posible = True
        reservas_futuras = FuturasReservas.objects.filter(object_id=current_id)
        if not reservas_futuras:
            p_id, context_fecha_inicio, context_fecha_fin = __hacer_reserva(request, p_fecha_inicio, p_fecha_fin,
                                                                            current_id, "quemador", request.user)
            mensaje = "La reserva se ha completado satisfactoriamente. Se te ha asignado el quemador " + \
                      str(p_id) + " del " + str(context_fecha_inicio) + " al " + str(context_fecha_fin)
            break
        else:
            for reserva in reservas_futuras:
                # Si no se solapan las fechas entra en el if
                if __avaiable(reserva, p_fecha_inicio, p_fecha_fin):
                    pass
                # Si se solapan las fechas
                else:
                    reserva_es_posible = False
                    print("Se solapan fechas, buscando otro quemador...")
                    break
        if reserva_es_posible:
            p_id, context_fecha_inicio, context_fecha_fin = __hacer_reserva(request, p_fecha_inicio, p_fecha_fin,
                                                                            current_id, "quemador", request.user)
            mensaje = "La reserva se ha completado satisfactoriamente. Se te ha asignado el quemador  " + \
                      str(p_id) + " del " + str(context_fecha_inicio) + " al " + str(context_fecha_fin)
    if not reserva_es_posible:
        mensaje = "No hay ningún quemador disponible en esas fechas. No se ha completado la reserva :("

    return redirect('/resultado_reserva/' + mensaje)


def resultado_reserva(request, mensaje):
    return render(request, 'resultado_reserva.html', context={"mensaje": mensaje, "user": request.user})


@login_required(login_url='/login')
def submit_tie(request):
    p_fecha_inicio, p_fecha_fin = __parse_datetime_to_date(request)
    reserva_es_posible = False

    # Iterar las tiendas del sistema a ver si está alguna libre en esas fechas
    for tienda in Tienda.objects.all():
        print("Chequeando id...")
        current_id = tienda.id_obj
        print(current_id)
        reserva_es_posible = True
        reservas_futuras = FuturasReservas.objects.filter(object_id=current_id)
        if not reservas_futuras:
            p_id, context_fecha_inicio, context_fecha_fin = __hacer_reserva(request, p_fecha_inicio, p_fecha_fin,
                                                                            current_id, "tienda", request.user)
            mensaje = "La reserva se ha completado satisfactoriamente. Se te ha asignado la tienda " + \
                      str(p_id) + " del " + str(context_fecha_inicio) + " al " + str(context_fecha_fin)
            break
        else:
            for reserva in reservas_futuras:
                # Si no se solapan las fechas entra en el if
                if __avaiable(reserva, p_fecha_inicio, p_fecha_fin):
                    pass
                # Si se solapan las fechas
                else:
                    reserva_es_posible = False
                    print("Se solapan fechas, buscando otra tienda...")
                    break
        if reserva_es_posible:
            p_id, context_fecha_inicio, context_fecha_fin = __hacer_reserva(request, p_fecha_inicio, p_fecha_fin,
                                                                            current_id, "tienda", request.user)
            mensaje = "La reserva se ha completado satisfactoriamente. Se te ha asignado la tienda " + \
                      str(p_id) + " del " + str(context_fecha_inicio) + " al " + str(context_fecha_fin)
    if not reserva_es_posible:
        mensaje = "No hay ninguna tienda disponible en esas fechas. No se ha completado la reserva :("

    return redirect('/resultado_reserva/' + mensaje)


def mis_reservas(request):
    return render(request, 'mis_reservas.html',
                  context={"reservasFuturas": FuturasReservas.objects.filter(email=request.user.email).order_by(
                      'fecha_inicio'),
                      "reservasAntiguas": HistoricoReservas.objects.filter(email=request.user.email).order_by(
                          'fecha_inicio'),
                      "tiendas": Tienda.objects.all()})


def eliminar_reserva(request, p_id):
    FuturasReservas.objects.filter(id=p_id).delete()
    subject = "Reserva eliminada"
    email_template_name = "main/reserva_eliminada.txt"
    c = {
        "email": request.user.email,
        "id_reserva": p_id,
        "nombre": request.user.username,
    }
    email = render_to_string(email_template_name, c)
    try:
        send_mail(subject, email, settings.EMAIL_HOST_USER, ["reservas.itakaescolapios@gmail.com"], fail_silently=False)
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    return redirect('/mis_reservas')


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
                    subject = "Solicitud de cambio de contraseña"
                    email_template_name = "main/password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': 'gilillo32.pythonanywhere.com',  # TODO cambiar en producción
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="main/password/password_reset.html",
                  context={"password_reset_form": password_reset_form})


# AUXILIARES:

def __hacer_reserva(request, p_fecha_inicio, p_fecha_fin, current_id, object_type, user):
    """Hace una reserva en el sistema. Método genérico para reservar cualquier tipo de objeto."""

    phone = Usuario.objects.get(username=request.user.username).telefono

    if str(object_type).lower() == "butanito":
        content_type_id = ContentType.objects.get_for_model(Butanito).id
    elif str(object_type).lower() == "quemador":
        content_type_id = ContentType.objects.get_for_model(Quemador).id
    elif str(object_type).lower() == "tienda":
        content_type_id = ContentType.objects.get_for_model(Tienda).id
    else:
        content_type_id = ""
    r = FuturasReservas(nombre=request.user.username,
                        apellido=request.user.last_name, email=request.user.email, telefono=phone,
                        fecha_inicio=p_fecha_inicio, fecha_fin=p_fecha_fin,
                        content_type_id=content_type_id,
                        object_id=current_id)
    r.save()
    subject = "Nueva reserva"
    email_template_name = "main/reserva_hecha.txt"
    c = {
        "email": user.email,
        "objeto": current_id,
        "nombre": user.username,
        "fecha_inicio": p_fecha_inicio,
        "fecha_fin": p_fecha_fin,
        "telefono": phone,
    }
    email = render_to_string(email_template_name, c)
    try:
        send_mail(subject, email, settings.EMAIL_HOST_USER, ["reservas.itakaescolapios@gmail.com"], fail_silently=False)
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    print("Reserva guardada.")
    return current_id, p_fecha_inicio, p_fecha_fin


def __avaiable(reserva, p_fecha_inicio, p_fecha_fin):
    # Si no se solapan las fechas devuelve True, False si se solapan.
    return True if not ((reserva.fecha_inicio <= p_fecha_inicio <= reserva.fecha_fin) or
                        (reserva.fecha_inicio <= p_fecha_fin <= reserva.fecha_fin) or
                        (reserva.fecha_inicio <= p_fecha_inicio <= p_fecha_fin < reserva.fecha_fin) or
                        (p_fecha_inicio <= reserva.fecha_inicio <= reserva.fecha_fin <= p_fecha_fin)) else False


def __parse_datetime_to_date(request):
    # Conseguir fechas del formulario y parsearlas a date y no datetime.
    p_fecha_inicio = request.POST.get('date-desde')
    p_fecha_inicio = datetime.strptime(p_fecha_inicio, '%Y-%m-%d')
    p_fecha_inicio = p_fecha_inicio.date()
    p_fecha_fin = request.POST.get('date-hasta')
    p_fecha_fin = datetime.strptime(p_fecha_fin, '%Y-%m-%d')
    p_fecha_fin = p_fecha_fin.date()

    return p_fecha_inicio, p_fecha_fin
