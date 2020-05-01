from django.http import HttpResponse, FileResponse, Http404
from django.shortcuts import render, redirect, reverse
from antiguos_alumnos_tfg.settings import MEDIA_URL, MEDIA_ROOT
import os
#from gestionBD.models import Titulacion, JuntaRectora, TipoActividad, RevistaIngenio, TipoUsuario
import gestionBD.models as modelos
import gestionBD.forms as formularios
from datetime import datetime

# Create your views here.

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
    formUsuario = formularios.FormularioAltaUsuario(request.POST or None)
    contexto = {'formUsuario': formUsuario}
    if(request.method == 'POST'):
        print(formUsuario.is_valid())
        if(formUsuario.is_valid()):
            pass
        else:
            errores = [error for error in formUsuario.errors['__all__']]
            contexto['errores'] = errores
        print(formUsuario.data)
    
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
    formRevistaIngenio = formularios.FormularioAltaRevistaIngenio()
    if(request.method == 'POST'):
        formRevistaIngenio = formularios.FormularioAltaRevistaIngenio(request.POST, request.FILES)
        if(formRevistaIngenio.is_valid()):
            revista = formRevistaIngenio.save(commit=False)
            numero = revista.numero
            formRevistaIngenio.save()
            formRevistaIngenio = formularios.FormularioAltaRevistaIngenio()
            return redirect('exitoAltaRevistaIngenio', numero = numero)
    contexto = {'formRevistaIngenio': formRevistaIngenio}
    return render(request, "formularioAltaRevistaIngenio.html", contexto)

def exitoAltaRevistaIngenio(request, numero):
    contexto = {'numero': numero}
    return render(request, "exitoAltaRevistaIngenio.html", contexto)