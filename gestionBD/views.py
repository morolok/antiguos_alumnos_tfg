from django.http import HttpResponse, FileResponse, Http404
from django.shortcuts import render, redirect, reverse
from antiguos_alumnos_tfg.settings import MEDIA_URL, MEDIA_ROOT
import os
import hashlib
import base64
#from gestionBD.models import Titulacion, JuntaRectora, TipoActividad, RevistaIngenio, TipoUsuario
import gestionBD.models as modelos
import gestionBD.forms as formularios
#from datetime import datetime

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
    noticias = modelos.Noticia.objects.all()
    contexto = {'noticias': noticias}
    return render(request, "noticias.html", contexto)


def noticia(request, titulo):
    noticia = modelos.Noticia.objects.get(titulo = titulo)
    lineas = noticia.texto.splitlines()
    contexto = {'noticia': noticia, 'MEDIA_URL': MEDIA_URL, 'lineas': lineas}
    return render(request, "noticia.html", contexto)


def empleo(request):
    ofertasEmpleo = modelos.OfertaEmpleo.objects.all()
    contexto = {'ofertasEmpleo': ofertasEmpleo}
    return render(request, "empleo.html", contexto)


def ofertaEmpleo(request, titulo):
    ofertaEmpleo = modelos.OfertaEmpleo.objects.get(titulo = titulo)
    lineas = ofertaEmpleo.texto.splitlines()
    contexto = {'ofertaEmpleo': ofertaEmpleo, 'MEDIA_URL': MEDIA_URL, 'lineas': lineas}
    return render(request, "ofertaEmpleo.html", contexto)


def acuerdosEmpresas(request):
    acuerdos = modelos.AcuerdosEmpresas.objects.all()
    contexto = {'acuerdos': acuerdos, 'MEDIA_URL': MEDIA_URL}
    return render(request, "acuerdosEmpresas.html", contexto)


def acuerdoEmpresa(request, nombre):
    acuerdo = modelos.AcuerdosEmpresas.objects.get(nombre = nombre)
    lineas = acuerdo.texto.splitlines()
    contexto = {'acuerdo': acuerdo, 'MEDIA_URL': MEDIA_URL, 'lineas': lineas}
    return render(request, "acuerdoEmpresa.html", contexto)


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
            salt = os.urandom(64)
            usuario.contraseña = hashlib.pbkdf2_hmac('sha256', usuario.contraseña.encode('utf-8'), salt, 1, dklen=128).hex()
            nombre = usuario.nombre
            apellidos = usuario.apellidos
            saltSalt = base64.b64encode(salt).decode('utf-8')
            usuarioSalt = usuario.usuario
            formUsuario.save()
            modelos.Salt.objects.create(usuarioUsuario=usuarioSalt, salt=saltSalt)
            formUsuario = formularios.FormularioAltaUsuario()
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
        if(formNoticia.is_valid()):
            noticia = formNoticia.save(commit=False)
            titulo = noticia.titulo
            formNoticia.save()
            formNoticia = formularios.FormularioAltaNoticia()
            return redirect('exitoAltaNoticia', titulo = titulo)
        else:
            if('__all__' in formNoticia.errors.keys()):
                errores = [error for error in formNoticia.errors['__all__']]
                contexto['errores'] = errores
            else:
                errores = [error for lsErrores in formNoticia.errors.values() for error in lsErrores]
                contexto['errores'] = errores
    return render(request, "formularioAltaNoticia.html", contexto)


def formularioAltaOfertaEmpleo(request):
    formOfertaEmpleo = formularios.FormularioAltaOfertaEmpleto()
    contexto = {'formOfertaEmpleo': formOfertaEmpleo}
    if(request.method == 'POST'):
        formOfertaEmpleo = formularios.FormularioAltaOfertaEmpleto(request.POST, request.FILES)
        if(formOfertaEmpleo.is_valid()):
            ofertaEmpleo = formOfertaEmpleo.save(commit=False)
            titulo = ofertaEmpleo.titulo
            formOfertaEmpleo.save()
            formOfertaEmpleo = formularios.FormularioAltaOfertaEmpleto()
            return redirect('exitoAltaOfertaEmpleo', titulo = titulo)
        else:
            if('__all__' in formOfertaEmpleo.errors.keys()):
                errores = [error for error in formOfertaEmpleo.errors['__all__']]
                contexto['errores'] = errores
            else:
                errores = [error for lsErrores in formOfertaEmpleo.errors.values() for error in lsErrores]
                contexto['errores'] = errores
    return render(request, "formularioAltaOfertaEmpleo.html", contexto)


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
            if('__all__' in formRevistaIngenio.errors.keys()):
                errores = [error for error in formRevistaIngenio.errors['__all__']]
                contexto['errores'] = errores
            else:
                errores = [error for lsErrores in formRevistaIngenio.errors.values() for error in lsErrores]
                contexto['errores'] = errores
    return render(request, "formularioAltaRevistaIngenio.html", contexto)


def formularioAltaAcuerdoEmpresa(request):
    formAcuerdo = formularios.FormularioAltaAcuerdoEmpresa()
    contexto = {'formAcuerdo': formAcuerdo}
    if(request.method == 'POST'):
        formAcuerdo = formularios.FormularioAltaAcuerdoEmpresa(request.POST, request.FILES)
        if(formAcuerdo.is_valid()):
            acuerdoEmpresa = formAcuerdo.save(commit=False)
            nombre = acuerdoEmpresa.nombre
            formAcuerdo.save()
            formAcuerdo = formularios.FormularioAltaAcuerdoEmpresa()
            return redirect('exitoAltaAcuerdoEmpresa', nombre = nombre)
        else:
            if('__all__' in formAcuerdo.errors.keys()):
                errores = [error for error in formAcuerdo.errors['__all__']]
                contexto['errores'] = errores
            else:
                errores = [error for lsErrores in formAcuerdo.errors.values() for error in lsErrores]
                contexto['errores'] = errores
    return render(request, "formularioAltaAcuerdoEmpresa.html", contexto)


def exitoAltaRevistaIngenio(request, numero):
    contexto = {'numero': numero}
    return render(request, "exitoAltaRevistaIngenio.html", contexto)


def exitoAltaUsuario(request, nombre, apellidos):
    contexto = {'nombre': nombre, 'apellidos': apellidos}
    return render(request, "exitoAltaUsuario.html", contexto)


def exitoAltaActividad(request, titulo):
    contexto = {'titulo': titulo}
    return render(request, "exitoAltaActividad.html", contexto)


def exitoAltaNoticia(request, titulo):
    contexto = {'titulo': titulo}
    return render(request, "exitoAltaNoticia.html", contexto)


def exitoAltaOfertaEmpleo(request, titulo):
    contexto = {'titulo': titulo}
    return render(request, "exitoAltaOfertaEmpleo.html", contexto)


def exitoAltaAcuerdoEmpresa(request, nombre):
    contexto = {'nombre': nombre}
    return render(request, "exitoAltaAcuerdoEmpresa.html", contexto)


def login(request):
    if(request.method == 'POST'):
        formulario = request.POST
        usuario = formulario['usuario']
        fila = modelos.Salt.objects.get(usuarioUsuario=usuario)
        token = fila.salt
        salt = base64.b64decode(token)
        contraseña = hashlib.pbkdf2_hmac('sha256', formulario['contraseña'].encode('utf-8'), salt, 1, dklen=128).hex()
        

    return render(request, "login.html")


