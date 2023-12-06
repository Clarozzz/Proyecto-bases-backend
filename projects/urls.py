from django.urls import path
from .views import *

urlpatterns = [
    path('tipoUsuario/', tipoUsuarioView.as_view(), name='tipoUsuario'),
    path('tipoUsuario/<int:id>/', tipoUsuarioView.as_view(), name='tipoUsuario_process'),
    path('usuario/', UsuariosView.as_view(), name='usuario'),
    path('usuario/<int:id>/', UsuariosView.as_view(), name='usuario_process'),
    path('telefonos/', TelefonosView.as_view(), name='telefonos'),
    path('telefonos/<int:usuario_id>/', TelefonosView.as_view(), name='telefonos_usuario'),
    path('telefonos/<int:telefono_id>/', TelefonosView.as_view(), name='telefonos_detalle'),
    path('perfiles/', PerfilesView.as_view(), name='perfiles'),
    path('perfiles/<int:usuario_id>/', PerfilesView.as_view(), name='perfiles_usuario'),
]