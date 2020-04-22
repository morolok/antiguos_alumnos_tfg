from django.http import HttpResponse
from django.shortcuts import render
from gestionBD.models import Titulacion, JuntaRectora, TipoActividad

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
    return render(request, "revistaIngenio.html")


def multimedia(request):
    return render(request, "multimedia.html")

def juntaRectora(request):
    return render(request, "juntaRectora.html")

def formularioAltaUsuario(request):
    titulaciones = Titulacion.objects.all()
    puestosJuntaRectora = JuntaRectora.objects.all()
    return render(request, "formularioAltaUsuario.html", {'titulaciones': titulaciones, 'puestosJuntaRectora': puestosJuntaRectora})

def formularioAltaActividad(request):
    tiposDeActividad = TipoActividad.objects.all()
    return render(request, "formularioAltaActividad.html", {'tiposDeActividad': tiposDeActividad})

def formularioAltaNoticia(request):
    return render(request, "formularioAltaNoticia.html")

def formularioAltaOfertaEmpleo(request):
    titulaciones = Titulacion.objects.all()
    return render(request, "formularioAltaOfertaEmpleo.html", {'titulaciones': titulaciones})

def formularioAltaDatosDeContacto(request):
    return render(request, "formularioAltaDatosDeContacto.html")

def formularioAltaRevistaIngenio(request):
    return render(request, "formularioAltaRevistaIngenio.html")
