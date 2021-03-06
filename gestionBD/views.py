from django.http import HttpResponse, FileResponse, Http404
from django.shortcuts import render, redirect, reverse
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from antiguos_alumnos_tfg.settings import MEDIA_URL, MEDIA_ROOT
import gestionBD.models as modelos
import gestionBD.forms as formularios
from django.conf import settings


#from django.db.models import CharField
#from django.db.models.functions import Lower
#CharField.register_lookup(Lower)
#from gestionBD.models import Titulacion, JuntaRectora, TipoActividad, RevistaIngenio, TipoUsuario
#from datetime import datetime


# Create your views here.


def busqueda(request):
    contexto = {}
    if(request.method=='POST'):
        palabra = request.POST.get('buscar')
        noticias = modelos.Noticia.objects.filter(titulo__unaccent__icontains=palabra)
        actividades = modelos.Actividad.objects.filter(titulo__unaccent__icontains=palabra)
        contexto['palabra'] = palabra
        contexto['noticias'] = noticias
        contexto['actividades'] = actividades
    return render(request, "busqueda.html", contexto)


def inicio(request):
    noticias = modelos.Noticia.objects.all()
    contexto = {'noticias': noticias}
    return render(request, "index.html", contexto)


def asociacion(request):
    return render(request, "asociacion.html")


def actividades(request):
    actividades = modelos.Actividad.objects.order_by('-fecha')
    diccionarioActividades = {}
    for i in range(0, len(actividades)):
        diccionarioActividades[i] = str(actividades[i].titulo)
    request.session['diccionarioActividades'] = diccionarioActividades
    contexto = {'actividades': actividades}
    return render(request, "actividades.html", contexto)


def actividad(request, titulo):
    actividad = modelos.Actividad.objects.get(titulo=titulo)
    lineas = actividad.descripcion.splitlines()
    contexto = {'actividad': actividad, 'MEDIA_URL': MEDIA_URL, 'lineas': lineas}
    diccionarioActividades = request.session['diccionarioActividades']
    for c, v in diccionarioActividades.items():
        if(v == titulo):
            actividadActual = int(c)
            break
    totalActividades = len(diccionarioActividades.keys())
    if(actividadActual == totalActividades-1):
        haySiguiente = False
        contexto['haySiguiente'] = haySiguiente
    else:
        actividadSiguiente = actividadActual+1
        tituloSiguiente = diccionarioActividades.get(str(actividadSiguiente))
        haySiguiente = True
        contexto['haySiguiente'] = haySiguiente
        contexto['tituloSiguiente'] = tituloSiguiente
    if(actividadActual == 0):
        hayAnterior = False
        contexto['hayAnterior'] = hayAnterior
    else:
        actividadAnterior = actividadActual-1
        tituloAnterior = diccionarioActividades.get(str(actividadAnterior))
        hayAnterior = True
        contexto['hayAnterior'] = hayAnterior
        contexto['tituloAnterior'] = tituloAnterior
    return render(request, "actividad.html", contexto)


def noticias(request):
    noticias = modelos.Noticia.objects.order_by('-fecha')
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


def perfil(request):
    contexto = {}
    if('usuario' in request.session.keys()):
        usuarioLogin = request.session['usuario']
        contexto['inicioSesion'] = True
        usuario = modelos.Usuario.objects.get(usuario = usuarioLogin)
        contexto['nombreUsuario'] = usuario.nombre
        contexto['apellidosUsuario'] = usuario.apellidos
        contexto['dniUsuario'] = usuario.dni
        contexto['fechaNacimientoUsuario'] = usuario.fechaNacimiento
        contexto['cuentaBancariaUsuario'] = usuario.cuentaBancaria
        contexto['emailUsuario'] = usuario.email
        contexto['telefonoUsuario'] = usuario.telefono
        contexto['direccionPostalUsuario'] = usuario.direccionPostal
        contexto['usuarioUsuario'] = usuario.usuario
        contexto['tipoUsuario'] = usuario.tipo
        contexto['titulacionUsuario'] = usuario.titulacion
        contexto['promocionUsuario'] = usuario.promocion
        contexto['añoFinalizacionUsuario'] = usuario.añoFinalizacion
        contexto['empresaUsuario'] = usuario.empresa
        contexto['comunicacionesUsuario'] = usuario.comunicaciones
        contexto['juntaRectoraUsuario'] = usuario.juntaRectora
    else:
        contexto['inicioSesion'] = False
    return render(request, "perfil.html", contexto)


def formularioAltaUsuario(request):
    formUsuario = formularios.FormularioAltaUsuario(request.POST or None)
    contexto = {'formUsuario': formUsuario}
    if(request.method == 'POST'):
        if(formUsuario.is_valid()):
            usuario = formUsuario.save(commit=False)
            nombre = usuario.nombre
            apellidos = usuario.apellidos
            formUsuario.save()
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


def enviarCorreosConActividad(titulo, descripcion):
    usuarios = modelos.Usuario.objects.all()
    lsUsuarios = []
    for usu in usuarios:
        if(usu.comunicaciones):
            lsUsuarios.append(str(usu.email))
    emisor = settings.EMAIL_HOST_USER
    send_mail('Nueva actividad: '+titulo, descripcion, emisor, lsUsuarios, fail_silently=False, )


def formularioAltaActividad(request):
    formActividad = formularios.FormularioAltaActividad()
    contexto = {'formActividad': formActividad}
    if(request.method == 'POST'):
        formActividad = formularios.FormularioAltaActividad(request.POST, request.FILES)
        if(formActividad.is_valid()):
            actividad = formActividad.save(commit=False)
            titulo = actividad.titulo
            descripcion = actividad.descripcion
            formActividad.save()
            formActividad = formularios.FormularioAltaActividad()
            enviarCorreosConActividad(str(titulo), str(descripcion))
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
    contexto = {}
    if(request.method == 'POST'):
        formulario = request.POST
        usuario = formulario['usuario']
        try:
            usuarioBD = modelos.Usuario.objects.get(usuario=usuario)
        except ObjectDoesNotExist:
            error = "El usuario es incorrecto"
            contexto['error'] = error
            return render(request, "login.html", contexto)
        contraseña = formulario['contraseña']
        if(not (contraseña == usuarioBD.contraseña)):
            error = "La contraseña es incorrecta"
            contexto['error'] = error
        else:
            request.session['usuario'] = usuarioBD.usuario
            if(str(usuarioBD.tipo)=='Administrador'):
                request.session['esAdministrador'] = True
            else:
                request.session['esAdministrador'] = False
            return redirect('exitoLogin')

    return render(request, "login.html", contexto)


def exitoLogin(request):
    contexto = {}
    contexto['usuario'] = request.session.get('usuario')
    contexto['esAdministrador'] = request.session.get('esAdministrador')
    return render(request, "exitoLogin.html", contexto)


def logout(request):
    request.session['usuario'] = None
    return render(request, "logout.html")