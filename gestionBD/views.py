from django.http import HttpResponse, FileResponse, Http404
from django.shortcuts import render, redirect, reverse
from antiguos_alumnos_tfg.settings import MEDIA_URL, MEDIA_ROOT
import os
import hashlib
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
    actividades = modelos.Actividad.objects.all()
    contexto = {'actividades': actividades}
    return render(request, "actividades.html", contexto)


def actividad(request, titulo):
    actividad = modelos.Actividad.objects.get(titulo=titulo)
    lineas = actividad.descripcion.splitlines()
    contexto = {'actividad': actividad, 'MEDIA_URL': MEDIA_URL, 'lineas': lineas}
    return render(request, "actividad.html", contexto)


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
        if(formUsuario.is_valid()):
            usuario = formUsuario.save(commit=False)
            salt = os.urandom(32)
            usuario.contraseña = hashlib.pbkdf2_hmac('sha256', usuario.contraseña.encode('utf-8'), salt, 1, dklen=128).hex()
            nombre = usuario.nombre
            apellidos = usuario.apellidos
            formUsuario = formularios.FormularioAltaUsuario()
            formUsuario.save()
            return redirect('exitoAltaUsuario', nombre=nombre, apellidos=apellidos)
        else:
            if('__all__' in formUsuario.errors.keys()):
                errores = [error for error in formUsuario.errors['__all__']]
                contexto['errores'] = errores
            else:
                errores = [error for lsErrores in formUsuario.errors.values() for error in lsErrores]
                contexto['errores'] = errores
    
    return render(request, "formularioAltaUsuario.html", contexto)


def formularioAltaActividad(request):
    formActividad = formularios.FormularioAltaActividad()
    contexto = {'formActividad': formActividad}
    if(request.method == 'POST'):
        formActividad = formularios.FormularioAltaActividad(request.POST, request.FILES)
        if(formActividad.is_valid()):
            actividad = formActividad.save(commit=False)
            titulo = actividad.titulo
            formActividad.save()
            formActividad = formularios.FormularioAltaActividad()
            return redirect('exitoAltaActividad', titulo = titulo)
        else:
            if('__all__' in formActividad.errors.keys()):
                errores = [error for error in formActividad.errors['__all__']]
                contexto['errores'] = errores
            else:
                errores = [error for lsErrores in formActividad.errors.values() for error in lsErrores]
                contexto['errores'] = errores
    
    return render(request, "formularioAltaActividad.html", contexto)


def formularioAltaNoticia(request):
    formNoticia = formularios.FormularioAltaNoticia()
    contexto = {'formNoticia': formNoticia}
    if(request.method == 'POST'):
        formNoticia = formularios.FormularioAltaNoticia(request.POST, request.FILES)
        print(formNoticia.is_valid())
        if(formNoticia.is_valid()):
            print(formNoticia.data)
    return render(request, "formularioAltaNoticia.html", contexto)


def formularioAltaOfertaEmpleo(request):
    titulaciones = modelos.Titulacion.objects.all()
    return render(request, "formularioAltaOfertaEmpleo.html", {'titulaciones': titulaciones})


def formularioAltaDatosDeContacto(request):
    return render(request, "formularioAltaDatosDeContacto.html")


def formularioAltaRevistaIngenio(request):
    formRevistaIngenio = formularios.FormularioAltaRevistaIngenio()
    contexto = {'formRevistaIngenio': formRevistaIngenio}
    if(request.method == 'POST'):
        formRevistaIngenio = formularios.FormularioAltaRevistaIngenio(request.POST, request.FILES)
        if(formRevistaIngenio.is_valid()):
            revista = formRevistaIngenio.save(commit=False)
            numero = revista.numero
            formRevistaIngenio.save()
            formRevistaIngenio = formularios.FormularioAltaRevistaIngenio()
            return redirect('exitoAltaRevistaIngenio', numero = numero)
        else:
            print(formRevistaIngenio.errors)
            if('__all__' in formRevistaIngenio.errors.keys()):
                errores = [error for error in formRevistaIngenio.errors['__all__']]
                contexto['errores'] = errores
            else:
                errores = [error for lsErrores in formRevistaIngenio.errors.values() for error in lsErrores]
                contexto['errores'] = errores
    return render(request, "formularioAltaRevistaIngenio.html", contexto)


def exitoAltaRevistaIngenio(request, numero):
    contexto = {'numero': numero}
    return render(request, "exitoAltaRevistaIngenio.html", contexto)


def exitoAltaUsuario(request, nombre, apellidos):
    contexto = {'nombre': nombre, 'apellidos': apellidos}
    return render(request, "exitoAltaUsuario.html", contexto)


def exitoAltaActividad(request, titulo):
    contexto = {'titulo': titulo}
    return render(request, "exitoAltaActividad.html", contexto)