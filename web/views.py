import datetime
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404, redirect, render
from django.core.mail import send_mail
from django.http import HttpResponseRedirect

from .forms import CiudadForm, ContactForm, AddUserForm, LocalComercialForm, tipoLocalForm
from .models import Ciudad, LocalComercial, TipoLocal, Usuario, Administrador, Roles

# DECORADORES DE SESSION
def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('user_id') and request.session.get('rol_id') == '2':
            return view_func(request, *args, **kwargs)
        return redirect('Login')
    return wrapper

# Control de Acceso
def RenderLogout(request):
    logout(request)
    return redirect('Login')

def RenderLogin(request):
    if request.method == "POST":
        has_error = {}
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Validaciones básicas
        if username.strip() == "":
            has_error['username_empty'] = 'El Campo Usuario no Puede Estar Vacio'
        if password.strip() == "":
            has_error['password_empty'] = 'El Campo Contraseña no Puede Estar Vacio'

        if not has_error:
            try:
                user = Usuario.objects.get(email=username)
                if user.check_password(password):
                    request.session['user_id'] = user.id
                    request.session['email'] = user.email
                    request.session['rol_id'] = str(user.rol.id) 

                    if user.rol.id == 1:
                        return redirect('home')
                    elif user.rol.id == 2:
                        return redirect('AdminHome')
                else:
                    has_error['cred_error'] = 'Las Credenciales no Coinciden'
            except Usuario.DoesNotExist:
                has_error['user_error'] = 'Usuario no Encontrado'
        return render(request, 'shared/login.html', {'errores': has_error})
    return render(request, 'shared/login.html')

# Usuario General
def register_view(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.estado = 'n/a'
            user.rol = Roles.objects.get(id=1)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('home')
    else:
        form = AddUserForm()
    return render(request, 'usuario/register.html', {'form': form})

def RenderInicio(request):
    return render(request, 'usuario/inicio.html')

def RenderLocales(request):
    locales = LocalComercial.objects.all()  # Recupera todos los locales comerciales
    return render(request, 'usuario/locales.html', {'locales': locales})

def RenderNosotros(request):
    return render(request, 'usuario/nosotros.html')

def RenderContacto(request):
    return render(request, 'usuario/contacto.html')

# Admin
@admin_required
def RenderAdminHome(request):
    return render(request, 'admin/views/inicio.html')

@admin_required
def RenderTrabajadores(request):
    users = Usuario.objects.all()
    adm = Administrador.objects.all()
    return render(request, 'admin/views/trabajadores.html', {'users': users, 'adm': adm})

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            send_mail(
                f"Nuevo mensaje de {form.cleaned_data['name']}",
                f"De: {form.cleaned_data['name']}\nCorreo: {form.cleaned_data['email']}\n\n{form.cleaned_data['message']}",
                form.cleaned_data['email'],
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            return HttpResponseRedirect('/gracias/')
    form = ContactForm()
    return render(request, 'contacto.html', {'form': form})

@admin_required
def gestion_ciudades(request):
    ciudades = Ciudad.objects.all()
    form = CiudadForm()

    if request.method == 'POST':
        form = CiudadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ciudad agregada exitosamente.')
            return redirect('GestionCiudades')  # Recarga la página para mostrar la nueva ciudad

    return render(request, 'admin/job/ciudades.html', {'ciudades': ciudades, 'form': form})

@admin_required
def eliminar_ciudad(request, ciudad_id):
    try:
        ciudad = Ciudad.objects.get(id=ciudad_id)
        ciudad.delete()
        messages.success(request, f'La ciudad "{ciudad.nombre}" ha sido eliminada exitosamente.')
    except Ciudad.DoesNotExist:
        messages.error(request, 'La ciudad no existe.')
    return redirect('GestionCiudades')

@admin_required
def gestion_tipoLocal(request):
    tipoLocales = TipoLocal.objects.all()  # Aquí ya estás obteniendo los tipos de local
    form = tipoLocalForm()

    if request.method == 'POST':
        form = tipoLocalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de Local agregado exitosamente.')
            return redirect('GestionTipoLocal')  # Recarga la página para mostrar el nuevo tipo de local

    return render(request, 'admin/job/tipoLocales.html', {'tipoLocales': tipoLocales, 'form': form})

@admin_required
def eliminar_tipoLocal(request, tipo_id):
    try:
        tipoLocal = TipoLocal.objects.get(id=tipo_id)
        tipoLocal.delete()
        messages.success(request, f'El tipo de local "{tipoLocal.nombre}" ha sido eliminado exitosamente.')
    except TipoLocal.DoesNotExist:
        messages.error(request, 'El tipo de local no existe.')
    return redirect('GestionTipoLocal')

@admin_required
def gestion_locales_comerciales(request):
    locales = LocalComercial.objects.all()
    tipos_local = TipoLocal.objects.all()
    ciudades = Ciudad.objects.all()

    form = LocalComercialForm()

    if request.method == 'POST':
        form = LocalComercialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Local Comercial agregado exitosamente.')
            return redirect('GestionLocalesComerciales')  # Recarga la página para mostrar el nuevo local

    return render(request, 'admin/job/localesComerciales.html', {
        'locales': locales,
        'form': form,
        'tipos_local': tipos_local,
        'ciudades': ciudades
    })

@admin_required
def eliminar_local(request, local_id):
    try:
        local = get_object_or_404(LocalComercial, id=local_id)
        local.delete()
        messages.success(request, f'El local comercial "{local.nombre}" ha sido eliminado exitosamente.')
    except LocalComercial.DoesNotExist:
        messages.error(request, 'El local comercial no existe.')
    return redirect('GestionLocalesComerciales')

def ver_local(request, id):
    local = get_object_or_404(LocalComercial, id=id)
    return render(request, 'verLocal.html', {'local': local})