from django.conf import settings
from django.core import paginator
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.http import HttpResponse, FileResponse, Http404
from django.shortcuts import render, redirect, reverse

from antiguos_alumnos_tfg.settings import MEDIA_URL, MEDIA_ROOT
import gestionBD.models as modelos
import gestionBD.forms as formularios

import math
import twitter


#from django.db.models import CharField
#from django.db.models.functions import Lower
#CharField.register_lookup(Lower)
#from gestionBD.models import Titulacion, JuntaRectora, TipoActividad, RevistaIngenio, TipoUsuario
#from datetime import datetime

# Create your views here.


def busqueda(request):
    contexto = {}
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    if(request.method=='POST'):
        palabra = request.POST.get('buscar')
        noticias = modelos.Noticia.objects.filter(titulo__unaccent__icontains=palabra)
        actividades = modelos.Actividad.objects.filter(titulo__unaccent__icontains=palabra)
        contexto['palabra'] = palabra
        contexto['noticias'] = noticias
        contexto['actividades'] = actividades
    return render(request, "busqueda.html", contexto)


def inicio(request):
    contexto = {}
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    noticias = modelos.Noticia.objects.order_by('-fecha')
    contexto['noticias'] = noticias
    actividades = modelos.Actividad.objects.order_by('-fecha')[:3]
    ofertas_empleo = modelos.OfertaEmpleo.objects.order_by('-fecha')[:3]
    actividades_ofertas = []
    for i in range(3):
        actividades_ofertas.append(actividades[i])
        actividades_ofertas.append(ofertas_empleo[i])
    contexto['actividades_ofertas'] = actividades_ofertas
    return render(request, "index.html", contexto)


def asociacion(request):
    contexto = {}
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    return render(request, "asociacion.html", contexto)


def actividades(request):
    contexto = {}
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    actividades = modelos.Actividad.objects.order_by('-fecha')
    objetos_paginacion = 5
    paginator = Paginator(actividades, objetos_paginacion)
    pagina = request.GET.get('page')
    actividades_paginadas = paginator.get_page(pagina)
    numero_paginas = math.ceil(actividades.count()/objetos_paginacion)
    paginas = [i for i in range(1, numero_paginas+1)]
    diccionarioActividades = {}
    for i in range(0, len(actividades)):
        diccionarioActividades[i] = str(actividades[i].titulo)
    request.session['diccionarioActividades'] = diccionarioActividades
    #contexto['actividades'] = actividades
    contexto['actividades_paginadas'] = actividades_paginadas
    contexto['paginas'] = paginas
    
    tipoInicio = False
    tipoMedio = False
    tipoFin = False
    no_puntos_suspensivos = False
    
    if(numero_paginas > 6):
        if((pagina is None) or (pagina is not None and int(pagina) < 5)):
            tipoInicio = True
            rango_inicio = [i for i in range(1, 6)]
            contexto['rango_inicio'] = rango_inicio
        
        elif(pagina is not None and int(pagina) >= 5 and int(pagina) < numero_paginas):
            tipoMedio = True
            if((numero_paginas - int(pagina)) == 1):
                rango_medio = [i for i in range(int(pagina)-1, int(pagina)+1)]
                no_puntos_suspensivos = True
            else:
                rango_medio = [i for i in range(int(pagina)-1, int(pagina)+2)]
                if(numero_paginas - rango_medio[len(rango_medio)-1] == 1):
                    no_puntos_suspensivos = True
            contexto['rango_medio'] = rango_medio
        
        elif(pagina is not None and int(pagina) == numero_paginas):
            tipoFin = True
            rango_fin = [i for i in range(numero_paginas-3, numero_paginas+1)]
            contexto['rango_fin'] = rango_fin
    
    contexto['tipoInicio'] = tipoInicio
    contexto['tipoMedio'] = tipoMedio
    contexto['tipoFin'] = tipoFin
    contexto['no_puntos_suspensivos'] = no_puntos_suspensivos
    
    return render(request, "actividades.html", contexto)


def actividad(request, titulo):
    contexto = {}
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    actividad = modelos.Actividad.objects.get(titulo=titulo)
    lineas = actividad.descripcion.splitlines()
    contexto['actividad'] = actividad
    contexto['MEDIA_URL'] = MEDIA_URL
    contexto['lineas'] = lineas
    diccionarioActividades = request.session.get('diccionarioActividades')
    actividadActual = None
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
    contexto = {}
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    noticias = modelos.Noticia.objects.order_by('-fecha')
    #contexto['noticias'] = noticias
    
    objetos_paginacion = 5
    paginator = Paginator(noticias, objetos_paginacion)
    pagina = request.GET.get('page')
    noticias_paginadas = paginator.get_page(pagina)
    numero_paginas = math.ceil(noticias.count()/objetos_paginacion)
    paginas = [i for i in range(1, numero_paginas+1)]
    contexto['noticias_paginadas'] = noticias_paginadas
    contexto['paginas'] = paginas
    
    tipoInicio = False
    tipoMedio = False
    tipoFin = False
    no_puntos_suspensivos = False
    
    if(numero_paginas > 6):
        if((pagina is None) or (pagina is not None and int(pagina) < 5)):
            tipoInicio = True
            rango_inicio = [i for i in range(1, 6)]
            contexto['rango_inicio'] = rango_inicio
        
        elif(pagina is not None and int(pagina) >= 5 and int(pagina) < numero_paginas):
            tipoMedio = True
            if((numero_paginas - int(pagina)) == 1):
                rango_medio = [i for i in range(int(pagina)-1, int(pagina)+1)]
                no_puntos_suspensivos = True
            else:
                rango_medio = [i for i in range(int(pagina)-1, int(pagina)+2)]
                if(numero_paginas - rango_medio[len(rango_medio)-1] == 1):
                    no_puntos_suspensivos = True
            contexto['rango_medio'] = rango_medio
        
        elif(pagina is not None and int(pagina) == numero_paginas):
            tipoFin = True
            rango_fin = [i for i in range(numero_paginas-3, numero_paginas+1)]
            contexto['rango_fin'] = rango_fin
    
    contexto['tipoInicio'] = tipoInicio
    contexto['tipoMedio'] = tipoMedio
    contexto['tipoFin'] = tipoFin
    contexto['no_puntos_suspensivos'] = no_puntos_suspensivos

    return render(request, "noticias.html", contexto)


def noticia(request, titulo):
    contexto = {}
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    noticia = modelos.Noticia.objects.get(titulo = titulo)
    lineas = noticia.texto.splitlines()
    contexto['noticia'] = noticia
    contexto['MEDIA_URL'] = MEDIA_URL
    contexto['lineas'] = lineas
    return render(request, "noticia.html", contexto)


def empleo(request):
    contexto = {}
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    ofertasEmpleo = modelos.OfertaEmpleo.objects.all()
    #contexto['ofertasEmpleo'] = ofertasEmpleo

    objetos_paginacion = 5
    paginator = Paginator(ofertasEmpleo, objetos_paginacion)
    pagina = request.GET.get('page')
    ofertasEmpleo_paginadas = paginator.get_page(pagina)
    numero_paginas = math.ceil(ofertasEmpleo.count()/objetos_paginacion)
    paginas = [i for i in range(1, numero_paginas+1)]
    contexto['ofertasEmpleo_paginadas'] = ofertasEmpleo_paginadas
    contexto['paginas'] = paginas
    
    tipoInicio = False
    tipoMedio = False
    tipoFin = False
    no_puntos_suspensivos = False
    
    if(numero_paginas > 6):
        if((pagina is None) or (pagina is not None and int(pagina) < 5)):
            tipoInicio = True
            rango_inicio = [i for i in range(1, 6)]
            contexto['rango_inicio'] = rango_inicio
        
        elif(pagina is not None and int(pagina) >= 5 and int(pagina) < numero_paginas):
            tipoMedio = True
            if((numero_paginas - int(pagina)) == 1):
                rango_medio = [i for i in range(int(pagina)-1, int(pagina)+1)]
                no_puntos_suspensivos = True
            else:
                rango_medio = [i for i in range(int(pagina)-1, int(pagina)+2)]
                if(numero_paginas - rango_medio[len(rango_medio)-1] == 1):
                    no_puntos_suspensivos = True
            contexto['rango_medio'] = rango_medio
        
        elif(pagina is not None and int(pagina) == numero_paginas):
            tipoFin = True
            rango_fin = [i for i in range(numero_paginas-3, numero_paginas+1)]
            contexto['rango_fin'] = rango_fin
    
    contexto['tipoInicio'] = tipoInicio
    contexto['tipoMedio'] = tipoMedio
    contexto['tipoFin'] = tipoFin
    contexto['no_puntos_suspensivos'] = no_puntos_suspensivos
    
    return render(request, "empleo.html", contexto)


def ofertaEmpleo(request, titulo):
    contexto = {}
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    ofertaEmpleo = modelos.OfertaEmpleo.objects.get(titulo = titulo)
    lineas = ofertaEmpleo.texto.splitlines()
    contexto['ofertaEmpleo'] = ofertaEmpleo
    contexto['MEDIA_URL'] = MEDIA_URL
    contexto['lineas'] = lineas
    return render(request, "ofertaEmpleo.html", contexto)


def acuerdosEmpresas(request):
    contexto = {}
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    acuerdos = modelos.AcuerdosEmpresas.objects.all()
    contexto['acuerdos'] = acuerdos
    contexto['MEDIA_URL'] = MEDIA_URL
    return render(request, "acuerdosEmpresas.html", contexto)


def acuerdoEmpresa(request, nombre):
    contexto = {}
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    acuerdo = modelos.AcuerdosEmpresas.objects.get(nombre = nombre)
    lineas = acuerdo.texto.splitlines()
    contexto['acuerdo'] = acuerdo
    contexto['MEDIA_URL'] = MEDIA_URL
    contexto['lineas'] = lineas
    return render(request, "acuerdoEmpresa.html", contexto)


def revistaIngenio(request):
    contexto = {}
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    revistas = modelos.RevistaIngenio.objects.all()
    contexto['revistas'] = revistas
    contexto['MEDIA_URL'] = MEDIA_URL
    return render(request, "revistaIngenio.html", contexto)


def multimedia(request):
    contexto = {}
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    return render(request, "multimedia.html", contexto)


def juntaRectora(request):
    contexto = {}
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    return render(request, "juntaRectora.html", contexto)


def perfil(request):
    contexto = {}
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    if(usuario is not None):
        usuarioLogin = usuario
        #contexto['inicioSesion'] = True
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
    #else:
        #contexto['inicioSesion'] = False
    return render(request, "perfil.html", contexto)


def login(request):
    contexto = {}
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    if(request.method == 'POST'):
        formulario = request.POST
        usuarioFormulario = formulario['usuario']
        try:
            usuarioBD = modelos.Usuario.objects.get(usuario=usuarioFormulario)
        except ObjectDoesNotExist:
            error = "El usuario es incorrecto"
            contexto['error'] = error
            return render(request, "login.html", contexto)
        contraseña = formulario['contraseña']
        if(not (contraseña == usuarioBD.contraseña)):
            error = "La contraseña es incorrecta"
            contexto['error'] = error
        else:
            inicioSesion = True
            request.session['inicioSesion'] = inicioSesion
            request.session['usuario'] = usuarioBD.usuario
            if(str(usuarioBD.tipo)=='Administrador'):
                request.session['esAdministrador'] = True
            else:
                request.session['esAdministrador'] = False
            usuario = request.session.get('usuario')
            esAdministrador = request.session.get('esAdministrador')
            inicioSesion = request.session.get('inicioSesion')
            contexto['usuario'] = usuario
            contexto['esAdministrador'] = esAdministrador
            contexto['inicioSesion'] = inicioSesion
            return redirect('exitoLogin')
    return render(request, "login.html", contexto)


def exitoLogin(request):
    contexto = {}
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    return render(request, "exitoLogin.html", contexto)


def logout(request):
    contexto = {}
    request.session['usuario'] = None
    request.session['esAdministrador'] = False
    request.session['inicioSesion'] = False
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    return render(request, "logout.html", contexto)


def formularioAltaUsuario(request):
    contexto = {}
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    formUsuario = formularios.FormularioAltaUsuario(request.POST or None)
    contexto['formUsuario'] = formUsuario
    if(request.method == 'POST'):
        if(formUsuario.is_valid()):
            usuarioFormulario = formUsuario.save(commit=False)
            nombre = usuarioFormulario.nombre
            apellidos = usuarioFormulario.apellidos
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
    send_mail('Nueva actividad: ' + titulo, descripcion, emisor, lsUsuarios, fail_silently=False, )


def publicarTweetActividad(titulo):
    api_twitter = twitter.Api(consumer_key = 'XSPvc9U4HgUm2dfqoY9WBvtHI', 
        consumer_secret = 'manhSe3L3mnjKHQjMu3QtUtDBQSlqX29217dyjB7FA6gE4THT4',
        access_token_key = '1327583260348739590-6uTs3sucXoMRV4UyIJ0Tr2EdhOiSR0',
        access_token_secret = 'YHlo610QHMmU5cE7CVDAfR1GeAmWcbyuHvdcAPyONUP7O')
    texto_tweet = 'Nueva actividad creada: ' + titulo
    api_twitter.PostUpdate(status = texto_tweet)


def formularioAltaActividad(request):
    contexto = {}
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    formActividad = formularios.FormularioAltaActividad()
    contexto['formActividad'] = formActividad
    if(request.method == 'POST'):
        formActividad = formularios.FormularioAltaActividad(request.POST, request.FILES)
        if(formActividad.is_valid()):
            actividad = formActividad.save(commit=False)
            titulo = actividad.titulo
            descripcion = actividad.descripcion
            formActividad.save()
            formActividad = formularios.FormularioAltaActividad()
            enviarCorreosConActividad(str(titulo), str(descripcion))
            publicarTweetActividad(str(titulo))
            return redirect('exitoAltaActividad', titulo = titulo)
        else:
            if('__all__' in formActividad.errors.keys()):
                errores = [error for error in formActividad.errors['__all__']]
                contexto['errores'] = errores
            else:
                errores = [error for lsErrores in formActividad.errors.values() for error in lsErrores]
                contexto['errores'] = errores
    
    return render(request, "formularioAltaActividad.html", contexto)


def publicarTweetNoticia(titulo):
    api_twitter = twitter.Api(consumer_key = 'XSPvc9U4HgUm2dfqoY9WBvtHI', 
        consumer_secret = 'manhSe3L3mnjKHQjMu3QtUtDBQSlqX29217dyjB7FA6gE4THT4',
        access_token_key = '1327583260348739590-6uTs3sucXoMRV4UyIJ0Tr2EdhOiSR0',
        access_token_secret = 'YHlo610QHMmU5cE7CVDAfR1GeAmWcbyuHvdcAPyONUP7O')
    texto_tweet = 'Nueva noticia en la sociación: ' + titulo
    api_twitter.PostUpdate(status = texto_tweet)


def formularioAltaNoticia(request):
    contexto = {}
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    formNoticia = formularios.FormularioAltaNoticia()
    contexto['formNoticia'] = formNoticia
    if(request.method == 'POST'):
        formNoticia = formularios.FormularioAltaNoticia(request.POST, request.FILES)
        if(formNoticia.is_valid()):
            noticia = formNoticia.save(commit=False)
            titulo = noticia.titulo
            formNoticia.save()
            formNoticia = formularios.FormularioAltaNoticia()
            publicarTweetNoticia(str(titulo))
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
    contexto = {}
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    formOfertaEmpleo = formularios.FormularioAltaOfertaEmpleto()
    contexto['formOfertaEmpleo'] = formOfertaEmpleo
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
    contexto = {}
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    return render(request, "formularioAltaDatosDeContacto.html", contexto)


def formularioAltaRevistaIngenio(request):
    contexto = {}
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    formRevistaIngenio = formularios.FormularioAltaRevistaIngenio()
    contexto['formRevistaIngenio'] = formRevistaIngenio
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
    contexto = {}
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    formAcuerdo = formularios.FormularioAltaAcuerdoEmpresa()
    contexto['formAcuerdo'] = formAcuerdo
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
    contexto = {}
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    contexto['numero'] = numero
    return render(request, "exitoAltaRevistaIngenio.html", contexto)


def exitoAltaUsuario(request, nombre, apellidos):
    contexto = {}
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    contexto['nombre'] = nombre
    contexto['apellidos'] = apellidos
    return render(request, "exitoAltaUsuario.html", contexto)


def exitoAltaActividad(request, titulo):
    contexto = {}
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    contexto['titulo'] = titulo
    return render(request, "exitoAltaActividad.html", contexto)


def exitoAltaNoticia(request, titulo):
    contexto = {}
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    contexto['titulo'] = titulo
    return render(request, "exitoAltaNoticia.html", contexto)


def exitoAltaOfertaEmpleo(request, titulo):
    contexto = {}
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    contexto['titulo'] = titulo
    return render(request, "exitoAltaOfertaEmpleo.html", contexto)


def exitoAltaAcuerdoEmpresa(request, nombre):
    contexto = {}
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    contexto['nombre'] = nombre
    return render(request, "exitoAltaAcuerdoEmpresa.html", contexto)