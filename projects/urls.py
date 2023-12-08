from django.urls import path
from .views import *



urlpatterns = [
    path('tipoUsuario/', tipoUsuarioView.as_view(), name='tipoUsuario'),
    path('tipoUsuario/<int:id>/', tipoUsuarioView.as_view(), name='tipoUsuario_process'),
    path('usuario/', UsuariosView.as_view(), name='usuario'),
    path('usuario/<int:id>/', UsuariosView.as_view(), name='usuario_process'),
    path('telefonos/', TelefonosView.as_view(), name='telefonos'),
    path('telefonos/<int:id>/', TelefonosView.as_view(), name='telefonos_usuario'),
    path('perfiles/', PerfilesView.as_view(), name='perfiles'),
    path('perfiles/<int:id>/', PerfilesView.as_view(), name='perfiles_usuario'),
    path('clasificacionEdad/', ClasificacionEdadView.as_view(), name='clasificacionEdad'),
    path('clasificacionEdad/<int:id>/', ClasificacionEdadView.as_view(), name='clasificacionEdad_detail'),
    path('generos/', GenerosView.as_view(), name='generos'),
    path('generos/<int:id>/', GenerosView.as_view(), name='generos_detail'),
    path('idioma/', IdiomaView.as_view(), name='idioma'),
    path('idioma/<int:id>/', IdiomaView.as_view(), name='idioma_detail'),
    path('contenido/', ContenidoView.as_view(), name='contenido'),
    path('contenido/<int:id>/', ContenidoView.as_view(), name='contenido_detail'),
    path('contenido_generos/', ContenidoGenerosView.as_view(), name='contenido_generos'),
    path('contenido_generos/<int:id>/', ContenidoGenerosView.as_view(), name='contenido_generos_detail'),
    path('subtitulos/', SubtitulosView.as_view(), name='subtitulos'),
    path('subtitulos/<int:id>/', SubtitulosView.as_view(), name='subtitulos_detail'),
    path('peliculas/', PeliculasView.as_view(), name='peliculas'),
    path('peliculas/<int:id>/', PeliculasView.as_view(), name='peliculas_detail'),
    path('series/', SeriesView.as_view(), name='series'),
    path('series/<int:id>/', SeriesView.as_view(), name='series_detail'),
    path('contenido_subtitulos/', ContenidoSubtitulosView.as_view(), name='contenido_subtitulos_list'),
    path('contenido_subtitulos/<int:id>/', ContenidoSubtitulosView.as_view(), name='contenido_subtitulos_detail'),
    path('contenido_idiomas/', ContenidoIdiomasView.as_view(), name='contenido_idiomas_list'),
    path('contenido_idiomas/<int:id>/', ContenidoIdiomasView.as_view(), name='contenido_idiomas_detail'),
    path('temporadas/', TemporadasView.as_view(), name='temporadas_list'),
    path('temporadas/<int:id>/', TemporadasView.as_view(), name='temporadas_detail'),
    path('episodios/', EpisodiosView.as_view(), name='episodios_list'),
    path('episodios/<int:id>/', EpisodiosView.as_view(), name='episodios_detail'),
]