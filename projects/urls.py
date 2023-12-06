from django.urls import path
from .views import *

urlpatterns = [
    path('tipoUsuario/', tipoUsuarioView.as_view(), name='tipoUsuario'),
    path('tipoUsuario/<int:id>/', tipoUsuarioView.as_view(), name='tipoUsuario_process')
]