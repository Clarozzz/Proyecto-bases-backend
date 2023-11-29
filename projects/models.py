from django.db import models

# Create your models here.

class tipoUsuario(models.Model):
    tipo = models.CharField(max_length=50)
    class Meta:
        db_table = 'tipo_Usuario'

class usuarios(models.Model):
    correo = models.CharField(max_length=255, unique=True)
    contrasena = models.CharField(max_length=50)
    fechaRegistro = models.DateTimeField(auto_now_add=True)
    tipoUsuario = models.ForeignKey(tipoUsuario, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'usuarios'

class telefonos(models.Model):
    usuarioId = models.ForeignKey(usuarios, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=8)

    class Meta:
        db_table = 'telefonos'

class perfiles(models.Model):
    nombre = models.CharField(max_length=50)
    usuario = models.ForeignKey(usuarios, on_delete=models.CASCADE)

    class Meta:
        db_table = 'perfiles'

class clasificacionEdad(models.Model):
    clasificacion = models.CharField(max_length=50)

    class Meta:
        db_table = 'clasificacionEdad'

class generos(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        db_table = 'generos'

class idioma(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        db_table = 'idioma'

class contenido(models.Model):
    titulo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255)
    anioLanzamiento = models.DateField()
    clasificacionEdad = models.ForeignKey(clasificacionEdad, null=True, on_delete=models.SET_NULL)
    idiomaOriginal = models.ForeignKey(idioma, on_delete=models.CASCADE)

    class Meta:
        db_table = 'contenido'

class contenido_generos(models.Model):
    contenido = models.ForeignKey(contenido, null=True, on_delete=models.SET_NULL)
    generos = models.ForeignKey(generos, null=True, on_delete=models.SET_NULL)
    
    class Meta:
        db_table = 'contenido_generos'
class subtitulos(models.Model):
    idioma = models.ForeignKey(idioma, on_delete=models.CASCADE)

    class Meta:
        db_table = 'subtitulos'

class peliculas(models.Model):
    contenido = models.ForeignKey(contenido, on_delete=models.CASCADE)
    duracion = models.IntegerField()

    class Meta:
        db_table = 'peliculas'

class series(models.Model):
    contenido = models.ForeignKey(contenido, on_delete=models.CASCADE)
    cantTemporadas = models.IntegerField()

    class Meta:
        db_table = 'series'
class contenido_idiomas(models.Model):
    idioma = models.ForeignKey(idioma, null=True, on_delete=models.SET_NULL)
    contenido = models.ForeignKey(contenido, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'contenido_idiomas'
class contenido_subtitulos(models.Model):
    idioma = models.ForeignKey(idioma, null=True, on_delete=models.SET_NULL)
    contenido = models.ForeignKey(contenido, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'contenido_subtitulos'

class temporadas(models.Model):
    nombre = models.CharField(max_length=50)
    serie = models.ForeignKey(series, on_delete=models.CASCADE)
    anoDeEstreno = models.DateField()
    cantEpisodios = models.IntegerField()

    class Meta:
        db_table = 'temporadas'

class episodios(models.Model):
    temporada = models.ForeignKey(temporadas, on_delete=models.CASCADE)
    numeroEpisodio = models.IntegerField()
    tituloEpisodio = models.CharField(max_length=50)
    duracion = models.IntegerField()
    anoLanzamiento = models.DateField()
    descripcion = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'episodios'

class ValoracionesContenido(models.Model):
    usuarioId  = models.ForeignKey(usuarios, on_delete=models.CASCADE)
    contenido  = models.ForeignKey(contenido, on_delete=models.CASCADE)
    valoracion = models.IntegerField()
    comentario = models.TextField()
    fechaValoracion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ValoracionesContenido'

class Playlists(models.Model):
    usuarioId = models.ForeignKey(usuarios, on_delete=models.CASCADE)
    contenido = models.ForeignKey(contenido, on_delete=models.CASCADE)
    nombreLista = models.CharField(max_length=50)

    class Meta:
        db_table = 'Playlists'

class Planes(models.Model):
    nombre = models.CharField(max_length=50)
    precioMensual = models.DecimalField(max_digits=10, decimal_places=2)
    calidadVideo = models.CharField(max_length=50)
    resolucion = models.CharField(max_length=20)

    class Meta:
        db_table = 'Planes'

class Facturacion(models.Model):
    usuarioId = models.ForeignKey(usuarios, on_delete=models.SET_NULL, null=True)
    numeroDeTarjeta = models.CharField(max_length=16)
    fechaDeVencimiento = models.DateField()
    cvv = models.CharField(max_length=3)
    nombreEnLaTarjeta = models.CharField(max_length=50)

    class Meta:
        db_table = 'Facturacion'

class pais(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        db_table = 'pais'

class rol(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        db_table = 'rol'

class personas(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    fechaDeNacimiento = models.DateField()
    pais = models.ForeignKey(pais, null=True, on_delete=models.SET_NULL)
    rol = models.ForeignKey(rol, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'personas'

class EstudiosProductoras(models.Model):
    nombre = models.CharField(max_length=50)
    pais = models.ForeignKey(pais, null=True, on_delete=models.SET_NULL)
    anoDeFundacion = models.IntegerField()

    class Meta:
        db_table = 'EstudiosProductoras'
    
class ListaReproduccionContenido(models.Model):
    usuarioId = models.ForeignKey(usuarios, on_delete=models.SET_NULL, null=True)
    nombreLista = models.CharField(max_length=50)

    class Meta:
        db_table = 'ListaReproduccionContenido'

class lista_contenido(models.Model):
    lista = models.ForeignKey(ListaReproduccionContenido, on_delete=models.CASCADE)
    contenido = models.ForeignKey(contenido, on_delete=models.CASCADE)

    class Meta:
        db_table = 'lista_contenido'
    
class Visualizaciones(models.Model):
    usuarioId=  models.ForeignKey(usuarios, on_delete=models.SET_NULL, null=True)
    contenido = models.ForeignKey(contenido, on_delete=models.CASCADE)
    fechaVisualizacion= models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Visualizaciones'
    
class RegistroSessiones(models.Model):
    usuarioId = models.ForeignKey(usuarios, on_delete=models.SET_NULL, null=True)
    fechaHoraInSesion= models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'RegistroSessiones'
    
class DescargasOffline(models.Model):
    usuarioId=  models.ForeignKey(usuarios, on_delete=models.SET_NULL, null=True)
    contenido = models.ForeignKey(contenido, on_delete=models.CASCADE)
    fechaDescarga= models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'DescargasOffline'
    
class Popularidad(models.Model):
    contenido = models.ForeignKey(contenido, on_delete=models.CASCADE)
    cantidadVisualizaciones = models.IntegerField(default=0)

    class Meta:
        db_table = 'Popularidad'

class HistorialVisualizacion(models.Model):
    usuarioId = models.ForeignKey(usuarios, on_delete=models.SET_NULL, null=True)
    contenido = models.ForeignKey(contenido, on_delete=models.CASCADE)
    fechaVisualizacion = models.DateTimeField(auto_now_add=True)
    duracionVisualizacion = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        db_table = 'HistorialVisualizacion'