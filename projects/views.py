from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json
from django.contrib.auth import authenticate, login

# Create your views here.
class tipoUsuarioView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if (id > 0):
            tipos=list(tipoUsuario.objects.filter(id=id).values())
            if len(tipos) > 0:
                tipo = tipos[0]
                datos = {'message':'Success', 'tipos':tipo}
            else:
                datos = {'message':'tipo no encontrado'}
            return JsonResponse(datos)
        else:
            tipos = list(tipoUsuario.objects.values())
            if len(tipos) > 0:
                datos = {'message':'Success', 'tipos':tipos}
            else:
                datos = {'message':'tipos no encontrados'}
            return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body)
        tipoUsuario.objects.create(tipo=jd['tipo'])
        datos = {'message':'Success'}
        return JsonResponse(datos)

    def put(self, request, id):
        jd = json.loads(request.body)
        tipos=list(tipoUsuario.objects.filter(id=id).values())
        if len(tipos) > 0:
            tipo = tipoUsuario.objects.get(id=id)
            tipo.tipo = jd['tipo']
            tipo.save()
            datos = {'message':'Success'}
        else:
            datos = {'message':'tipo no encontrado'}
        return JsonResponse(datos)

    def delete(self, request, id):
        tipos=list(tipoUsuario.objects.filter(id=id).values())
        if len(tipos) > 0:
            tipoUsuario.objects.filter(id=id).delete()
            datos = {'message':'Success'}
        else:
            datos = {'message':'tipo no encontrado'}
        return JsonResponse(datos)

    
        
## Clientes 

class UsuariosView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if id > 0:
            usuario_data = list(usuarios.objects.filter(id=id).values('id', 'correo', 'contrasena', 'fechaRegistro', 'tipoUsuario__tipo'))
            if len(usuario_data) > 0:
                usuario = usuario_data[0]
                datos = {'message': 'Success', 'usuario': usuario}
            else:
                datos = {'message': 'Usuario no encontrado'}
            return JsonResponse(datos)
        else:
            usuarios_data = list(usuarios.objects.values('id', 'correo', 'contrasena', 'fechaRegistro', 'tipoUsuario__tipo'))
            if len(usuarios_data) > 0:
                datos = {'message': 'Success', 'usuarios': usuarios_data}
            else:
                datos = {'message': 'Usuarios no encontrados'}
            return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body)
        correo_existente = usuarios.objects.filter(correo=jd['correo']).exists()

        if correo_existente:
            datos = {'message': 'Correo ya registrado. Intente con otro correo.'}
        else:
            try:
                tipo_usuario = tipoUsuario.objects.get(id=jd['tipoUsuario'])
                usuario = usuarios.objects.create(
                    correo=jd['correo'],
                    contrasena=jd['contrasena'],
                    tipoUsuario=tipo_usuario
                )
                datos = {'message': 'Success', 'usuario_id': usuario.id}
            except tipoUsuario.DoesNotExist:
                datos = {'message': 'Tipo de usuario no encontrado'}
            except Exception as e:
                datos = {'message': f'Error: {str(e)}'}

        return JsonResponse(datos)

    def put(self, request, id):
        jd = json.loads(request.body)
        usuario_data = list(usuarios.objects.filter(id=id).values())
        if len(usuario_data) > 0:
            try:
                tipo_usuario = tipoUsuario.objects.get(id=jd['tipoUsuario'])
                usuario = usuarios.objects.get(id=id)
                usuario.correo = jd['correo']
                usuario.contrasena = jd['contrasena']
                usuario.tipoUsuario = tipo_usuario
                usuario.save()
                datos = {'message': 'Success'}
            except tipoUsuario.DoesNotExist:
                datos = {'message': 'Tipo de usuario no encontrado'}
            except Exception as e:
                datos = {'message': f'Error: {str(e)}'}
        else:
            datos = {'message': 'Usuario no encontrado'}
        return JsonResponse(datos)

    def delete(self, request, id):
        usuario_data = list(usuarios.objects.filter(id=id).values())
        if len(usuario_data) > 0:
            usuarios.objects.filter(id=id).delete()
            datos = {'message': 'Success'}
        else:
            datos = {'message': 'Usuario no encontrado'}
        return JsonResponse(datos)

##telefonos

class TelefonosView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, usuario_id=0):
        if usuario_id > 0:
            try:
                usuario = usuarios.objects.get(id=usuario_id)
                telefonos_data = list(telefonos.objects.filter(usuarioId=usuario_id).values())
                if len(telefonos_data) > 0:
                    telefonos_list = telefonos_data
                    usuario_info = {
                        'id': usuario.id,
                        'correo': usuario.correo,
                        # Agrega más campos según sea necesario
                    }
                    datos = {'message': 'Success', 'usuario': usuario_info, 'telefonos': telefonos_list}
                else:
                    datos = {'message': 'Telefonos no encontrados para el usuario', 'usuario': {}}
            except usuarios.DoesNotExist:
                datos = {'message': 'Usuario no encontrado'}
        else:
            telefonos_data = list(telefonos.objects.values())
            if len(telefonos_data) > 0:
                datos = {'message': 'Success', 'telefonos': telefonos_data}
            else:
                datos = {'message': 'Telefonos no encontrados'}

        return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body)
        usuario_id = jd.get('usuarioId', '')
        telefono = jd.get('telefono', '')

        # Verificar si el usuario existe antes de agregar el teléfono
        if usuarios.objects.filter(id=usuario_id).exists():
            telefono_obj = telefonos.objects.create(usuarioId_id=usuario_id, telefono=telefono)
            datos = {'message': 'Success', 'telefono_id': telefono_obj.id}
        else:
            datos = {'message': 'Usuario no encontrado'}

        return JsonResponse(datos)

    def put(self, request, telefono_id):
        jd = json.loads(request.body)
        telefonos_data = list(telefonos.objects.filter(id=telefono_id).values())

        if len(telefonos_data) > 0:
            telefono = telefonos.objects.get(id=telefono_id)
            telefono.telefono = jd.get('telefono', '')
            telefono.save()
            datos = {'message': 'Success'}
        else:
            datos = {'message': 'Teléfono no encontrado'}

        return JsonResponse(datos)

    def delete(self, request, telefono_id):
        telefonos_data = list(telefonos.objects.filter(id=telefono_id).values())

        if len(telefonos_data) > 0:
            telefonos.objects.filter(id=telefono_id).delete()
            datos = {'message': 'Success'}
        else:
            datos = {'message': 'Teléfono no encontrado'}

        return JsonResponse(datos)

class PerfilesView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, usuario_id=0):
        if usuario_id > 0:
            try:
                usuario = usuarios.objects.get(id=usuario_id)
                perfiles_data = list(perfiles.objects.filter(usuario=usuario_id).values())
                if len(perfiles_data) > 0:
                    perfiles_list = perfiles_data
                    usuario_info = {
                        'id': usuario.id,
                        'correo': usuario.correo,
                        # Agrega más campos según sea necesario
                    }
                    datos = {'message': 'Success', 'usuario': usuario_info, 'perfiles': perfiles_list}
                else:
                    datos = {'message': 'Perfiles no encontrados para el usuario', 'usuario': {}}
            except usuarios.DoesNotExist:
                datos = {'message': 'Usuario no encontrado'}
        else:
            perfiles_data = list(perfiles.objects.values())
            if len(perfiles_data) > 0:
                datos = {'message': 'Success', 'perfiles': perfiles_data}
            else:
                datos = {'message': 'Perfiles no encontrados'}

        return JsonResponse(datos)

