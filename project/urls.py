from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from web import views as v

urlpatterns = [
    # Principal
    path('', v.RenderInicio, name='home'),

    # Control de acceso
    path('login/', v.RenderLogin, name='Login'),
    path('registro/', v.register_view, name='RegisterUSER'),
    path('logout/', v.RenderLogout, name='LogOut'),
    
    # Usuario
    path('locales/', v.RenderLocales, name='Locales'),
    path('locales/<int:id>/', v.ver_local, name='ver_local'),
    path('acerca-de/', v.RenderNosotros, name='Nosotros'),
    path('contacto/', v.RenderContacto, name='Contacto'),

    # Admin
    path('home/administrador/', v.RenderAdminHome, name='AdminHome'),
    path('home/administrador/ciudades/', v.gestion_ciudades, name='GestionCiudades'),
    path('home/administrador/ciudades/eliminar/<int:ciudad_id>/', v.eliminar_ciudad, name='EliminarCiudad'),
    path('home/administrador/tipos-locales/', v.gestion_tipoLocal, name='GestionTipoLocal'),
    path('home/administrador/tipos-locales/eliminar/<int:tipo_id>/', v.eliminar_tipoLocal, name='EliminarTipoLocal'),
    path('gestion/locales/', v.gestion_locales_comerciales, name='GestionLocalesComerciales'),
    path('home/administrador/locales/eliminar/<int:local_id>/', v.eliminar_local, name='EliminarLocal'),
    path('home/administrador/usuarios/', v.gestion_usuarios, name='GestionUsuarios'),
    path('home/administrador/usuarios/eliminar/<int:usuario_id>/', v.eliminar_usuario, name='EliminarUsuario'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
