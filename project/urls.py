from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from web import views as vistas
from django.urls import re_path

urlpatterns = [
    # Principal
    path('', vistas.RenderUserHome, name='home'),

    # Control de acceso
    path('login/', vistas.RenderLogin, name='Login'),
    path('registro/administrador/', vistas.RenderRegister, name='RegisterADM'),
    path('registro/', vistas.register_view, name='RegisterUSER'),
    path('logout/', vistas.RenderLogout, name='LogOut'),
    
    # Usuario
    path('locales/', vistas.RenderUserCatalog, name='Catalog'),
    path('acerca-de/', vistas.RenderAbout, name='About'),
    path('contacto/', vistas.RenderFAQ, name='FAQ'),

    # Admin
    path('home/administrador/', vistas.RenderAdminHome, name='AdminHome'),
    path('home/administrador/trabajadores/', vistas.RenderTrabajadores, name='Trabajadores'),

        # Categorias
    path('home/administrador/configuracion/productos/categorias/', vistas.RenderCategorias, name='categorias'),
    path('home/administrador/configuracion/productos/categorias/edit-categoria/<int:id>/', vistas.EditCategoria, name='editCategoria'),
    
        # Block/Unblock categoria
    path('home/admin/config/productos/categorias/delete-categoria/<int:id>/', vistas.EliminarCategoria, name='deleteCategoria'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
