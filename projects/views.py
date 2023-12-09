from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from .models import *
import json

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
                datos = {'message':'Success', 'tipo':tipo}
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
            usuario_data = list(usuarios.objects.filter(id=id).values())
            if len(usuario_data) > 0:
                usuario = usuario_data[0]
                telefonosA = list(telefonos.objects.filter(usuarioId = usuario.get('id')).values())
                facturacionA = list(Facturacion.objects.filter(usuarioId = usuario.get('id')).values())
                perfilesA = list(perfiles.objects.filter(usuario_id = usuario.get('id')).values())
                usuario['telefonos']=telefonosA
                usuario['facturacion']=facturacionA
                usuario['perfiles']=perfilesA
                datos = {'message': 'Success', 'usuario': usuario}
            else:
                datos = {'message': 'Usuario no encontrado'}
            return JsonResponse(datos)
        else:
            usuarios_data = list(usuarios.objects.values())
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

    def get(self, request, id=0):
        if id > 0:
            telefonos_data = list(telefonos.objects.filter(id=id).values())
            if len(telefonos_data) > 0:
                telefono = telefonos_data[0]
                datos = {'message': 'Success', 'telefono': telefono}
            else:
                datos = {'message': 'Telefono no encontrado'}
            return JsonResponse(datos)
        else:
            telefonos_data = list(telefonos.objects.values())
            if len(telefonos_data) > 0:
                datos = {'message': 'Success', 'telefonos': telefonos_data}
            else:
                datos = {'message': 'Telefonos no encontrados'}
            return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body)
        telefonos.objects.create(usuarioId_id=jd['usuarioId'], telefono=jd['telefono'])
        datos = {'message':'Success'}
        return JsonResponse(datos)

    def put(self, request, id):
        jd = json.loads(request.body)
        telefonos_data = list(telefonos.objects.filter(id=id).values())

        if len(telefonos_data) > 0:
            usuario = usuarios.objects.get(id=jd['usuarioId_id'])
            telefono = telefonos.objects.get(id=id)
            telefono.telefono = jd['telefono']
            telefono.usuarioId = usuario
            telefono.save()
            datos = {'message': 'Success'}
        else:
            datos = {'message': 'Teléfono no encontrado'}

        return JsonResponse(datos)

    def delete(self, request, id):
        telefonos_data = list(telefonos.objects.filter(id=id).values())

        if len(telefonos_data) > 0:
            telefonos.objects.filter(id=id).delete()
            datos = {'message': 'Success'}
        else:
            datos = {'message': 'Teléfono no encontrado'}

        return JsonResponse(datos)

class PerfilesView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if id > 0:
            perfiles_data = list(perfiles.objects.filter(id=id).values())
            if len(perfiles_data) > 0:
                perfil = perfiles_data[0]
                datos = {'message': 'Success', 'usuario': perfil}
            else:
                datos = {'message': 'Usuario no encontrado'}
            return JsonResponse(datos)
        else:
            perfiles_data = list(perfiles.objects.values())
            if len(perfiles_data) > 0:
                datos = {'message': 'Success', 'usuarios': perfiles_data}
            else:
                datos = {'message': 'Usuarios no encontrados'}
            return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body)
        perfiles.objects.create(nombre=jd['nombre'], usuario_id=['usuario_id'])
        datos = {'message':'Success'}
        return JsonResponse(datos)

    def put(self, request, id):
        jd = json.loads(request.body)
        perfiles=list(perfiles.objects.filter(id=id).values())
        if len(perfiles) > 0:
            perfil = perfiles.objects.get(id=id)
            perfil.nombre = jd['nombre']
            perfil.usuario_id = jd['usuario_id']
            perfil.save()
            datos = {'message':'Success'}
        else:
            datos = {'message':'perfil no encontrado'}
        return JsonResponse(datos)

    def delete(self, request, id):
        perfiles=list(perfiles.objects.filter(id=id).values())
        if len(perfiles) > 0:
            perfiles.objects.filter(id=id).delete()
            datos = {'message':'Success'}
        else:
            datos = {'message':'perfil no encontrado'}
        return JsonResponse(datos)
    

class ClasificacionEdadView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if (id > 0):
            clasificaciones=list(clasificacionEdad.objects.filter(id=id).values())
            if len(clasificaciones) > 0:
                clasificacion = clasificaciones[0]
                datos = {'message':'Success', 'tipo':clasificaciones}
            else:
                datos = {'message':'tipo no encontrado'}
            return JsonResponse(datos)
        else:
            clasificaciones = list(tipoUsuario.objects.values())
            if len(clasificaciones) > 0:
                datos = {'message':'Success', 'tipos':clasificaciones}
            else:
                datos = {'message':'tipos no encontrados'}
            return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body)
        clasificacionEdad.objects.create(clasificacion=jd['clasificacion'])
        datos = {'message':'Success'}
        return JsonResponse(datos)
    
class GenerosView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if id > 0:
            try:
                genero = generos.objects.get(id=id)
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

    def get(self, request, id=0):
        if id > 0:
            try:
                idioma_obj = idioma.objects.get(id=id)
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

    def get(self, request, id=0):
        if id > 0:
            try:
                contenido_obj = contenido.objects.get(id=id)
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
            idiomaObj = idioma.objects.get(id=idioma_id)

            nuevo_contenido = contenido(
                titulo=jd['titulo'],
                descripcion=jd['descripcion'],
                anioLanzamiento=jd['anioLanzamiento'],
                clasificacionEdad=clasificacion,
                idiomaOriginal=idiomaObj
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

    def get(self, request, id=0):
        if id > 0:
            try:
                contenido_generos_obj = contenido_generos.objects.select_related('contenido', 'generos').get(id=id)
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

    def get(self, request, id=0):
        if id > 0:
            try:
                subtitulos_obj = subtitulos.objects.select_related('idioma').get(id=id)

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

    def get(self, request, id=0):
        if id > 0:
            try:
                pelicula = peliculas.objects.get(id=id)
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

    def put(self, request, id):
        jd = json.loads(request.body)
        duracion = jd.get('duracion', 0)
        contenido_id = jd.get('contenido_id', 0)

        try:
            pelicula = peliculas.objects.get(id=id)
            contenido_obj = contenido.objects.get(id=id)
            pelicula.duracion = duracion
            pelicula.contenido = contenido_obj
            pelicula.save()
            datos = {'message': 'Success'}
        except peliculas.DoesNotExist:
            datos = {'message': 'Pelicula no encontrada'}
        except contenido.DoesNotExist:
            datos = {'message': 'Contenido no encontrado'}

        return JsonResponse(datos)

    def delete(self, request, id):
        try:
            pelicula = peliculas.objects.get(id=id)
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
    
class ContenidoIdiomasView(View):
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if id > 0:
            try:
                contenidoIdiomas_obj = contenido_idiomas.objects.get(id=id)
                contenidoIdioma_data = {
                    
                    'idioma': {
                        'id': contenidoIdiomas_obj.idioma.id,
                        'nombre': contenidoIdiomas_obj.idioma.nombre
                    },
                    'contenido': {
                        'id': contenidoIdiomas_obj.contenido.id,
                        'titulo': contenidoIdiomas_obj.contenido.titulo,
                        'descripcion': contenidoIdiomas_obj.contenido.descripcion,
                        'anioLanzamiento': contenidoIdiomas_obj.contenido.anioLanzamiento,
                        'clasificacionEdad': {
                            'id': contenidoIdiomas_obj.contenido.clasificacionEdad.id,
                            'clasificacion': contenidoIdiomas_obj.contenido.clasificacionEdad.clasificacion
                        },
                        'idiomaOriginal': {
                            'id': contenidoIdiomas_obj.contenido.idiomaOriginal.id,
                            'nombre': contenidoIdiomas_obj.contenido.idiomaOriginal.nombre
                        }
                    }
                }
                datos = {'message': 'Success', 'contenido': contenidoIdioma_data}
            except contenido_subtitulos.DoesNotExist:
                datos = {'message': 'Contenido no encontrado'}
        else:
            contenidoIdioma_data = list(contenido_idiomas.objects.values())
            if len(contenidoIdioma_data) > 0:
                datos = {'message': 'Success', 'contenidos': contenidoIdioma_data}
            else:
                datos = {'message': 'Contenidos no encontrados'}

        return JsonResponse(datos)
        
        
    def post(self, request):
        jd = json.loads(request.body)
        contenido_id = jd.get('contenido', None)
        idioma_id = jd.get('idioma', None)

        try:
            contenidoObj = contenido.objects.get(id=contenido_id)
            idiomaObj = idioma.objects.get(id=idioma_id)
            cont_idioma = contenido_idiomas(
                idioma = idiomaObj,
                contenido = contenidoObj
            )
            cont_idioma.save()
            datos = {'message': 'Success'}
        except (contenido.DoesNotExist, idioma.DoesNotExist) as e:
            datos = {'message': f'Error: {str(e)}'}

        return JsonResponse(datos)
    
class ContenidoSubtitulosView(View):
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if id > 0:
            try:
                contenidoSubtitulos_obj = contenido_subtitulos.objects.get(id=id)
                contenidoSubtitulos_data = {
                    
                    'idioma': {
                        'id': contenidoSubtitulos_obj.idioma.id,
                        'nombre': contenidoSubtitulos_obj.idioma.nombre
                    },
                    'contenido': {
                        'id': contenidoSubtitulos_obj.contenido.id,
                        'titulo': contenidoSubtitulos_obj.contenido.titulo,
                        'descripcion': contenidoSubtitulos_obj.contenido.descripcion,
                        'anioLanzamiento': contenidoSubtitulos_obj.contenido.anioLanzamiento,
                        'clasificacionEdad': {
                            'id': contenidoSubtitulos_obj.contenido.clasificacionEdad.id,
                            'clasificacion': contenidoSubtitulos_obj.contenido.clasificacionEdad.clasificacion
                        },
                        'idiomaOriginal': {
                            'id': contenidoSubtitulos_obj.contenido.idiomaOriginal.id,
                            'nombre': contenidoSubtitulos_obj.contenido.idiomaOriginal.nombre
                        }
                    }
                }
                datos = {'message': 'Success', 'contenido': contenidoSubtitulos_data}
            except contenido_subtitulos.DoesNotExist:
                datos = {'message': 'Contenido no encontrado'}
        else:
            contenidoSubtitulos_data = list(contenido_subtitulos.objects.values())
            if len(contenidoSubtitulos_data) > 0:
                datos = {'message': 'Success', 'contenidos': contenidoSubtitulos_data}
            else:
                datos = {'message': 'Contenidos no encontrados'}

        return JsonResponse(datos)
        
        
    def post(self, request):
        jd = json.loads(request.body)
        contenido_id = jd.get('contenido', None)
        idioma_id = jd.get('idioma', None)

        try:
            contenidoObj = contenido.objects.get(id=contenido_id)
            idiomaObj = idioma.objects.get(id=idioma_id)
            cont_sub = contenido_subtitulos(
                idioma = idiomaObj,
                contenido = contenidoObj
            )
            cont_sub.save()
            datos = {'message': 'Success'}
        except (contenido.DoesNotExist, idioma.DoesNotExist) as e:
            datos = {'message': f'Error: {str(e)}'}

        return JsonResponse(datos)
    
    
class TemporadasView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if id > 0:
            try:
                temporadas_obj = temporadas.objects.get(id=id)
                temporadas_data = {
                    'id': temporadas_obj.id,
                    'nombre': temporadas_obj.nombre,
                    'serie': {
                        'id': temporadas_obj.serie.id,
                        'contenido': {
                        'id': temporadas_obj.serie.contenido.id,
                        'titulo': temporadas_obj.serie.contenido.titulo,
                        'descripcion': temporadas_obj.serie.contenido.descripcion,
                        'anioLanzamiento': temporadas_obj.serie.contenido.anioLanzamiento,
                        'clasificacionEdad': {
                            'id': temporadas_obj.serie.contenido.clasificacionEdad.id,
                            'clasificacion': temporadas_obj.serie.contenido.clasificacionEdad.clasificacion
                        },
                        'idiomaOriginal': {
                            'id': temporadas_obj.serie.contenido.idiomaOriginal.id,
                            'nombre': temporadas_obj.serie.contenido.idiomaOriginal.nombre
                        }
                    },
                        'cantTemporadas': temporadas_obj.serie.cantTemporadas
                    },
                    'anoDeEstreno': temporadas_obj.anoDeEstreno,
                    'cantEpisodios': temporadas_obj.cantEpisodios
                   
                }
                datos = {'message': 'Success', 'temporada': temporadas_data}
            except temporadas.DoesNotExist:
                datos = {'message': 'temporada no encontrado'}
        else:
            temporadas_data = list(temporadas.objects.values())
            if len(temporadas_data) > 0:
                datos = {'message': 'Success', 'temporadas': temporadas_data}
            else:
                datos = {'message': 'Temporadas no encontrados'}

        return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body)
        serie_id = jd.get('serie', None)
        

        try:
            serie = series.objects.get(id=serie_id)
           

            nuevo_temporada = temporadas(
                nombre =jd['nombre'],
                serie = serie,
                anoDeEstreno =jd['anoDeEstreno'],
                cantEpisodios = jd['cantEpisodios']
            )
            nuevo_temporada.save()

            datos = {'message': 'Success'}
        except (serie.DoesNotExist) as e:
            datos = {'message': f'Error: {str(e)}'}

        return JsonResponse(datos)
    
    def put(self, request, id):
        jd = json.loads(request.body)
        serie_id = jd.get('serie', None)
        try:
            serie = series.objects.get(id=serie_id)
            temporada = temporadas.objects.get(id=id)
            temporada.nombre = jd['nombre']
            temporada.anoDeEstreno = jd['anoDeEstreno']
            temporada.cantEpisodios = jd['cantEpisodios']
            temporada.serie = serie
            temporada.save()
            datos = {'message': 'Success'}
        except temporadas.DoesNotExist:
            datos = {'message': 'Temporada no encontrada'}
        except series.DoesNotExist:
            datos = {'message': 'Serie no encontrada'}

        return JsonResponse(datos)

    def delete(self, request, id):
        try:
            temporada = temporadas.objects.get(id=id)
            temporada.delete()
            datos = {'message': 'Success'}
        except temporadas.DoesNotExist:
            datos = {'message': 'Temporada no encontrada'}

        return JsonResponse(datos)   

class EpisodiosView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if id > 0:
            try:
                episodio_obj = episodios.objects.get(id=id)
                episodio_data = {
                    'id': episodio_obj.id,
                    'temporada': {
                        'id': episodio_obj.temporada.id,
                        'nombre': episodio_obj.temporada.nombre,
                        'serie': {
                            'id': episodio_obj.temporada.serie.id,
                            'contenido': {
                            'id': episodio_obj.temporada.serie.contenido.id,
                            'titulo': episodio_obj.temporada.serie.contenido.titulo,
                            'descripcion': episodio_obj.temporada.serie.contenido.descripcion,
                            'anioLanzamiento': episodio_obj.temporada.serie.contenido.anioLanzamiento,
                            'clasificacionEdad': {
                                'id': episodio_obj.temporada.serie.contenido.clasificacionEdad.id,
                                'clasificacion': episodio_obj.temporada.serie.contenido.clasificacionEdad.clasificacion
                            },
                            'idiomaOriginal': {
                                'id': episodio_obj.temporada.serie.contenido.idiomaOriginal.id,
                                'nombre': episodio_obj.temporada.serie.contenido.idiomaOriginal.nombre
                            }
                    },
                            'cantTemporadas': episodio_obj.temporada.serie.cantTemporadas
                        },
                        'anoDeEstreno': episodio_obj.temporada.anoDeEstreno,
                        'cantEpisodios': episodio_obj.temporada.cantEpisodios
                    },
                    'numeroEpisodio': episodio_obj.numeroEpisodio,
                    'tituloEpisodio': episodio_obj.tituloEpisodio,
                    'duracion': episodio_obj.duracion,
                    'anoLanzamiento': episodio_obj.anoLanzamiento,
                    'descripcion': episodio_obj.descripcion
                }
                datos = {'message': 'Success', 'episodio': episodio_data}
            except episodios.DoesNotExist:
                datos = {'message': 'Episodio no encontrado'}
        else:
            episodios_data = list(episodios.objects.values())
            if len(episodios_data) > 0:
                datos = {'message': 'Success', 'episodios': episodios_data}
            else:
                datos = {'message': 'Episodios no encontrados'}

        return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body)
        temporada_id = jd.get('temporada', None)

        try:
            temporada = temporadas.objects.get(id=temporada_id)

            nuevo_episodio = episodios(
                temporada=temporada,
                numeroEpisodio=jd['numeroEpisodio'],
                tituloEpisodio=jd['tituloEpisodio'],
                duracion=jd['duracion'],
                anoLanzamiento=jd['anoLanzamiento'],
                descripcion=jd.get('descripcion', None)
            )
            nuevo_episodio.save()

            datos = {'message': 'Success'}
        except temporadas.DoesNotExist as e:
            datos = {'message': f'Error: {str(e)}'}

        return JsonResponse(datos)

    def put(self, request, id):
        jd = json.loads(request.body)
        try:
            episodio = episodios.objects.get(id=id)
            episodio.temporada = temporadas.objects.get(id=jd['temporada'])
            episodio.numeroEpisodio = jd['numeroEpisodio']
            episodio.tituloEpisodio = jd['tituloEpisodio']
            episodio.duracion = jd['duracion']
            episodio.anoLanzamiento = jd['anoLanzamiento']
            episodio.descripcion = jd.get('descripcion', None)
            episodio.save()
            datos = {'message': 'Success'}
        except episodios.DoesNotExist:
            datos = {'message': 'Episodio no encontrado'}
        except temporadas.DoesNotExist:
            datos = {'message': 'Temporada no encontrada'}

        return JsonResponse(datos)

    def delete(self, request, id):
        try:
            episodio = episodios.objects.get(id=id)
            episodio.delete()
            datos = {'message': 'Success'}
        except episodios.DoesNotExist:
            datos = {'message': 'Episodio no encontrado'}

        return JsonResponse(datos)
    
class ValoracionesContenidoView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if id > 0:
            try:
                valoracion_obj = ValoracionesContenido.objects.get(id=id)
                valoracion_data = {
                    'id': valoracion_obj.id,
                    'usuarioId': {
                        'id': valoracion_obj.usuarioId.id,
                        'correo': valoracion_obj.usuarioId.correo
                    },
                    'contenido': {
                        'id': valoracion_obj.contenido.id,
                        'titulo': valoracion_obj.contenido.titulo,
                        'descripcion': valoracion_obj.contenido.descripcion,
                        'anioLanzamiento': valoracion_obj.contenido.anioLanzamiento,
                        'clasificacionEdad': {
                            'id': valoracion_obj.contenido.clasificacionEdad.id,
                            'clasificacion': valoracion_obj.contenido.clasificacionEdad.clasificacion
                        },
                        'idiomaOriginal': {
                            'id': valoracion_obj.contenido.idiomaOriginal.id,
                            'nombre': valoracion_obj.contenido.idiomaOriginal.nombre
                         }
                    },
                    'valoracion': valoracion_obj.valoracion,
                    'comentario': valoracion_obj.comentario,
                    'fechaValoracion': valoracion_obj.fechaValoracion
                }
                datos = {'message': 'Success', 'valoracion': valoracion_data}
            except ValoracionesContenido.DoesNotExist:
                datos = {'message': 'Valoración no encontrada'}
        else:
            valoraciones_data = list(ValoracionesContenido.objects.values())
            if len(valoraciones_data) > 0:
                datos = {'message': 'Success', 'valoraciones': valoraciones_data}
            else:
                datos = {'message': 'Valoraciones no encontradas'}

        return JsonResponse(datos)
    
    def post(self, request):
        jd = json.loads(request.body)
        usuario_id = jd.get('usuarioId', None)
        contenido_id = jd.get('contenido', None)

        try:
            usuario = usuarios.objects.get(id=usuario_id)
            contenido_obj = contenido.objects.get(id=contenido_id)

            nueva_valoracion = ValoracionesContenido(
                usuarioId=usuario,
                contenido=contenido_obj,
                valoracion=jd['valoracion'],
                comentario=jd['comentario']
            )
            nueva_valoracion.save()

            datos = {'message': 'Success'}
        except usuarios.DoesNotExist or contenido.DoesNotExist as e:
            datos = {'message': f'Error: {str(e)}'}

        return JsonResponse(datos)

    def put(self, request, id):
        jd = json.loads(request.body)
        try:
            valoracion = ValoracionesContenido.objects.get(id=id)
            valoracion.usuarioId = usuarios.objects.get(id=jd['usuarioId'])
            valoracion.contenido = contenido.objects.get(id=jd['contenido'])
            valoracion.valoracion = jd['valoracion']
            valoracion.comentario = jd['comentario']
            valoracion.save()
            datos = {'message': 'Success'}
        except ValoracionesContenido.DoesNotExist:
            datos = {'message': 'Valoración no encontrada'}
        except usuarios.DoesNotExist or contenido.DoesNotExist as e:
            datos = {'message': f'Error: {str(e)}'}

        return JsonResponse(datos)

    def delete(self, request, id):
        try:
            valoracion = ValoracionesContenido.objects.get(id=id)
            valoracion.delete()
            datos = {'message': 'Success'}
        except ValoracionesContenido.DoesNotExist:
            datos = {'message': 'Valoración no encontrada'}

        return JsonResponse(datos)

class PlaylistsView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if id > 0:
            try:
                playlists_obj = Playlists.objects.get(id=id)
                playlists_data = {
                    'id': playlists_obj.id,
                    'usuarioId': {
                        'id': playlists_obj.usuarioId.id,
                        'correo': playlists_obj.usuarioId.correo
                    },
                    'contenido': {
                        'id': playlists_obj.contenido.id,
                        'titulo': playlists_obj.contenido.titulo,
                        'descripcion': playlists_obj.contenido.descripcion,
                        'anioLanzamiento': playlists_obj.contenido.anioLanzamiento,
                        'clasificacionEdad': {
                            'id': playlists_obj.contenido.clasificacionEdad.id,
                            'clasificacion': playlists_obj.contenido.clasificacionEdad.clasificacion
                        },
                        'idiomaOriginal': {
                            'id': playlists_obj.contenido.idiomaOriginal.id,
                            'nombre': playlists_obj.contenido.idiomaOriginal.nombre
                         }
                    },
                    'valoracion': playlists_obj.valoracion,
                    'comentario': playlists_obj.comentario,
                    'fechaValoracion': playlists_obj.fechaValoracion
                }
                datos = {'message': 'Success', 'valoracion': playlists_data}
            except Playlists.DoesNotExist:
                datos = {'message': 'Valoración no encontrada'}
        else:
            playlists_data = list(Playlists.objects.values())
            if len(playlists_data) > 0:
                datos = {'message': 'Success', 'valoraciones': playlists_data}
            else:
                datos = {'message': 'Valoraciones no encontradas'}

        return JsonResponse(datos)
    
    def post(self, request):
        jd = json.loads(request.body)
        usuario_id = jd.get('usuarioId', None)
        contenido_id = jd.get('contenido', None)

        try:
            usuario = usuarios.objects.get(id=usuario_id)
            contenido_obj = contenido.objects.get(id=contenido_id)

            nueva_playlist = Playlists(
                usuarioId=usuario,
                contenido=contenido_obj,
                nombreLista=jd['nombreLista']
            )
            nueva_playlist.save()

            datos = {'message': 'Success'}
        except usuarios.DoesNotExist or contenido.DoesNotExist as e:
            datos = {'message': f'Error: {str(e)}'}

        return JsonResponse(datos)

    def put(self, request, id):
        jd = json.loads(request.body)
        try:
            playlist = Playlists.objects.get(id=id)
            playlist.usuarioId = usuarios.objects.get(id=jd['usuarioId'])
            playlist.contenido = contenido.objects.get(id=jd['contenido'])
            playlist.nombreLista = jd['nombreLista']
            playlist.save()
            datos = {'message': 'Success'}
        except Playlists.DoesNotExist:
            datos = {'message': 'Valoración no encontrada'}
        except usuarios.DoesNotExist or contenido.DoesNotExist as e:
            datos = {'message': f'Error: {str(e)}'}

        return JsonResponse(datos)

    def delete(self, request, id):
        try:
            playlist = Playlists.objects.get(id=id)
            playlist.delete()
            datos = {'message': 'Success'}
        except ValoracionesContenido.DoesNotExist:
            datos = {'message': 'Valoración no encontrada'}

        return JsonResponse(datos)

class PlanesView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if id > 0:
            try:
                plan_obj = Planes.objects.get(id=id)
                plan_data = {
                    'id': plan_obj.id,
                    'nombre': plan_obj.nombre,
                    'precioMensual': str(plan_obj.precioMensual),
                    'calidadVideo': plan_obj.calidadVideo,
                    'resolucion': plan_obj.resolucion
                }
                datos = {'message': 'Success', 'plan': plan_data}
            except Planes.DoesNotExist:
                datos = {'message': 'Plan no encontrado'}
        else:
            planes_data = list(Planes.objects.values())
            if len(planes_data) > 0:
                datos = {'message': 'Success', 'planes': planes_data}
            else:
                datos = {'message': 'Planes no encontrados'}

        return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body)
        nuevo_plan = Planes(
            nombre=jd['nombre'],
            precioMensual=jd['precioMensual'],
            calidadVideo=jd['calidadVideo'],
            resolucion=jd['resolucion']
        )
        nuevo_plan.save()

        datos = {'message': 'Success'}
        return JsonResponse(datos)

    def put(self, request, id):
        jd = json.loads(request.body)
        try:
            plan = Planes.objects.get(id=id)
            plan.nombre = jd['nombre']
            plan.precioMensual = jd['precioMensual']
            plan.calidadVideo = jd['calidadVideo']
            plan.resolucion = jd['resolucion']
            plan.save()
            datos = {'message': 'Success'}
        except Planes.DoesNotExist:
            datos = {'message': 'Plan no encontrado'}

        return JsonResponse(datos)

    def delete(self, request, id):
        try:
            plan = Planes.objects.get(id=id)
            plan.delete()
            datos = {'message': 'Success'}
        except Planes.DoesNotExist:
            datos = {'message': 'Plan no encontrado'}

        return JsonResponse(datos)
    
class FacturacionView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if id > 0:
            try:
                factura_obj = Facturacion.objects.get(id=id)
                factura_data = {
                    'id': factura_obj.id,
                    'usuarioId': {
                        'id': factura_obj.usuarioId.id,
                        'correo': factura_obj.usuarioId.correo
                    },
                    'numeroDeTarjeta': factura_obj.numeroDeTarjeta,
                    'fechaDeVencimiento': str(factura_obj.fechaDeVencimiento),
                    'cvv': factura_obj.cvv,
                    'nombreEnLaTarjeta': factura_obj.nombreEnLaTarjeta
                }
                datos = {'message': 'Success', 'facturacion': factura_data}
            except Facturacion.DoesNotExist:
                datos = {'message': 'Facturación no encontrada'}
        else:
            facturas_data = list(Facturacion.objects.values())
            if len(facturas_data) > 0:
                datos = {'message': 'Success', 'facturaciones': facturas_data}
            else:
                datos = {'message': 'Facturaciones no encontradas'}

        return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body)
        usuario_id = jd.get('usuarioId', None)

        try:
            usuario = usuarios.objects.get(id=usuario_id)

            nueva_factura = Facturacion(
                usuarioId=usuario,
                numeroDeTarjeta=jd['numeroDeTarjeta'],
                fechaDeVencimiento=jd['fechaDeVencimiento'],
                cvv=jd['cvv'],
                nombreEnLaTarjeta=jd['nombreEnLaTarjeta']
            )
            nueva_factura.save()

            datos = {'message': 'Success'}
        except usuarios.DoesNotExist as e:
            datos = {'message': f'Error: {str(e)}'}

        return JsonResponse(datos)

    def put(self, request, id):
        jd = json.loads(request.body)
        try:
            factura = Facturacion.objects.get(id=id)
            factura.usuarioId = usuarios.objects.get(id=jd['usuarioId'])
            factura.numeroDeTarjeta = jd['numeroDeTarjeta']
            factura.fechaDeVencimiento = jd['fechaDeVencimiento']
            factura.cvv = jd['cvv']
            factura.nombreEnLaTarjeta = jd['nombreEnLaTarjeta']
            factura.save()
            datos = {'message': 'Success'}
        except Facturacion.DoesNotExist:
            datos = {'message': 'Facturación no encontrada'}
        except usuarios.DoesNotExist as e:
            datos = {'message': f'Error: {str(e)}'}

        return JsonResponse(datos)

    def delete(self, request, id):
        try:
            factura = Facturacion.objects.get(id=id)
            factura.delete()
            datos = {'message': 'Success'}
        except Facturacion.DoesNotExist:
            datos = {'message': 'Facturación no encontrada'}

        return JsonResponse(datos)
    
class PaisView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if id > 0:
            try:
                pais_obj = pais.objects.get(id=id)
                pais_data = {
                    'id': pais_obj.id,
                    'nombre': pais_obj.nombre
                }
                datos = {'message': 'Success', 'pais': pais_data}
            except pais.DoesNotExist:
                datos = {'message': 'País no encontrado'}
        else:
            paises_data = list(pais.objects.values())
            if len(paises_data) > 0:
                datos = {'message': 'Success', 'paises': paises_data}
            else:
                datos = {'message': 'Países no encontrados'}

        return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body)

        nuevo_pais = pais(nombre=jd['nombre'])
        nuevo_pais.save()

        datos = {'message': 'Success'}
        return JsonResponse(datos)

    def put(self, request, id):
        jd = json.loads(request.body)
        try:
            paisobj = pais.objects.get(id=id)
            paisobj.nombre = jd['nombre']
            paisobj.save()
            datos = {'message': 'Success'}
        except pais.DoesNotExist:
            datos = {'message': 'País no encontrado'}

        return JsonResponse(datos)

    def delete(self, request, id):
        try:
            paisobj = pais.objects.get(id=id)
            paisobj.delete()
            datos = {'message': 'Success'}
        except pais.DoesNotExist:
            datos = {'message': 'País no encontrado'}

        return JsonResponse(datos)

class RolView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if id > 0:
            try:
                rol_obj = rol.objects.get(id=id)
                rol_data = {
                    'id': rol_obj.id,
                    'nombre': rol_obj.nombre
                }
                datos = {'message': 'Success', 'rol': rol_data}
            except rol.DoesNotExist:
                datos = {'message': 'Rol no encontrado'}
        else:
            roles_data = list(rol.objects.values())
            if len(roles_data) > 0:
                datos = {'message': 'Success', 'roles': roles_data}
            else:
                datos = {'message': 'Roles no encontrados'}

        return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body)

        nuevo_rol = rol(nombre=jd['nombre'])
        nuevo_rol.save()

        datos = {'message': 'Success'}
        return JsonResponse(datos)

    def put(self, request, id):
        jd = json.loads(request.body)
        try:
            rolObj =rol.objects.get(id=id)
            rolObj.nombre = jd['nombre']
            rolObj.save()
            datos = {'message': 'Success'}
        except rol.DoesNotExist:
            datos = {'message': 'Rol no encontrado'}

        return JsonResponse(datos)

    def delete(self, request, id):
        try:
            rolObj = rol.objects.get(id=id)
            rolObj.delete()
            datos = {'message': 'Success'}
        except rol.DoesNotExist:
            datos = {'message': 'Rol no encontrado'}

        return JsonResponse(datos)
    
class PersonasView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if id > 0:
            try:
                persona_obj = personas.objects.get(id=id)
                persona_data = {
                    'id': persona_obj.id,
                    'nombre': persona_obj.nombre,
                    'apellido': persona_obj.apellido,
                    'fechaDeNacimiento': str(persona_obj.fechaDeNacimiento),
                    'pais': {
                        'id': persona_obj.pais.id,
                        'nombre': persona_obj.pais.nombre
                    },
                    'rol': {
                        'id': persona_obj.rol.id,
                        'nombre': persona_obj.rol.nombre
                    }
                }
                datos = {'message': 'Success', 'persona': persona_data}
            except personas.DoesNotExist:
                datos = {'message': 'Persona no encontrada'}
        else:
            personas_data = list(personas.objects.values())
            if len(personas_data) > 0:
                datos = {'message': 'Success', 'personas': personas_data}
            else:
                datos = {'message': 'Personas no encontradas'}

        return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body)
        pais_id = jd.get('pais', None)
        rol_id = jd.get('rol', None)

        try:
            paisObj = pais.objects.get(id=pais_id)
            rolObj = rol.objects.get(id=rol_id)

            nueva_persona = personas(
                nombre=jd['nombre'],
                apellido=jd['apellido'],
                fechaDeNacimiento=jd['fechaDeNacimiento'],
                pais=paisObj,
                rol=rolObj
            )
            nueva_persona.save()

            datos = {'message': 'Success'}
        except (pais.DoesNotExist, rol.DoesNotExist) as e:
            datos = {'message': f'Error: {str(e)}'}

        return JsonResponse(datos)

    def put(self, request, id):
        jd = json.loads(request.body)
        try:
            persona = personas.objects.get(id=id)
            persona.nombre = jd['nombre']
            persona.apellido = jd['apellido']
            persona.fechaDeNacimiento = jd['fechaDeNacimiento']
            persona.pais = pais.objects.get(id=jd['pais'])
            persona.rol = rol.objects.get(id=jd['rol'])
            persona.save()
            datos = {'message': 'Success'}
        except personas.DoesNotExist:
            datos = {'message': 'Persona no encontrada'}
        except (pais.DoesNotExist, rol.DoesNotExist) as e:
            datos = {'message': f'Error: {str(e)}'}

        return JsonResponse(datos)

    def delete(self, request, id):
        try:
            persona = personas.objects.get(id=id)
            persona.delete()
            datos = {'message': 'Success'}
        except personas.DoesNotExist:
            datos = {'message': 'Persona no encontrada'}

        return JsonResponse(datos)
    
class EstudiosProductorasView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if id > 0:
            try:
                estudio_obj = EstudiosProductoras.objects.get(id=id)
                estudio_data = {
                    'id': estudio_obj.id,
                    'nombre': estudio_obj.nombre,
                    'pais': {
                        'id': estudio_obj.pais.id,
                        'nombre': estudio_obj.pais.nombre
                    },
                    'anoDeFundacion': estudio_obj.anoDeFundacion
                }
                datos = {'message': 'Success', 'estudio': estudio_data}
            except EstudiosProductoras.DoesNotExist:
                datos = {'message': 'Estudio no encontrado'}
        else:
            estudios_data = list(EstudiosProductoras.objects.values())
            if len(estudios_data) > 0:
                datos = {'message': 'Success', 'estudios': estudios_data}
            else:
                datos = {'message': 'Estudios no encontrados'}

        return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body)
        pais_id = jd.get('pais', None)

        try:
            paisObj = pais.objects.get(id=pais_id)

            nuevo_estudio = EstudiosProductoras(
                nombre=jd['nombre'],
                pais=paisObj,
                anoDeFundacion=jd['anoDeFundacion']
            )
            nuevo_estudio.save()

            datos = {'message': 'Success'}
        except pais.DoesNotExist as e:
            datos = {'message': f'Error: {str(e)}'}

        return JsonResponse(datos)

    def put(self, request, id):
        jd = json.loads(request.body)
        try:
            estudio = EstudiosProductoras.objects.get(id=id)
            estudio.nombre = jd['nombre']
            estudio.pais = pais.objects.get(id=jd['pais'])
            estudio.anoDeFundacion = jd['anoDeFundacion']
            estudio.save()
            datos = {'message': 'Success'}
        except EstudiosProductoras.DoesNotExist:
            datos = {'message': 'Estudio no encontrado'}
        except pais.DoesNotExist as e:
            datos = {'message': f'Error: {str(e)}'}

        return JsonResponse(datos)

    def delete(self, request, id):
        try:
            estudio = EstudiosProductoras.objects.get(id=id)
            estudio.delete()
            datos = {'message': 'Success'}
        except EstudiosProductoras.DoesNotExist:
            datos = {'message': 'Estudio no encontrado'}

        return JsonResponse(datos)
    
class ListaReproduccionContenidoView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if id > 0:
            try:
                lista_obj = ListaReproduccionContenido.objects.get(id=id)
                lista_data = {
                    'id': lista_obj.id,
                    'usuarioId': {
                        'id': lista_obj.usuarioId.id,
                        'correo': lista_obj.usuarioId.correo
                    },
                    'nombreLista': lista_obj.nombreLista
                }
                datos = {'message': 'Success', 'lista': lista_data}
            except ListaReproduccionContenido.DoesNotExist:
                datos = {'message': 'Lista no encontrada'}
        else:
            listas_data = list(ListaReproduccionContenido.objects.values())
            if len(listas_data) > 0:
                datos = {'message': 'Success', 'listas': listas_data}
            else:
                datos = {'message': 'Listas no encontradas'}

        return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body)
        usuario_id = jd.get('usuarioId', None)

        try:
            usuario = usuarios.objects.get(id=usuario_id)

            nueva_lista = ListaReproduccionContenido(
                usuarioId=usuario,
                nombreLista=jd['nombreLista']
            )
            nueva_lista.save()

            datos = {'message': 'Success'}
        except usuarios.DoesNotExist as e:
            datos = {'message': f'Error: {str(e)}'}

        return JsonResponse(datos)

    def put(self, request, id):
        jd = json.loads(request.body)
        try:
            lista = ListaReproduccionContenido.objects.get(id=id)
            lista.usuarioId = usuarios.objects.get(id=jd['usuarioId'])
            lista.nombreLista = jd['nombreLista']
            lista.save()
            datos = {'message': 'Success'}
        except ListaReproduccionContenido.DoesNotExist:
            datos = {'message': 'Lista no encontrada'}
        except usuarios.DoesNotExist as e:
            datos = {'message': f'Error: {str(e)}'}

        return JsonResponse(datos)

    def delete(self, request, id):
        try:
            lista = ListaReproduccionContenido.objects.get(id=id)
            lista.delete()
            datos = {'message': 'Success'}
        except ListaReproduccionContenido.DoesNotExist:
            datos = {'message': 'Lista no encontrada'}

        return JsonResponse(datos)

class VisualizacionesView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if id > 0:
            try:
                visualizacion_obj = Visualizaciones.objects.get(id=id)
                visualizacion_data = {
                    'id': visualizacion_obj.id,
                    'usuarioId': {
                        'id': visualizacion_obj.usuarioId.id,
                        'correo': visualizacion_obj.usuarioId.correo
                    },
                    'contenido': {
                        'id': visualizacion_obj.contenido.id,
                        'titulo': visualizacion_obj.contenido.titulo,
                        'descripcion': visualizacion_obj.contenido.descripcion,
                        'anioLanzamiento': visualizacion_obj.contenido.anioLanzamiento,
                        'clasificacionEdad': {
                            'id': visualizacion_obj.contenido.clasificacionEdad.id,
                            'clasificacion': visualizacion_obj.contenido.clasificacionEdad.clasificacion
                        },
                        'idiomaOriginal': {
                            'id': visualizacion_obj.contenido.idiomaOriginal.id,
                            'nombre': visualizacion_obj.contenido.idiomaOriginal.nombre
                         }
                    },
                    'fechaVisualizacion': visualizacion_obj.fechaVisualizacion
                }
                datos = {'message': 'Success', 'visualizacion': visualizacion_data}
            except Visualizaciones.DoesNotExist:
                datos = {'message': 'Visualización no encontrada'}
        else:
            visualizaciones_data = list(Visualizaciones.objects.values())
            if len(visualizaciones_data) > 0:
                datos = {'message': 'Success', 'visualizaciones': visualizaciones_data}
            else:
                datos = {'message': 'Visualizaciones no encontradas'}

        return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body)
        usuario_id = jd.get('usuarioId', None)
        contenido_id = jd.get('contenidoId', None)

        try:
            usuario = usuarios.objects.get(id=usuario_id)
            contenidoObj = contenido.objects.get(id=contenido_id)

            nueva_visualizacion = Visualizaciones(
                usuarioId=usuario,
                contenido=contenidoObj
                #nose si mandarlo ya que es un dato tipo fecha que se genera solo
            )
            nueva_visualizacion.save()

            datos = {'message': 'Success'}
        except (usuarios.DoesNotExist, contenido.DoesNotExist) as e:
            datos = {'message': f'Error: {str(e)}'}

        return JsonResponse(datos)

    def put(self, request, id):
        jd = json.loads(request.body)
        try:
            visualizacion = Visualizaciones.objects.get(id=id)
            visualizacion.usuarioId = usuarios.objects.get(id=jd['usuarioId'])
            visualizacion.contenido = contenido.objects.get(id=jd['contenidoId'])
            visualizacion.save()
            datos = {'message': 'Success'}
        except Visualizaciones.DoesNotExist:
            datos = {'message': 'Visualización no encontrada'}
        except (usuarios.DoesNotExist, contenido.DoesNotExist) as e:
            datos = {'message': f'Error: {str(e)}'}

        return JsonResponse(datos)

    def delete(self, request, id):
        try:
            visualizacion = Visualizaciones.objects.get(id=id)
            visualizacion.delete()
            datos = {'message': 'Success'}
        except Visualizaciones.DoesNotExist:
            datos = {'message': 'Visualización no encontrada'}

        return JsonResponse(datos)

class RegistroSessionesView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if id > 0:
            try:
                sesion_obj = RegistroSessiones.objects.get(id=id)
                sesion_data = {
                    'id': sesion_obj.id,
                    'usuarioId': {
                        'id': sesion_obj.usuarioId.id,
                        'correo': sesion_obj.usuarioId.correo
                    },
                    'fechaHoraInSesion': sesion_obj.fechaHoraInSesion
                }
                datos = {'message': 'Success', 'sesion': sesion_data}
            except RegistroSessiones.DoesNotExist:
                datos = {'message': 'Sesión no encontrada'}
        else:
            sesiones_data = list(RegistroSessiones.objects.values())
            if len(sesiones_data) > 0:
                datos = {'message': 'Success', 'sesiones': sesiones_data}
            else:
                datos = {'message': 'Sesiones no encontradas'}

        return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body)
        usuario_id = jd.get('usuarioId', None)

        try:
            usuario = usuarios.objects.get(id=usuario_id)

            nueva_sesion = RegistroSessiones(
                usuarioId=usuario
                ##nose si mandarlo ya que es un dato tipo fecha que se genera solo
            )
            nueva_sesion.save()

            datos = {'message': 'Success'}
        except usuarios.DoesNotExist as e:
            datos = {'message': f'Error: {str(e)}'}

        return JsonResponse(datos)

    def put(self, request, id):
        jd = json.loads(request.body)
        try:
            sesion = RegistroSessiones.objects.get(id=id)
            sesion.usuarioId = usuarios.objects.get(id=jd['usuarioId'])
            sesion.save()
            datos = {'message': 'Success'}
        except RegistroSessiones.DoesNotExist:
            datos = {'message': 'Sesión no encontrada'}
        except usuarios.DoesNotExist as e:
            datos = {'message': f'Error: {str(e)}'}

        return JsonResponse(datos)

    def delete(self, request, id):
        try:
            sesion = RegistroSessiones.objects.get(id=id)
            sesion.delete()
            datos = {'message': 'Success'}
        except RegistroSessiones.DoesNotExist:
            datos = {'message': 'Sesión no encontrada'}

        return JsonResponse(datos)
    
class DescargasOfflineView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if id > 0:
            try:
                descarga_obj = DescargasOffline.objects.get(id=id)
                descarga_data = {
                    'id': descarga_obj.id,
                    'usuarioId': {
                        'id': descarga_obj.usuarioId.id,
                        'correo': descarga_obj.usuarioId.correo
                    },
                    'contenido': {
                        'id': descarga_obj.contenido.id,
                        'titulo': descarga_obj.contenido.titulo,
                        'descripcion': descarga_obj.contenido.descripcion,
                        'anioLanzamiento': descarga_obj.contenido.anioLanzamiento,
                        'clasificacionEdad': {
                            'id': descarga_obj.contenido.clasificacionEdad.id,
                            'clasificacion': descarga_obj.contenido.clasificacionEdad.clasificacion
                        },
                        'idiomaOriginal': {
                            'id': descarga_obj.contenido.idiomaOriginal.id,
                            'nombre': descarga_obj.contenido.idiomaOriginal.nombre
                         }
                    },
                    'fechaDescarga': descarga_obj.fechaDescarga
                }
                datos = {'message': 'Success', 'descarga': descarga_data}
            except DescargasOffline.DoesNotExist:
                datos = {'message': 'Descarga no encontrada'}
        else:
            descargas_data = list(DescargasOffline.objects.values())
            if len(descargas_data) > 0:
                datos = {'message': 'Success', 'descargas': descargas_data}
            else:
                datos = {'message': 'Descargas no encontradas'}

        return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body)
        usuario_id = jd.get('usuarioId', None)
        contenido_id = jd.get('contenidoId', None)

        try:
            usuario = usuarios.objects.get(id=usuario_id)
            contenidoObj = contenido.objects.get(id=contenido_id)

            nueva_descarga = DescargasOffline(
                usuarioId=usuario,
                contenido=contenidoObj
                ## aqui nose si recopilarlo ya que es un dato tipo fecha que se genera solo
            )
            nueva_descarga.save()

            datos = {'message': 'Success'}
        except (usuarios.DoesNotExist, contenido.DoesNotExist) as e:
            datos = {'message': f'Error: {str(e)}'}

        return JsonResponse(datos)

    def put(self, request, id):
        jd = json.loads(request.body)
        try:
            descarga = DescargasOffline.objects.get(id=id)
            descarga.usuarioId = usuarios.objects.get(id=jd['usuarioId'])
            descarga.contenido = contenido.objects.get(id=jd['contenidoId'])
            descarga.save()
            datos = {'message': 'Success'}
        except DescargasOffline.DoesNotExist:
            datos = {'message': 'Descarga no encontrada'}
        except (usuarios.DoesNotExist, contenido.DoesNotExist) as e:
            datos = {'message': f'Error: {str(e)}'}

        return JsonResponse(datos)

    def delete(self, request, id):
        try:
            descarga = DescargasOffline.objects.get(id=id)
            descarga.delete()
            datos = {'message': 'Success'}
        except DescargasOffline.DoesNotExist:
            datos = {'message': 'Descarga no encontrada'}

        return JsonResponse(datos)

class PopularidadView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if id > 0:
            try:
                popularidad_obj = Popularidad.objects.get(id=id)
                popularidad_data = {
                    'id': popularidad_obj.id,
                    'contenido': {
                        'id': popularidad_obj.contenido.id,
                        'titulo': popularidad_obj.contenido.titulo,
                        'descripcion': popularidad_obj.contenido.descripcion,
                        'anioLanzamiento': popularidad_obj.contenido.anioLanzamiento,
                        'clasificacionEdad': {
                            'id': popularidad_obj.contenido.clasificacionEdad.id,
                            'clasificacion': popularidad_obj.contenido.clasificacionEdad.clasificacion
                        },
                        'idiomaOriginal': {
                            'id': popularidad_obj.contenido.idiomaOriginal.id,
                            'nombre': popularidad_obj.contenido.idiomaOriginal.nombre
                        }
                    },
                    'cantidadVisualizaciones': popularidad_obj.cantidadVisualizaciones
                }
                datos = {'message': 'Success', 'popularidad': popularidad_data}
            except Popularidad.DoesNotExist:
                datos = {'message': 'Popularidad no encontrada'}
        else:
            
            popularidades_data = list(Popularidad.objects.order_by('cantidadVisualizaciones').values())
            
            if len(popularidades_data) > 0:
                datos = {'message': 'Success', 'popularidades': popularidades_data}
            else:
                datos = {'message': 'Popularidades no encontradas'}

        return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body)
        contenido_id = jd.get('contenidoId', None)

        try:
            contenidoId = contenido.objects.get(id=contenido_id)

            nueva_popularidad = Popularidad(
                contenido=contenidoId,
                cantidadVisualizaciones=jd.get('cantidadVisualizaciones', 0)
            )
            nueva_popularidad.save()

            datos = {'message': 'Success'}
        except contenido.DoesNotExist as e:
            datos = {'message': f'Error: {str(e)}'}

        return JsonResponse(datos)

    def put(self, request, id):
        jd = json.loads(request.body)
        try:
            popularidad = Popularidad.objects.get(id=id)
            popularidad.contenido = contenido.objects.get(id=jd['contenidoId'])
            popularidad.cantidadVisualizaciones = jd.get('cantidadVisualizaciones', 0)
            popularidad.save()
            datos = {'message': 'Success'}
        except Popularidad.DoesNotExist:
            datos = {'message': 'Popularidad no encontrada'}
        except contenido.DoesNotExist as e:
            datos = {'message': f'Error: {str(e)}'}

        return JsonResponse(datos)

    def delete(self, request, id):
        try:
            popularidad = Popularidad.objects.get(id=id)
            popularidad.delete()
            datos = {'message': 'Success'}
        except Popularidad.DoesNotExist:
            datos = {'message': 'Popularidad no encontrada'}

        return JsonResponse(datos)

class HistorialVisualizacionView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if id > 0:
            try:
                historial_obj = HistorialVisualizacion.objects.get(id=id)
                historial_data = {
                    'id': historial_obj.id,
                    'usuarioId': {
                        'id': historial_obj.usuarioId.id,
                        'correo': historial_obj.usuarioId.correo
                    },
                    'contenido': {
                        'id': historial_obj.contenido.id,
                        'titulo': historial_obj.contenido.titulo,
                        'descripcion': historial_obj.contenido.descripcion,
                        'anioLanzamiento': historial_obj.contenido.anioLanzamiento,
                        'clasificacionEdad': {
                            'id': historial_obj.contenido.clasificacionEdad.id,
                            'clasificacion': historial_obj.contenido.clasificacionEdad.clasificacion
                        },
                        'idiomaOriginal': {
                            'id': historial_obj.contenido.idiomaOriginal.id,
                            'nombre': historial_obj.contenido.idiomaOriginal.nombre
                         }
                    },
                    'fechaVisualizacion': historial_obj.fechaVisualizacion,
                    'duracionVisualizacion': historial_obj.duracionVisualizacion
                }
                datos = {'message': 'Success', 'historial': historial_data}
            except HistorialVisualizacion.DoesNotExist:
                datos = {'message': 'Historial no encontrado'}
        else:
            historiales_data = list(HistorialVisualizacion.objects.values())
            if len(historiales_data) > 0:
                datos = {'message': 'Success', 'historiales': historiales_data}
            else:
                datos = {'message': 'Historiales no encontrados'}

        return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body)
        usuario_id = jd.get('usuarioId', None)
        contenido_id = jd.get('contenidoId', None)

        try:
            usuario = usuarios.objects.get(id=usuario_id)
            contenidoObj = contenido.objects.get(id=contenido_id)

            nuevo_historial = HistorialVisualizacion(
                usuarioId=usuario,
                contenido=contenidoObj,
                duracionVisualizacion=jd.get('duracionVisualizacion', 0)
            )
            nuevo_historial.save()

            datos = {'message': 'Success'}
        except (usuarios.DoesNotExist, contenido.DoesNotExist) as e:
            datos = {'message': f'Error: {str(e)}'}

        return JsonResponse(datos)

    def put(self, request, id):
        jd = json.loads(request.body)
        try:
            historial = HistorialVisualizacion.objects.get(id=id)
            historial.usuarioId = usuarios.objects.get(id=jd['usuarioId'])
            historial.contenido = contenido.objects.get(id=jd['contenidoId'])
            historial.duracionVisualizacion = jd.get('duracionVisualizacion', 0)
            historial.save()
            datos = {'message': 'Success'}
        except HistorialVisualizacion.DoesNotExist:
            datos = {'message': 'Historial no encontrado'}
        except (usuarios.DoesNotExist, contenido.DoesNotExist) as e:
            datos = {'message': f'Error: {str(e)}'}

        return JsonResponse(datos)

    def delete(self, request, id):
        try:
            historial = HistorialVisualizacion.objects.get(id=id)
            historial.delete()
            datos = {'message': 'Success'}
        except HistorialVisualizacion.DoesNotExist:
            datos = {'message': 'Historial no encontrado'}

        return JsonResponse(datos)
