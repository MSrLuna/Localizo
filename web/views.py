import datetime
from django.contrib import messages
#SESSION
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm
#HTTP
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from django.http import HttpResponseRedirect

from web.forms import AddUserForm

#MODEL
from .models import Usuario,Administrador , Roles, Producto, CategoriaProducto

#DECORADORES DE SESSION
def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        # rol_id se basan en los de bd
        if request.session.get('user_id') and request.session.get('rol_id') == '2':
            return view_func(request, *args, **kwargs)
        return redirect('Login')  # Redirige al login si no es admin
    return wrapper

# Control de Acceso
def RenderLogout(request):
    logout(request)  # Limpia la sesión del usuario
    return redirect('Login')

def RenderLogin(request):
    if request.method == "POST":
        has_error = {}
        chars_restringidos_user = [
            ' ', '..', '(', ')', '<', '>', '[',
            ']', ',', ';', ':', '"'
            ]
        
        username = request.POST.get('username')

        if username.strip() == "":
            has_error['username_empty'] = 'El Campo Usuario no Puede Estar Vacio'
        elif len(username) > 255:
            has_error['username_max_char'] = 'Se ha Superado el MAXIMO de Caracteres, MAXIMO Permitido: 255'
        else:
            invalid_char = []
            for char in username:
                if char in chars_restringidos_user:
                    invalid_char.append(char)
            if len(invalid_char) > 0:
                invalid_char_str = ', '.join(set(invalid_char))
                has_error['username_char_error'] = 'Caracter no Valido: {}.'.format(invalid_char_str)
        
        password = request.POST.get('password')
        if password.strip() == "":
            has_error['password_empty'] = 'El Campo Contraseña no Puede Estar Vacio'
        elif len(password) > 128:
            has_error['password_max_char'] = 'Se ha Superado el MAXIMO de Caracteres, MAXIMO Permitido: 128'
            
        if not has_error:
            try:
                username = username
                user = Usuario.objects.get(email=username)
                if user.check_password(password):
                    # SESSION DATA
                    request.session['user_id'] = user.id
                    request.session['email'] = user.email
                    request.session['rol_id'] = str(user.rol.id) 

                    if user.rol.id == 1:
                        # ESTO QUITARLO SI DA DRAMA ES PARA EL CARRO
                        request.session['rut'] = user.rut  
                        return redirect('home')
                    elif user.rol.id == 2:
                        return redirect('AdminHome')
                else:
                    has_error['cred_error'] = 'Las Credenciales no Coinciden'
            except Usuario.DoesNotExist:
                has_error['user_error'] = 'Usuario no Encontrado'
        return render(request, 'shared/login.html', {'errores': has_error})

    elif request.method == "GET":
        return render(request, 'shared/login.html')

@admin_required
def RenderRegister(request):
    roles = Roles.objects.all()
    if request.method == "POST":
        # USUARIO
        has_error = {}
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        username = request.POST.get('username')
        rol = request.POST.get('rol')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        telefono = request.POST.get('telefono')

        
        # VALIDACIONES GENERALES
        chars_restringidos_correo = [
            ' ', '..', '(', ')', '<', '>', '[',
            ']', ',', ';', ':', '"', '@'
            ]
        
        if nombre.strip() == "":
            has_error['name_empty'] = 'El Campo NOMBRE no Puede Estar Vacio'
        elif len(nombre) > 150:
            has_error['name_max_char'] = 'Se ha Superado el MAXIMO de Caracteres, MAXIMO Permitido: 150'
        else:
            nombre = nombre.title()

        if telefono.strip() == "":
            has_error['telefono_empty'] = 'El Campo TELEFONO no Puede Estar Vacio'

        if apellido.strip() == "":
            has_error['ape_empty'] = 'El Campo Apellido no Puede Estar Vacio'
        elif len(apellido) > 150:
            has_error['ape_max_char'] = 'Se ha Superado el MAXIMO de Caracteres, MAXIMO Permitido: 150'
        else:
            apellido = apellido.title()

        if username.strip() == "":
            has_error['username_empty'] = 'El Campo CORREO no Puede Estar Vacio'
        else:
            invalid_char = []
            for char in username:
                if char in chars_restringidos_correo:
                    invalid_char.append(char)
            if len(invalid_char) > 0:
                invalid_char_str = ', '.join(set(invalid_char))
                has_error['username_char_error'] = 'Caracter no Valido: {}.'.format(invalid_char_str)
        
        if rol == '-1':
            has_error['rol_default'] = 'El Campo ROL Debe ser DISTINTO al PREDETERMINADO'

        if password.strip() == "":
            has_error['password_empty'] = 'El Campo Contraseña no Puede Estar Vacio'
        elif len(password) > 128:
            has_error['password_max_char'] = 'Se ha Superado el MAXIMO de Caracteres, MAXIMO Permitido: 128'
        
        if confirm_password.strip() == "":
            has_error['con_pass_empty'] = 'El Campo de Confirmacion de Contraseña no Puede Estar Vacio'
        elif len(confirm_password) > 128:
            has_error['con_pass_max_char'] = 'Se ha Superado el MAXIMO de Caracteres, MAXIMO Permitido: 128'

        if password != confirm_password:
            has_error['password_final'] = 'Las contraseñas no coinciden'     

        # VALIDAR EXISTENCIA DEL OBJETO

        if not has_error:
            if rol == '2':
                user = Administrador(
                    nombre=nombre,
                    apellido=apellido,
                    rol=Roles.objects.get(id=rol),
                    email= username + '@nufra.com',
                    estado= 'Activo',
                    telefono=telefono
                )
                user.set_password(password)
                user.save()

            return render(request, 'admin/views/register.html', {'roles': roles})
        else:
            return render(request, 'admin/views/register.html', {'roles': roles, 'errores': has_error})
    
    elif request.method == "GET":
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

def RenderUserHome(request):
    return render(request, 'usuario/inicio.html')

def RenderUserCatalog(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id', None)
        # Filtros para visualizar solo las categorias con productos 
        categorias_con_productos = CategoriaProducto.objects.filter(producto__isnull=False).distinct()
        productos = Producto.objects.filter(categoria__in=categorias_con_productos)

        return render(request, 'usuario/locales.html', {
            'categorias': categorias_con_productos, 
            'productos': productos, 
            'user_id': user_id,
            })

def RenderAbout(request):
    return render(request, 'usuario/nosotros.html')

def RenderFAQ(request):
    return render(request, 'usuario/contacto.html')

# Admin
@admin_required
def RenderAdminHome(request):
    return render(request, 'admin/views/inicio.html')

@admin_required
def RenderTrabajadores(request):
    users = Usuario.objects.all()
    adm = Administrador.objects.all()
    return render(request, 'admin/views/trabajadores.html',{'users': users, 'adm': adm})



# Categorias
@admin_required
def RenderCategorias(request):
    categorias = CategoriaProducto.objects.all()
    if request.method == 'POST':
        has_error = {}
        nombre = request.POST.get('nombre')

        if nombre == "":
            has_error['name_empty'] = 'El NOMBRE NO puede estar VACIO'
        elif len(nombre) > 50:
            has_error['name_max_char'] = 'Se ha Superado el MAXIMO de Caracteres, MAXIMO Permitido: 50'
        else:
            nombre = nombre.title()

        if not has_error:
            categoria = CategoriaProducto(nombre=nombre)
            categoria.save()
            return redirect('categorias')
        else:
            return render(request, 'admin/productos/categorias/categorias.html', {'categorias': categorias, 'errores':has_error})
        
    elif request.method == 'GET':
        return render(request, 'admin/productos/categorias/categorias.html', {'categorias': categorias})

@admin_required
def EditCategoria(request, id):
    categorias = CategoriaProducto.objects.all()
    categoria = get_object_or_404(CategoriaProducto, id=id)

    if request.method == 'POST':
        has_error = {}
        nombre = request.POST.get('nombre')

        # Validaciones de datos
        if not nombre:
            has_error['name_empty'] = 'El NOMBRE NO puede estar VACIO'
        elif len(nombre) > 50:
            has_error['name_max_char'] = 'Se ha Superado el MAXIMO de Caracteres, MAXIMO Permitido: 50'
        else:
            nombre = nombre.title()

        if not has_error:
            categoria.nombre = nombre
            categoria.save()
            return redirect('categorias')
        else:
            return render(request, 'admin/productos/categorias/categorias.html', {
                'categorias': categorias,
                'editable': categoria,
                'errores': has_error
            })

    elif request.method == 'GET':
        return render(request, 'admin/productos/categorias/categorias.html', {
            'categorias': categorias,
            'editable': categoria
        })

@admin_required 
def EliminarCategoria(request, id):
    if request.method == 'GET':
        try:
            categoria = CategoriaProducto.objects.get(id=id)
            categoria.delete()  # Eliminar la categoría de la base de datos
            return redirect('categorias')
        except CategoriaProducto.DoesNotExist:
            return HttpResponse("La categoría no existe.", status=404)
        except Exception as e:
            return HttpResponse(f"Error al eliminar la categoria: {e}", status=404)

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Enviar el correo
            send_mail(
                f"Nuevo mensaje de {name}",  # Asunto
                f"De: {name}\nCorreo: {email}\n\n{message}",  # Cuerpo del mensaje
                email,  # Dirección de quien envía el correo
                [settings.EMAIL_HOST_USER],  # Dirección de destino (tu correo)
                fail_silently=False,
            )
            return HttpResponseRedirect('/gracias/')  # Redirige a una página de agradecimiento (puedes crearla)
    else:
        form = ContactForm()

    return render(request, 'contacto.html', {'form': form})