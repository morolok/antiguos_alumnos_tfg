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
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

#from antiguos_alumnos_tfg.views import saludo, inicio, asociacion, actividades, noticias, empleo, revistaIngenio, multimedia, juntaRectora
from gestionBD import views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('saludo/', views.saludo),
    path('antalumnos/', views.inicio, name='inicio'),
    path('asociacion/', views.asociacion, name='asociacion'),
    path('actividades/', views.actividades, name='actividades'),
    path('noticias/', views.noticias, name='noticias'),
    path('empleo/', views.empleo, name='empleo'),
    path('revistaIngenio/', views.revistaIngenio, name='revistaIngenio'),
    path('multimedia/', views.multimedia, name='multimedia'),
    path('juntaRectora/', views.juntaRectora, name='juntaRectora'),
    path('formularioAltaUsuario/', views.formularioAltaUsuario, name='formularioAltaUsuario'),
    path('formularioAltaActividad/', views.formularioAltaActividad, name='formularioAltaActividad'),
    path('formularioAltaNoticia/', views.formularioAltaNoticia, name='formularioAltaNoticia'),
    path('formularioAltaOfertaEmpleo/', views.formularioAltaOfertaEmpleo, name='formularioAltaOfertaEmpleo'),
    path('formularioAltaDatosDeContacto/', views.formularioAltaDatosDeContacto, name='formularioAltaDatosDeContacto'),
    path('formularioAltaRevistaIngenio/', views.formularioAltaRevistaIngenio, name='formularioAltaRevistaIngenio'),
    path('exitoAltaRevistaIngenio/<numero>/', views.exitoAltaRevistaIngenio, name='exitoAltaRevistaIngenio'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()