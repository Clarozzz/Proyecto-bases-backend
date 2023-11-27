from django.db import models

# Create your models here.
class tipoUsuario(models.Model):
    tipo = models.CharField(max_length=50)

class usuarios(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.CharField(max_length=255, unique=True)
    contrasena = models.CharField(max_length=50)
    fechaRegistro = models.DateTimeField(auto_now_add=True)
    tipoUsuario = models.ForeignKey(tipoUsuario, on_delete=models.SET_NULL, null=True)

class telefonos(models.Model):
    usuarioId = models.ForeignKey(usuarios, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=8)

class perfiles(models.Model):
    nombre = models.CharField(max_length=50)
    usuario = models.ForeignKey(usuarios, on_delete=models.CASCADE)

class clasificacionEdad(models.Model):
    clasificacion = models.CharField(max_length=50)

class peliculas(models.Model):
    titulo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255)
    anioLanzamiento = models.DateField()
    clasificacionEdad = models.ForeignKey(clasificacionEdad, null=True, on_delete=models.SET_NULL)
    duracion = models.IntegerField()


class series(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255)
    anioLanzamiento = models.DateField()
    clasificacionEdad = models.ForeignKey(clasificacionEdad, null=True, on_delete=models.SET_NULL)

class generos(models.Model):
    nombre = models.CharField(max_length=50)

class peliculas_generos(models.Model):
    pelicula = models.ForeignKey(peliculas, on_delete=models.CASCADE)
    genero = models.ForeignKey(generos, on_delete=models.CASCADE)

class series_generos(models.Model):
    series = models.ForeignKey(series, on_delete=models.CASCADE)
    genero = models.ForeignKey(generos, on_delete=models.CASCADE)

class episodios(models.Model):
    serieId = models.ForeignKey(series, on_delete=models.SET_NULL, null=True)
    numeroEpisodio = models.IntegerField()
    tituloEpisodio = models.CharField(max_length=50)
    duracion = models.IntegerField()
    anoLanzamiento = models.DateField()

class ValoracionesPeliculas(models.Model):
    usuarioId  = models.ForeignKey(usuarios, on_delete=models.SET_NULL, null=True)
    peliculaId  = models.ForeignKey(peliculas, on_delete=models.SET_NULL, null=True)
    valoracion = models.IntegerField()
    comentario = models.TextField()
    fechaValoracion = models.DateTimeField(auto_now_add=True)


class ValoracionesSeries(models.Model):
    usuarioId = models.ForeignKey(usuarios,on_delete=models.SET_NULL, null=True)
    serieId = models.ForeignKey(series, on_delete=models.SET_NULL, null=True)
    valoracion = models.IntegerField()
    comentario = models.TextField()
    fechaValoracion = models.DateTimeField(auto_now_add=True)

class Playlists(models.Model):
    usuarioId = models.ForeignKey(usuarios, on_delete=models.SET_NULL, null=True)
    nombreLista = models.CharField(max_length=50)


class Planes(models.Model):
    nombre = models.CharField(max_length=50)
    precioMensual = models.DecimalField(max_digits=10, decimal_places=2)
    calidadVideo = models.CharField(max_length=50)
    resolucion = models.CharField(max_length=20)
class Facturacion(models.Model):
    usuarioId = models.ForeignKey(usuarios, on_delete=models.SET_NULL, null=True)
    numeroDeTarjeta = models.CharField(max_length=16)
    fechaDeVencimiento = models.DateField()
    cvv = models.CharField(max_length=4)
    nombreEnLaTarjeta = models.CharField(max_length=50)

class ActoresYActrices(models.Model):
    nombre = models.CharField(max_length=50)
    fechaDeNacimiento = models.DateField()
    nacionalidad = models.CharField(max_length=50)

class Directores(models.Model):
    nombre = models.CharField(max_length=50)
    fechaDeNacimiento = models.DateField()
    nacionalidad = models.CharField(max_length=50)

class EstudiosProductoras(models.Model):
    nombre = models.CharField(max_length=50)
    pais = models.CharField(max_length=50)
    anoDeFundacion = models.IntegerField()
    
class ListaReproduccionContenido(models.Model):
    usuarioId = models.ForeignKey(usuarios, on_delete=models.SET_NULL, null=True)
    nombreLista = models.CharField(max_length=50)
    peliculaId  = models.ForeignKey(peliculas, on_delete=models.SET_NULL, null=True)
    serieId = models.ForeignKey(series, on_delete=models.SET_NULL, null=True)
    
class Visualizaciones(models.Model):
    usuarioId=  models.ForeignKey(usuarios, on_delete=models.SET_NULL, null=True)
    peliculaId  = models.ForeignKey(peliculas, on_delete=models.SET_NULL, null=True)
    serieId = models.ForeignKey(series, on_delete=models.SET_NULL, null=True)
    fechaVisualizacion= models.DateTimeField(auto_now_add=True)
 
class ComentariosGenerales(models.Model):
    usuarioId = models.ForeignKey(usuarios, on_delete=models.SET_NULL, null=True)
    comentario = models.TextField()
    fechaComentario= models.DateTimeField(auto_now_add=True)
    
class RegistroSessiones(models.Model):
    usuarioId = models.ForeignKey(usuarios, on_delete=models.SET_NULL, null=True)
    fechaHoraInSesion= models.DateTimeField(auto_now_add=True)
    
class DescargasOffline(models.Model):
    usuarioId=  models.ForeignKey(usuarios, on_delete=models.SET_NULL, null=True)
    peliculaId  = models.ForeignKey(peliculas, on_delete=models.SET_NULL, null=True)
    serieId = models.ForeignKey(series, on_delete=models.SET_NULL, null=True)
    fechaDescarga= models.DateTimeField(auto_now_add=True)
    
class Subtitulos(models.Model):
    peliculaId  = models.ForeignKey(peliculas, on_delete=models.SET_NULL, null=True)
    serieId = models.ForeignKey(series, on_delete=models.SET_NULL, null=True)
    idioma= models.CharField(max_length=50)
    formato=models.CharField(max_length=3)
    RutaArchivo=models.CharField(max_length=50)
    fechaCreacion= models.DateTimeField()
    fechaModificacion= models.DateTimeField(auto_now_add=True)
    
class Popularidad(models.Model):
    serieId = models.ForeignKey(series, on_delete=models.SET_NULL, null=True) 
    peliculaId  = models.ForeignKey(peliculas, on_delete=models.SET_NULL, null=True)
    episodioId=  models.ForeignKey(episodios, on_delete=models.SET_NULL, null=True)
    cantidadVisualizaciones = models.IntegerField(default=0)

class HistorialVisualizacion(models.Model):
    usuarioId = models.ForeignKey(usuarios, on_delete=models.SET_NULL, null=True)
    TIPO_CONTENIDO_CHOICES = [
        ('serie', 'Serie'),
        ('pelicula', 'Película'),
        ('episodio', 'Episodio'),
    ]

    tipoContenido = models.CharField(
        max_length=10,
        choices=TIPO_CONTENIDO_CHOICES,
        default='serie'  # se puede establecer de deafualt cualuiqera al chile.
    )
    fechaVisualizacion = models.DateTimeField(auto_now_add=True)
    duracionVisualizacion = models.DecimalField(max_digits=4, decimal_places=2)

   
    
    
    
      
    
    
    
      
    
    
    
    