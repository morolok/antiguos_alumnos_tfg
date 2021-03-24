from django.conf import settings
from django.core import paginator
from django.core.mail import send_mail, EmailMessage
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.http import HttpResponse, FileResponse, Http404
from django.shortcuts import render, redirect, reverse

from antiguos_alumnos_tfg.settings import MEDIA_URL, MEDIA_ROOT
import gestionBD.models as modelos
import gestionBD.forms as formularios

import math
import twitter
import re


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


def enviarCorreoApuntarseActividad(emailUsuario, tituloActividad):
    asunto = "Apuntarse a una actividad"
    cuerpo = "Le enviamos este correo para informarle de que se acaba de apuntar a una actividad de la asociación. La actividad a la que se ha apuntado es " + tituloActividad
    emisor = settings.EMAIL_HOST_USER
    send_mail(asunto, cuerpo, emisor, [emailUsuario], fail_silently=False, )


def enviarCorreoApuntarseListaEspera(emailUsuario, tituloActividad):
    asunto = "Apuntarse en la lista de espera"
    cuerpo = "Le enviamos este correo para informarle de que se acaba de apuntar a la lista de espera de la actividad " + tituloActividad + ". En cuanto haya una plaza disponible se le apuntará automáticamente."
    emisor = settings.EMAIL_HOST_USER
    send_mail(asunto, cuerpo, emisor, [emailUsuario], fail_silently=False, )


def enviarCorreoApuntarseActividadAutomaticamente(emailUsuario, tituloActividad):
    asunto = "Apuntarse a una actividad"
    cuerpo = "Le enviamos este correo para informarle de que se le ha apuntado automáticamente a una actividad ya que estaba el primero en la lista de espera y se ha quedado una plaza libre. La actividad en cuestión es " + tituloActividad
    emisor = settings.EMAIL_HOST_USER
    send_mail(asunto, cuerpo, emisor, [emailUsuario], fail_silently=False, )


def actividad(request, titulo):
    contexto = {}
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    actividadBD = modelos.Actividad.objects.get(titulo = titulo)
    contexto['actividad'] = actividadBD
    plazasTotal = actividadBD.numeroPlazas
    plazasOcupadas = modelos.UsuarioActividad.objects.filter(actividad = actividadBD).count()
    plazasLibres = plazasTotal - plazasOcupadas
    hayPlazasLibres = False
    if(plazasLibres > 0):
        hayPlazasLibres = True
    contexto['plazasLibres'] = plazasLibres
    contexto['hayPlazasLibres'] = hayPlazasLibres
    if(usuario is not None):
        usuarioBD = modelos.Usuario.objects.get(usuario = usuario)
        usuarioActividad = modelos.UsuarioActividad.objects.filter(usuario = usuarioBD, actividad = actividadBD).count()
        listaEsperaUsuarioActividad = modelos.ListaEsperaUsuarioActividad.objects.filter(usuario = usuarioBD, actividad = actividadBD).count()
        apuntado = False
        apuntadoListaEspera = False
        if(usuarioActividad > 0):
            apuntado = True
        if(listaEsperaUsuarioActividad > 0):
            apuntadoListaEspera = True
        contexto['apuntado'] = apuntado
        contexto['apuntadoListaEspera'] = apuntadoListaEspera
    if(request.method == 'POST' and inicioSesion):
        if('apuntarseActividad' in request.POST):
            vecesApuntado = modelos.UsuarioActividad.objects.filter(usuario = usuarioBD, actividad = actividadBD).count()
            if(vecesApuntado == 0):
                usuarioActividad = modelos.UsuarioActividad(usuario = usuarioBD, actividad = actividadBD)
                usuarioActividad.save()
                enviarCorreoApuntarseActividad(str(usuarioBD.email), str(actividadBD.titulo))
                return redirect('actividad', titulo = titulo)
            else:
                return redirect('actividad', titulo = titulo)
        elif('borrarseActividad' in request.POST):
            modelos.UsuarioActividad.objects.filter(usuario = usuarioBD, actividad = actividadBD).delete()
            primerUsuarioListaEspera = modelos.ListaEsperaUsuarioActividad.objects.filter(actividad = actividadBD).order_by('fecha')[0]
            usuarioListaEspera = modelos.ListaEsperaUsuarioActividad.objects.filter(usuario = primerUsuarioListaEspera.usuario, actividad = primerUsuarioListaEspera.actividad)
            usuarioActividad = modelos.UsuarioActividad(usuario = primerUsuarioListaEspera.usuario, actividad = actividadBD)
            usuarioActividad.save()
            usuarioListaEspera.delete()
            enviarCorreoApuntarseActividadAutomaticamente(str(primerUsuarioListaEspera.usuario.email), str(actividadBD))
            return redirect('actividad', titulo = titulo)
        elif('botonApuntarseListaEspera' in request.POST):
            listaEsperaUsuarioActividad = modelos.ListaEsperaUsuarioActividad(usuario = usuarioBD, actividad = actividadBD)
            listaEsperaUsuarioActividad.save()
            enviarCorreoApuntarseListaEspera(str(usuarioBD.email), str(actividadBD.titulo))
            return redirect('actividad', titulo = titulo)
    contexto['MEDIA_URL'] = MEDIA_URL
    lineas = actividadBD.descripcion.splitlines()
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


def misActividades(request):
    contexto = {}
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    usuarioBD = modelos.Usuario.objects.get(usuario = usuario)
    actividades_apuntado = modelos.UsuarioActividad.objects.filter(usuario = usuarioBD).order_by('-actividad__fecha')
    contexto['actividades_apuntado'] = actividades_apuntado
    return render(request, "misActividades.html", contexto)


def perfil(request):
    contexto = {}
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion

    editarNombre = False
    editarApellidos = False
    editarComunicaciones = False
    editarCuentaBancaria = False
    editarEmail = False
    editarTelefono = False
    editarDireccionPostal = False
    editarEmpresa = False
    editarContraseña = False
    errores = []
    if(request.method == 'POST'):
        # Editar el nombre:
        if('editarNombrePerfil.x' in request.POST):
            editarNombre = True
        elif('guardarNombrePerfil.x' in request.POST):
            nuevoNombre = request.POST['inputNuevoNombre']
            if(nuevoNombre == ''):
                errores.append('Debe introducir un nombre')
            else:
                modelos.Usuario.objects.filter(usuario = usuario).update(nombre = nuevoNombre)
                editarNombre = False
                errores.clear()
        elif('cancelarNombrePerfil.x' in request.POST):
            editarNombre = False
        # Editar los apellidos:
        elif('editarApellidosPerfil.x' in request.POST):
            editarApellidos = True
        elif('guardarApellidosPerfil.x' in request.POST):
            nuevosApellidos = request.POST['inputNuevosApellidos']
            if(nuevosApellidos == ''):
                errores.append('Debe introducir unos apellidos')
            else:
                modelos.Usuario.objects.filter(usuario = usuario).update(apellidos = nuevosApellidos)
                editarApellidos = False
                errores.clear()
        elif('cancelarApellidosPerfil.x' in request.POST):
            editarApellidos = False
        # Editar la cuenta bancaria:
        elif('editarCuentaBancariaPerfil.x' in request.POST):
            editarCuentaBancaria = True
        elif('guardarCuentaBancariaPerfil.x' in request.POST):
            nuevaCuentaBancaria = request.POST['inputNuevaCuentaBancaria']
            if(nuevaCuentaBancaria == ''):
                errores.append('Debe introducir una cuenta bancaria')
            elif(not nuevaCuentaBancaria.startswith('ES')):
                errores.append('La cuenta bancaria debe empezar por ES')
            else:
                modelos.Usuario.objects.filter(usuario = usuario).update(cuentaBancaria = nuevaCuentaBancaria)
                editarCuentaBancaria = False
                errores.clear()
        elif('cancelarCuentaBancariaPerfil.x' in request.POST):
            editarCuentaBancaria = False
        # Editar el email:
        elif('editarEmailPerfil.x' in request.POST):
            editarEmail = True
        elif('guardarEmailPerfil.x' in request.POST):
            nuevoEmail = request.POST['inputNuevoEmail']
            if(nuevoEmail == ''):
                errores.append('Introduzca el nuevo email')
            elif('@' not in nuevoEmail):
                errores.append('Introduzca un formato de email válido')
            else:
                modelos.Usuario.objects.filter(usuario = usuario).update(email = nuevoEmail)
                editarEmail = False
                errores.clear()
        elif('cancelarEmailPerfil.x' in request.POST):
            editarEmail = False
        # Editar el telefono:
        elif('editarTelefonoPerfil.x' in request.POST):
            editarTelefono = True
        elif('guardarTelefonoPerfil.x' in request.POST):
            nuevoTelefono = request.POST['inputNuevoTelefono']
            if(nuevoTelefono == ''):
                errores.append('Introduzca el nuevo teléfono')
            elif((not nuevoTelefono.startswith('6')) and (not nuevoTelefono.startswith('7'))):
                errores.append('El teléfono debe empezar por 6 o por 7')
            else:
                modelos.Usuario.objects.filter(usuario = usuario).update(telefono = nuevoTelefono)
                editarTelefono = False
                errores.clear()
        elif('cancelarTelefonoPerfil.x' in request.POST):
            editarDireccionPostal = False
        # Editar la dirección
        elif('editarDireccionPostalPerfil.x' in request.POST):
            editarDireccionPostal = True
        elif('guardarDireccionPostalPerfil.x' in request.POST):
            nuevaDireccionPostal = request.POST['inputNuevaDireccionPostal']
            if(nuevaDireccionPostal == ''):
                errores.append('Introduce la nueva dirección postal')
            else:
                modelos.Usuario.objects.filter(usuario = usuario).update(direccionPostal = nuevaDireccionPostal)
                editarDireccionPostal = False
                errores.clear()
        elif('cancelarDireccionPostalPerfil.x' in request.POST):
            editarTelefono = False
        # Editar empresa:
        if('editarEmpresaPerfil.x' in request.POST):
            editarEmpresa = True
        elif('guardarEmpresaPerfil.x' in request.POST):
            nuevaEmpresa = request.POST['inputNuevaEmpresa']
            if(nuevaEmpresa == ''):
                errores.append('Introduce la nueva empresa')
            else:
                modelos.Usuario.objects.filter(usuario = usuario).update(empresa = nuevaEmpresa)
                editarEmpresa = False
                errores.clear()
        elif('cancelarEmpresaPerfil.x' in request.POST):
            editarEmpresa = False
        # Editar las comunicaciones:
        elif('editarComunicacionesPerfil.x' in request.POST):
            editarComunicaciones = True
        elif('guardarComunicacionesPerfil.x' in request.POST):
            if('inputNuevasComunicaciones' in request.POST):
                modelos.Usuario.objects.filter(usuario = usuario).update(comunicaciones = True)
            else:
                modelos.Usuario.objects.filter(usuario = usuario).update(comunicaciones = False)
            editarComunicaciones = False
        elif('cancelarComunicacionesPerfil.x' in request.POST):
            editarComunicaciones = False
        # Editar la contraseña:
        elif('botonCambiarContraseña' in request.POST):
            editarContraseña = True
        elif('guardarNuevaContraseña.x' in request.POST):
            nuevaContraseña = request.POST['inputNuevaContraseña']
            confirmacionContraseña = request.POST['inputConfirmacionContraseña']
            if(nuevaContraseña != confirmacionContraseña):
                errores.append('La nueva contraseña y su confirmación deben coincidir')
            else:
                antiguaContraseña = modelos.Usuario.objects.get(usuario = usuario).contraseña
                contieneMayuscula = re.search("[A-Z]", nuevaContraseña)
                contieneNumero = re.search("[0-9]", nuevaContraseña)
                if(len(nuevaContraseña) < 8):
                    errores.append('La nueva contraseña debe contener más de 8 caracteres')
                elif(nuevaContraseña == antiguaContraseña):
                    errores.append('La nueva contraseña no puede ser igual que la anterior')
                elif(not contieneMayuscula):
                    errores.append('La nueva contraseña debe contener alguna letra mayúscula')
                elif(not contieneNumero):
                    errores.append('La nueva contraseña debe contener algún número')
                else:
                    modelos.Usuario.objects.filter(usuario = usuario).update(contraseña = nuevaContraseña)
                    editarContraseña = False
                    errores.clear()
        elif('cancelarNuevaContraseña.x' in request.POST):
            editarContraseña = False

    contexto['editarNombre'] = editarNombre
    contexto['editarApellidos'] = editarApellidos
    contexto['editarComunicaciones'] = editarComunicaciones
    contexto['editarCuentaBancaria'] = editarCuentaBancaria
    contexto['editarEmail'] = editarEmail
    contexto['editarTelefono'] = editarTelefono
    contexto['editarDireccionPostal'] = editarDireccionPostal
    contexto['editarEmpresa'] = editarEmpresa
    contexto['editarContraseña'] = editarContraseña
    contexto['errores'] = errores
    
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
    texto_tweet = 'Tenemos una nueva actividad para vosotros: ' + titulo
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
    texto_tweet = 'Tenemos una nueva noticia que contaros: ' + titulo
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