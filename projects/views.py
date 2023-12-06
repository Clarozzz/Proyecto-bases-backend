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

    def post(self, request):
        jd = json.loads(request.body)
        correo = jd.get('correo', '')

        try:
            usuario = usuarios.objects.get(correo=correo)
            perfiles.objects.create(usuario=usuario, nombre=jd['nombre'])
            datos = {'message': 'Success'}
        except usuarios.DoesNotExist:
            datos = {'message': 'Usuario no encontrado'}

        return JsonResponse(datos)

    def put(self, request, perfil_id):
        jd = json.loads(request.body)
        try:
            perfil = perfiles.objects.get(id=perfil_id)
            perfil.nombre = jd['nombre']
            perfil.save()
            datos = {'message': 'Success'}
        except perfiles.DoesNotExist:
            datos = {'message': 'Perfil no encontrado'}
        return JsonResponse(datos)

    def delete(self, request, perfil_id):
        try:
            perfil = perfiles.objects.get(id=perfil_id)
            perfil.delete()
            datos = {'message': 'Success'}
        except perfiles.DoesNotExist:
            datos = {'message': 'Perfil no encontrado'}
        return JsonResponse(datos)
    

class ClasificacionEdadView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, clasificacion_id=0):
        if clasificacion_id > 0:
            try:
                clasificacion = clasificacionEdad.objects.get(id=clasificacion_id)
                datos = {'message': 'Success', 'clasificacion': {'id': clasificacion.id, 'clasificacion': clasificacion.clasificacion}}
            except clasificacionEdad.DoesNotExist:
                datos = {'message': 'Clasificación no encontrada'}
        else:
            clasificaciones_data = list(clasificacionEdad.objects.values())
            if len(clasificaciones_data) > 0:
                datos = {'message': 'Success', 'clasificaciones': clasificaciones_data}
            else:
                datos = {'message': 'Clasificaciones no encontradas'}

        return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body)
        clasificacion = jd.get('clasificacion', '')

        try:
            clasificacionEdad.objects.create(clasificacion=clasificacion)
            datos = {'message': 'Success'}
        except Exception as e:
            datos = {'message': f'Error: {str(e)}'}

        return JsonResponse(datos)
    
class GenerosView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, genero_id=0):
        if genero_id > 0:
            try:
                genero = generos.objects.get(id=genero_id)
                datos = {'message': 'Success', 'genero': {'id': genero.id, 'nombre': genero.nombre}}
            except generos.DoesNotExist:
                datos = {'message': 'Género no encontrado'}
        else:
            generos_data = list(generos.objects.values())
            if len(generos_data) > 0:
                datos = {'message': 'Success', 'generos': generos_data}
            else:
                datos = {'message': 'Géneros no encontrados'}

        return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body)
        nombre = jd.get('nombre', '')

        try:
            generos.objects.create(nombre=nombre)
            datos = {'message': 'Success'}
        except Exception as e:
            datos = {'message': f'Error: {str(e)}'}

        return JsonResponse(datos)
    
class IdiomaView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, idioma_id=0):
        if idioma_id > 0:
            try:
                idioma_obj = idioma.objects.get(id=idioma_id)
                datos = {'message': 'Success', 'idioma': {'id': idioma_obj.id, 'nombre': idioma_obj.nombre}}
            except idioma.DoesNotExist:
                datos = {'message': 'Idioma no encontrado'}
        else:
            idiomas_data = list(idioma.objects.values())
            if len(idiomas_data) > 0:
                datos = {'message': 'Success', 'idiomas': idiomas_data}
            else:
                datos = {'message': 'Idiomas no encontrados'}

        return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body)
        nombre = jd.get('nombre', '')

        try:
            idioma.objects.create(nombre=nombre)
            datos = {'message': 'Success'}
        except Exception as e:
            datos = {'message': f'Error: {str(e)}'}

        return JsonResponse(datos)

class ContenidoView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, contenido_id=0):
        if contenido_id > 0:
            try:
                contenido_obj = contenido.objects.get(id=contenido_id)
                contenido_data = {
                    'id': contenido_obj.id,
                    'titulo': contenido_obj.titulo,
                    'descripcion': contenido_obj.descripcion,
                    'anioLanzamiento': contenido_obj.anioLanzamiento,
                    'clasificacionEdad': {
                        'id': contenido_obj.clasificacionEdad.id,
                        'clasificacion': contenido_obj.clasificacionEdad.clasificacion
                    },
                    'idiomaOriginal': {
                        'id': contenido_obj.idiomaOriginal.id,
                        'nombre': contenido_obj.idiomaOriginal.nombre
                    }
                }
                datos = {'message': 'Success', 'contenido': contenido_data}
            except contenido.DoesNotExist:
                datos = {'message': 'Contenido no encontrado'}
        else:
            contenido_data = list(contenido.objects.values())
            if len(contenido_data) > 0:
                datos = {'message': 'Success', 'contenidos': contenido_data}
            else:
                datos = {'message': 'Contenidos no encontrados'}

        return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body)
        clasificacion_id = jd.get('clasificacionEdad', None)
        idioma_id = jd.get('idiomaOriginal', None)

        try:
            clasificacion = clasificacionEdad.objects.get(id=clasificacion_id)
            idioma = idioma.objects.get(id=idioma_id)

            nuevo_contenido = contenido(
                titulo=jd['titulo'],
                descripcion=jd['descripcion'],
                anioLanzamiento=jd['anioLanzamiento'],
                clasificacionEdad=clasificacion,
                idiomaOriginal=idioma
            )
            nuevo_contenido.save()

            datos = {'message': 'Success'}
        except (clasificacionEdad.DoesNotExist, idioma.DoesNotExist) as e:
            datos = {'message': f'Error: {str(e)}'}

        return JsonResponse(datos)


class ContenidoGenerosView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, contenido_generos_id=0):
        if contenido_generos_id > 0:
            try:
                contenido_generos_obj = contenido_generos.objects.select_related('contenido', 'generos').get(id=contenido_generos_id)

                contenido_generos_data = {
                    'id': contenido_generos_obj.id,
                    'contenido': {
                        'id': contenido_generos_obj.contenido.id,
                        'titulo': contenido_generos_obj.contenido.titulo,
                        'descripcion': contenido_generos_obj.contenido.descripcion,
                        'anioLanzamiento': contenido_generos_obj.contenido.anioLanzamiento,
                        'clasificacionEdad': {
                            'id': contenido_generos_obj.contenido.clasificacionEdad.id,
                            'clasificacion': contenido_generos_obj.contenido.clasificacionEdad.clasificacion
                        },
                        'idiomaOriginal': {
                            'id': contenido_generos_obj.contenido.idiomaOriginal.id,
                            'nombre': contenido_generos_obj.contenido.idiomaOriginal.nombre
                        }
                    },
                    'generos': {
                        'id': contenido_generos_obj.generos.id,
                        'nombre': contenido_generos_obj.generos.nombre
                    }
                }
                datos = {'message': 'Success', 'contenido_generos': contenido_generos_data}
            except contenido_generos.DoesNotExist:
                datos = {'message': 'Contenido_Generos no encontrado'}
        else:
            contenido_generos_data = list(contenido_generos.objects.values())
            if len(contenido_generos_data) > 0:
                datos = {'message': 'Success', 'contenido_generos': contenido_generos_data}
            else:
                datos = {'message': 'Contenido_Generos no encontrados'}

        return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body)
        contenido_id = jd.get('contenido', None)
        generos_id = jd.get('generos', None)

        try:
            contenido_generos_obj = contenido_generos.objects.select_related('contenido', 'generos').get(
                contenido__id=contenido_id, generos__id=generos_id
            )

            datos = {'message': 'Success', 'contenido_generos': {'id': contenido_generos_obj.id}}
        except contenido_generos.DoesNotExist:
            datos = {'message': 'Contenido_Generos no encontrado'}

        return JsonResponse(datos)
    
class SubtitulosView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, subtitulos_id=0):
        if subtitulos_id > 0:
            try:
                subtitulos_obj = subtitulos.objects.select_related('idioma').get(id=subtitulos_id)

                subtitulos_data = {
                    'id': subtitulos_obj.id,
                    'idioma': {
                        'id': subtitulos_obj.idioma.id,
                        'nombre': subtitulos_obj.idioma.nombre
                    }
                }
                datos = {'message': 'Success', 'subtitulos': subtitulos_data}
            except subtitulos.DoesNotExist:
                datos = {'message': 'Subtitulos no encontrado'}
        else:
            subtitulos_data = list(subtitulos.objects.select_related('idioma').values())
            if len(subtitulos_data) > 0:
                datos = {'message': 'Success', 'subtitulos': subtitulos_data}
            else:
                datos = {'message': 'Subtitulos no encontrados'}

        return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body)
        idioma_id = jd.get('idioma', None)

        try:
            idioma_obj = idioma.objects.get(id=idioma_id)
            subtitulos_obj = subtitulos.objects.get(idioma=idioma_obj)

            datos = {'message': 'Success', 'subtitulos': {'id': subtitulos_obj.id}}
        except idioma.DoesNotExist:
            datos = {'message': 'Idioma no encontrado'}
        except subtitulos.DoesNotExist:
            datos = {'message': 'Subtitulos no encontrado'}

        return JsonResponse(datos)
    
class PeliculasView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, peliculas_id=0):
        if peliculas_id > 0:
            try:
                pelicula = peliculas.objects.get(id=peliculas_id)
                datos = {
                    'message': 'Success',
                    'pelicula': {
                        'id': pelicula.id,
                        'duracion': pelicula.duracion,
                        'contenido': {
                            'id': pelicula.contenido.id,
                            'titulo': pelicula.contenido.titulo,
                            'descripcion': pelicula.contenido.descripcion,
                            'anioLanzamiento': pelicula.contenido.anioLanzamiento,
                            'clasificacionEdad': {
                                'id': pelicula.contenido.clasificacionEdad.id,
                                'clasificacion': pelicula.contenido.clasificacionEdad.clasificacion,
                            },
                            'idiomaOriginal': {
                                'id': pelicula.contenido.idiomaOriginal.id,
                                'nombre': pelicula.contenido.idiomaOriginal.nombre,
                            },
                        },
                    },
                }
            except peliculas.DoesNotExist:
                datos = {'message': 'Pelicula no encontrada'}
        else:
            peliculas_data = list(peliculas.objects.values())
            datos = {'message': 'Success', 'peliculas': peliculas_data}

        return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body)
        duracion = jd.get('duracion', 0)
        contenido_id = jd.get('contenido_id', 0)

        try:
            contenido_obj = contenido.objects.get(id=contenido_id)
            pelicula = peliculas.objects.create(duracion=duracion, contenido=contenido_obj)
            datos = {'message': 'Success', 'pelicula_id': pelicula.id}
        except contenido.DoesNotExist:
            datos = {'message': 'Contenido no encontrado'}

        return JsonResponse(datos)

    def put(self, request, peliculas_id):
        jd = json.loads(request.body)
        duracion = jd.get('duracion', 0)
        contenido_id = jd.get('contenido_id', 0)

        try:
            pelicula = peliculas.objects.get(id=peliculas_id)
            contenido_obj = contenido.objects.get(id=contenido_id)
            pelicula.duracion = duracion
            pelicula.contenido = contenido_obj
            pelicula.save()
            datos = {'message': 'Success'}
        except peliculas.DoesNotExist:
            datos = {'message': 'Pelicula no encontrada'}
        except contenido.DoesNotExist:
            datos = {'message': 'Contenido no encontrado'}

        return JsonResponse(datos)

    def delete(self, request, peliculas_id):
        try:
            pelicula = peliculas.objects.get(id=peliculas_id)
            pelicula.delete()
            datos = {'message': 'Success'}
        except peliculas.DoesNotExist:
            datos = {'message': 'Pelicula no encontrada'}

        return JsonResponse(datos)
    
class SeriesView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if id > 0:
            try:
                serie = series.objects.select_related('contenido').get(id=id)
                serie_data = {
                    'id': serie.id,
                    'cant_temporadas': serie.cantTemporadas,
                    'contenido': {
                        'id': serie.contenido.id,
                        'titulo': serie.contenido.titulo,
                        'descripcion': serie.contenido.descripcion,
                        'anio_lanzamiento': serie.contenido.anioLanzamiento,
                        'clasificacion_edad': serie.contenido.clasificacionEdad.clasificacion,
                        'idioma_original': serie.contenido.idiomaOriginal.nombre
                    }
                }
                datos = {'message': 'Success', 'serie': serie_data}
            except series.DoesNotExist:
                datos = {'message': 'Serie no encontrada'}
        else:
            series_data = list(series.objects.select_related('contenido').values())
            if len(series_data) > 0:
                datos = {'message': 'Success', 'series': series_data}
            else:
                datos = {'message': 'Series no encontradas'}

        return JsonResponse(datos)

    def post(self, request):
        try:
            jd = json.loads(request.body)
            cant_temporadas = jd.get('cant_temporadas', 0)
            contenido_id = jd.get('contenido_id', 0)

            contenido_obj = contenido.objects.get(id=contenido_id)

            nueva_serie = series.objects.create(
                cantTemporadas=cant_temporadas,
                contenido=contenido_obj
            )

            serie_data = {
                'id': nueva_serie.id,
                'cant_temporadas': nueva_serie.cantTemporadas,
                'contenido': {
                    'id': nueva_serie.contenido.id,
                    'titulo': nueva_serie.contenido.titulo,
                    'descripcion': nueva_serie.contenido.descripcion,
                    'anio_lanzamiento': nueva_serie.contenido.anioLanzamiento,
                    'clasificacion_edad': nueva_serie.contenido.clasificacionEdad.clasificacion,
                    'idioma_original': nueva_serie.contenido.idiomaOriginal.nombre
                }
            }
            datos = {'message': 'Serie creada con éxito', 'serie': serie_data}

        except contenido.DoesNotExist:
            datos = {'message': 'Contenido no encontrado'}
        except Exception as e:
            datos = {'message': f'Error: {str(e)}'}

        return JsonResponse(datos)

    def put(self, request, id):
        try:
            jd = json.loads(request.body)
            cant_temporadas = jd.get('cant_temporadas', 0)
            contenido_id = jd.get('contenido_id', 0)

            serie = series.objects.get(id=id)
            contenido_obj = contenido.objects.get(id=contenido_id)

            serie.cantTemporadas = cant_temporadas
            serie.contenido = contenido_obj
            serie.save()

            serie_data = {
                'id': serie.id,
                'cant_temporadas': serie.cantTemporadas,
                'contenido': {
                    'id': serie.contenido.id,
                    'titulo': serie.contenido.titulo,
                    'descripcion': serie.contenido.descripcion,
                    'anio_lanzamiento': serie.contenido.anioLanzamiento,
                    'clasificacion_edad': serie.contenido.clasificacionEdad.clasificacion,
                    'idioma_original': serie.contenido.idiomaOriginal.nombre
                }
            }
            datos = {'message': 'Serie actualizada con éxito', 'serie': serie_data}

        except series.DoesNotExist:
            datos = {'message': 'Serie no encontrada'}
        except contenido.DoesNotExist:
            datos = {'message': 'Contenido no encontrado'}
        except Exception as e:
            datos = {'message': f'Error: {str(e)}'}

        return JsonResponse(datos)

    def delete(self, request, id):
        try:
            serie = series.objects.get(id=id)
            serie.delete()
            datos = {'message': 'Serie eliminada con éxito'}
        except series.DoesNotExist:
            datos = {'message': 'Serie no encontrada'}

        return JsonResponse(datos)