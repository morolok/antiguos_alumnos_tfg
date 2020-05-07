"""antiguos_alumnos_tfg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

#C:\Users\carlo\Documents\Carlos Mata Blasco\Universidad\Django\antiguos_alumnos_tfg


from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.views import static as static2
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

#from antiguos_alumnos_tfg.views import saludo, inicio, asociacion, actividades, noticias, empleo, revistaIngenio, multimedia, juntaRectora
from gestionBD import views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('media/<path>', static2.serve, {'document_root': settings.MEDIA_ROOT,}),
    path('antalumnos/', views.inicio, name='inicio'),
    path('antalumnos/asociacion/', views.asociacion, name='asociacion'),
    path('antalumnos/actividades/', views.actividades, name='actividades'),
    path('antalumnos/actividad/<titulo>/', views.actividad, name='actividad'),
    path('antalumnos/noticias/', views.noticias, name='noticias'),
    path('antalumnos/noticia/<titulo>', views.noticia, name='noticia'),
    path('antalumnos/empleo/', views.empleo, name='empleo'),
    path('antalumnos/revistaIngenio/', views.revistaIngenio, name='revistaIngenio'),
    path('antalumnos/multimedia/', views.multimedia, name='multimedia'),
    path('antalumnos/juntaRectora/', views.juntaRectora, name='juntaRectora'),
    path('antalumnos/formularioAltaUsuario/', views.formularioAltaUsuario, name='formularioAltaUsuario'),
    path('antalumnos/formularioAltaActividad/', views.formularioAltaActividad, name='formularioAltaActividad'),
    path('antalumnos/formularioAltaNoticia/', views.formularioAltaNoticia, name='formularioAltaNoticia'),
    path('antalumnos/formularioAltaOfertaEmpleo/', views.formularioAltaOfertaEmpleo, name='formularioAltaOfertaEmpleo'),
    path('antalumnos/formularioAltaDatosDeContacto/', views.formularioAltaDatosDeContacto, name='formularioAltaDatosDeContacto'),
    path('antalumnos/formularioAltaRevistaIngenio/', views.formularioAltaRevistaIngenio, name='formularioAltaRevistaIngenio'),
    path('antalumnos/exitoAltaRevistaIngenio/<numero>/', views.exitoAltaRevistaIngenio, name='exitoAltaRevistaIngenio'),
    path('antalumnos/exitoAltaUsuario/<nombre>/<apellidos>/', views.exitoAltaUsuario, name='exitoAltaUsuario'),
    path('antalumnos/exitoAltaActividad/<titulo>', views.exitoAltaActividad, name='exitoAltaActividad'),
    path('antalumnos/exitoAltaNoticia/<titulo>', views.exitoAltaNoticia, name='exitoAltaNoticia'),
    path('antalumnos/exitoAltaOfertaEmpleo/<titulo>', views.exitoAltaOfertaEmpleo, name='exitoAltaOfertaEmpleo'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()