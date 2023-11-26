# Generated by Django 4.2.7 on 2023-11-26 18:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='clasificacionEdad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clasificacion', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='generos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='peliculas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=255)),
                ('anioLanzamiento', models.DateField()),
                ('duracion', models.IntegerField()),
                ('clasificacionEdad', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.clasificacionedad')),
            ],
        ),
        migrations.CreateModel(
            name='peliculas_generos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.generos')),
                ('pelicula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.peliculas')),
            ],
        ),
        migrations.CreateModel(
            name='perfiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='series',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=255)),
                ('anioLanzamiento', models.DateField()),
                ('clasificacionEdad', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.clasificacionedad')),
            ],
        ),
        migrations.CreateModel(
            name='telefonos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telefono', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='tipoUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='usuarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('correo', models.CharField(max_length=255, unique=True)),
                ('contrasena', models.CharField(max_length=50)),
                ('fechaRegistro', models.DateTimeField(auto_now_add=True)),
                ('tipoUsuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.tipousuario')),
            ],
        ),
        migrations.DeleteModel(
            name='prueba',
        ),
        migrations.AddField(
            model_name='telefonos',
            name='usuarioId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.usuarios'),
        ),
        migrations.AddField(
            model_name='perfiles',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.usuarios'),
        ),
    ]
