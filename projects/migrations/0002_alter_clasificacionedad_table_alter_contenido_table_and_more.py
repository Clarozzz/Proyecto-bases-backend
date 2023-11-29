# Generated by Django 4.2.7 on 2023-11-29 07:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='clasificacionedad',
            table='clasificacionEdad',
        ),
        migrations.AlterModelTable(
            name='contenido',
            table='contenido',
        ),
        migrations.AlterModelTable(
            name='contenido_generos',
            table='contenido_generos',
        ),
        migrations.AlterModelTable(
            name='contenido_idiomas',
            table='contenido_idiomas',
        ),
        migrations.AlterModelTable(
            name='contenido_subtitulos',
            table='contenido_subtitulos',
        ),
        migrations.AlterModelTable(
            name='descargasoffline',
            table='DescargasOffline',
        ),
        migrations.AlterModelTable(
            name='episodios',
            table='episodios',
        ),
        migrations.AlterModelTable(
            name='estudiosproductoras',
            table='EstudiosProductoras',
        ),
        migrations.AlterModelTable(
            name='facturacion',
            table='Facturacion',
        ),
        migrations.AlterModelTable(
            name='generos',
            table='generos',
        ),
        migrations.AlterModelTable(
            name='historialvisualizacion',
            table='HistorialVisualizacion',
        ),
        migrations.AlterModelTable(
            name='idioma',
            table='idioma',
        ),
        migrations.AlterModelTable(
            name='lista_contenido',
            table='lista_contenido',
        ),
        migrations.AlterModelTable(
            name='listareproduccioncontenido',
            table='ListaReproduccionContenido',
        ),
        migrations.AlterModelTable(
            name='pais',
            table='pais',
        ),
        migrations.AlterModelTable(
            name='peliculas',
            table='peliculas',
        ),
        migrations.AlterModelTable(
            name='perfiles',
            table='perfiles',
        ),
        migrations.AlterModelTable(
            name='personas',
            table='personas',
        ),
        migrations.AlterModelTable(
            name='planes',
            table='Planes',
        ),
        migrations.AlterModelTable(
            name='playlists',
            table='Playlists',
        ),
        migrations.AlterModelTable(
            name='popularidad',
            table='Popularidad',
        ),
        migrations.AlterModelTable(
            name='registrosessiones',
            table='RegistroSessiones',
        ),
        migrations.AlterModelTable(
            name='rol',
            table='rol',
        ),
        migrations.AlterModelTable(
            name='series',
            table='series',
        ),
        migrations.AlterModelTable(
            name='subtitulos',
            table='subtitulos',
        ),
        migrations.AlterModelTable(
            name='telefonos',
            table='telefonos',
        ),
        migrations.AlterModelTable(
            name='temporadas',
            table='temporadas',
        ),
        migrations.AlterModelTable(
            name='usuarios',
            table='usuarios',
        ),
        migrations.AlterModelTable(
            name='valoracionescontenido',
            table='ValoracionesContenido',
        ),
        migrations.AlterModelTable(
            name='visualizaciones',
            table='Visualizaciones',
        ),
    ]