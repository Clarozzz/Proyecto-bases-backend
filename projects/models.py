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