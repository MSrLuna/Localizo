import datetime
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.http import HttpResponseRedirect

from .forms import ContactForm, AddUserForm
from .models import Usuario, Administrador, Roles

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

@admin_required
def RenderRegister(request):
    roles = Roles.objects.all()
    if request.method == "POST":
        has_error = {}
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        username = request.POST.get('username')
        rol = request.POST.get('rol')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        telefono = request.POST.get('telefono')

        if password != confirm_password:
            has_error['password_final'] = 'Las contraseñas no coinciden'

        if not has_error:
            if rol == '2':
                user = Administrador(
                    nombre=nombre.title(),
                    apellido=apellido.title(),
                    rol=Roles.objects.get(id=rol),
                    email=username,
                    estado='Activo',
                    telefono=telefono
                )
                user.set_password(password)
                user.save()
            return render(request, 'admin/views/register.html', {'roles': roles})
        return render(request, 'admin/views/register.html', {'roles': roles, 'errores': has_error})
    return render(request, 'admin/views/register.html', {'roles': roles})

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
    return render(request, 'usuario/locales.html')

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
