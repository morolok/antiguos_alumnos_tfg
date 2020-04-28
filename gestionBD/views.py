from django.http import HttpResponse, FileResponse, Http404
from django.shortcuts import render
from antiguos_alumnos_tfg.settings import MEDIA_URL, MEDIA_ROOT
import os
#from gestionBD.models import Titulacion, JuntaRectora, TipoActividad, RevistaIngenio, TipoUsuario
import gestionBD.models as modelos
import gestionBD.forms as formularios

# Create your views here.

from django.shortcuts import render


def saludo(request):
    return HttpResponse("Pagina del TFG")


def inicio(request):
	return render(request, "index.html")


def asociacion(request):
    return render(request, "asociacion.html")


def actividades(request):
    return render(request, "actividades.html")


def noticias(request):
    return render(request, "noticias.html")


def empleo(request):
    return render(request, "empleo.html")


def revistaIngenio(request):
    revistas = modelos.RevistaIngenio.objects.all()
    return render(request, "revistaIngenio.html", {'revistas': revistas, 'MEDIA_URL': MEDIA_URL})


def multimedia(request):
    return render(request, "multimedia.html")

def juntaRectora(request):
    return render(request, "juntaRectora.html")

def formularioAltaUsuario(request):
    tiposUsuario = modelos.TipoUsuario.objects.all()
    titulaciones = modelos.Titulacion.objects.all()
    puestosJuntaRectora = modelos.JuntaRectora.objects.all()
    formUsuario = formularios.FormularioAltaUsuario(request.POST or None)
    contexto = {'titulaciones': titulaciones, 'puestosJuntaRectora': puestosJuntaRectora, 'tiposUsuario': tiposUsuario, 'formUsuario': formUsuario}
    return render(request, "formularioAltaUsuario.html", contexto)

def formularioAltaActividad(request):
    tiposDeActividad = modelos.TipoActividad.objects.all()
    return render(request, "formularioAltaActividad.html", {'tiposDeActividad': tiposDeActividad})

def formularioAltaNoticia(request):
    return render(request, "formularioAltaNoticia.html")

def formularioAltaOfertaEmpleo(request):
    titulaciones = modelos.Titulacion.objects.all()
    return render(request, "formularioAltaOfertaEmpleo.html", {'titulaciones': titulaciones})

def formularioAltaDatosDeContacto(request):
    return render(request, "formularioAltaDatosDeContacto.html")

def formularioAltaRevistaIngenio(request):
    return render(request, "formularioAltaRevistaIngenio.html")

