from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from web import views as vistas

urlpatterns = [
    # Principal
    path('', vistas.RenderInicio, name='home'),

    # Control de acceso
    path('login/', vistas.RenderLogin, name='Login'),
    path('registro/administrador/', vistas.RenderRegister, name='RegisterADM'),
    path('registro/', vistas.register_view, name='RegisterUSER'),
    path('logout/', vistas.RenderLogout, name='LogOut'),
    
    # Usuario
    path('locales/', vistas.RenderLocales, name='Locales'),
    path('acerca-de/', vistas.RenderNosotros, name='Nosotros'),
    path('contacto/', vistas.RenderContacto, name='Contacto'),

    # Admin
    path('home/administrador/', vistas.RenderAdminHome, name='AdminHome'),
    path('home/administrador/trabajadores/', vistas.RenderTrabajadores, name='Trabajadores'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
