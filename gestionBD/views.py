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
from validate_email import validate_email


#from django.db.models import CharField
#from django.db.models.functions import Lower
#CharField.register_lookup(Lower)
#from gestionBD.models import Titulacion, JuntaRectora, TipoActividad, RevistaIngenio, TipoUsuario
#from datetime import datetime

# Create your views here.


def busqueda(request):
    # Creamos el 'contexto' (Diccionario Python) de la vista en donde almacenaremos aquellos elementos que queramos mostrar
    # en la vista
    contexto = {}
    # Guardamos el usuario, si es administrador y si ha iniciado sesión en el contexto
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    if(request.method=='POST'):
        # Si se ha pulsado el botón de buscar guardamos lo que se ha introducido en la búsqueda
        palabra = request.POST.get('buscar')
        if(palabra == ""):
            # Si el usuario no ha introducido ninguna palabra y solo ha pulsado el icono de pulsar declaramos el error para 
            # mostrarlo en la página
            error = "Introduzca una palabra para realizar la búsqueda"
            contexto['error'] = error
        else:
            # Si ha introducido un término buscamos noticias y actividades con lo que se ha introducido
            noticias = modelos.Noticia.objects.filter(titulo__unaccent__icontains=palabra)
            actividades = modelos.Actividad.objects.filter(titulo__unaccent__icontains=palabra)
            # Guardamos en el contexto lo que se ha introducido, y las noticias y actividades encontradas
            contexto['palabra'] = palabra
            contexto['noticias'] = noticias
            contexto['actividades'] = actividades
    # Renderizamos la página de búsqueda con los resultados
    return render(request, "busqueda.html", contexto)


def inicio(request):
    contexto = {}
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    actividades = modelos.Actividad.objects.order_by('-fecha')[:3]
    ofertas_empleo = modelos.OfertaEmpleo.objects.order_by('-fecha')[:3]
    noticias = modelos.Noticia.objects.values_list('titulo').order_by('-fecha')
    ultimaRevistaIngenio = modelos.RevistaIngenio.objects.order_by('-numero')[0]
    elementosCarrusel = [ultimaRevistaIngenio] + [n[0] for n in noticias]
    contexto['elementosCarrusel'] = elementosCarrusel
    actividades_ofertas = []
    for i in range(3):
        actividades_ofertas.append(actividades[i])
        actividades_ofertas.append(ofertas_empleo[i])
    contexto['actividades_ofertas'] = actividades_ofertas
    contexto['MEDIA_URL'] = MEDIA_URL
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
    # Creamos el 'contexto' (Diccionario Python) de la vista en donde almacenaremos aquellos elementos que queramos mostrar
    # en la vista
    contexto = {}
    # Guardamos el usuario, si es administrador y si ha iniciado sesión en el contexto
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    # Consultamos las actividades a la base de datos ordenadas de más recientes a más antiguas y las guardamos en una variable
    actividades = modelos.Actividad.objects.order_by('-fecha')
    # Determinamos el número de actividades por página
    objetos_paginacion = 5
    # Paginamos las actividades por la cantidad determinada anteriormente
    paginator = Paginator(actividades, objetos_paginacion)
    # Nos quedamos con la página en la que estamos y guardamos en el contexto la página. La página puede ser None ya que la
    # primera vez que entramos se ven las actividades de la primera página pero no hay un valor de página
    pagina = request.GET.get('page')
    if(pagina is not None):
        contexto['paginaActual'] = int(pagina)
    # Nos quedamos con las actividades de la página en la que estamos y lo guardamos en el contexto
    actividades_paginadas = paginator.get_page(pagina)
    contexto['actividades_paginadas'] = actividades_paginadas
    # Nos quedamos con el número de páginas en total
    numero_paginas = math.ceil(actividades.count()/objetos_paginacion)
    # Creamos una lista con el número de páginas que hay y lo guardamos en el contexto
    paginas = [i for i in range(1, numero_paginas+1)]
    contexto['paginas'] = paginas
    # Creamos un diccionario que tiene un índice numérico de clave y el título de una actividad como valor para poder
    # navegar entre las actividades cuando pulsemos anterior y siguiente y lo guardamos en la sesión para acceder a ello
    # en todo momento
    diccionarioActividades = {}
    for i in range(0, len(actividades)):
        diccionarioActividades[i] = str(actividades[i].titulo)
    request.session['diccionarioActividades'] = diccionarioActividades
    # Para hacer la paginación vemos si la página que estamos viendo es de las primeras, de las intermedias o de las finales
    # a fin de dar un formato u otro a la hora de mostrar la página en cada uno de esos intervalos
    tipoInicio = False
    tipoMedio = False
    tipoFin = False
    # Si hay más de 5 páginas y una difencia de más de 2 páginas con la quinta haremos paginación. En caso mostramos 
    # todas las páginas
    if(numero_paginas > 5 and (numero_paginas - 5) > 2):
        # Si estamos en una página inferior a 5 o es la primera vez que entramos en las actividades consideramos 
        # que estamos al inicio de las páginas
        if((pagina is None) or (pagina is not None and int(pagina) < 5)):
            # Marcamos que estamos al inicio, creamos un lista con el rango de las páginas y lo guardamos en el contexto
            tipoInicio = True
            rango_inicio = [i for i in range(1, 6)]
            contexto['rango_inicio'] = rango_inicio
        # Si estamos en una página mayor a 5 y quedan más de 3 páginas por ver consideramos que estamos en una zona media
        # de las páginas
        elif(pagina is not None and int(pagina) >= 5 and int(pagina) < numero_paginas-3):
            # Marcamos que estamos en la zona media, creamos un lista con el rango de las páginas y lo guardamos 
            # en el contexto
            tipoMedio = True
            rango_medio = [i for i in range(int(pagina)-1, int(pagina)+2)]
            contexto['rango_medio'] = rango_medio
        # Si estamos en una de las 4 últimas páginas consideramos que estamos en la zona final de las páginas
        elif(pagina is not None and int(pagina) >= numero_paginas-3):
            # Marcamos que estamos en la zona final, creamos un lista con el rango de las páginas y lo guardamos 
            # en el contexto
            tipoFin = True
            rango_fin = [i for i in range(numero_paginas-3, numero_paginas+1)]
            contexto['rango_fin'] = rango_fin
            # Nos quedamos con la página de la mitad entre la primera del rango final y la primera página. Así hay un enlace
            # a una página intermedia
            pagina_media = math.ceil((rango_fin[0]+1)/2)
            contexto['pagina_media'] = pagina_media
    # Guardamos en el contexto las variables para saber en que zona de las páginas estamos
    contexto['tipoInicio'] = tipoInicio
    contexto['tipoMedio'] = tipoMedio
    contexto['tipoFin'] = tipoFin
    # Renderizamos la página de las actividades paginadas
    return render(request, "actividades.html", contexto)


def enviarCorreoApuntarseActividad(emailUsuario, tituloActividad):
    asunto = "Apuntarse a una actividad"
    cuerpo = "Le enviamos este correo para informarle de que se acaba de apuntar a una actividad de la asociación. La actividad a la que se ha apuntado es " + tituloActividad
    emisor = settings.EMAIL_HOST_USER
    send_mail(asunto, cuerpo, emisor, [emailUsuario], fail_silently=False, )


def enviarCorreoBorrarseActividad(emailUsuario, tituloActividad):
    asunto = "Borrarse de una actividad"
    cuerpo = "Le enviamos este correo para informarle de que se acaba de borrar de una actividad de la asociación. La actividad de la que se ha borrado es " + tituloActividad
    emisor = settings.EMAIL_HOST_USER
    send_mail(asunto, cuerpo, emisor, [emailUsuario], fail_silently=False, )


def enviarCorreoApuntarseListaEspera(emailUsuario, tituloActividad):
    asunto = "Apuntarse en la lista de espera"
    cuerpo = "Le enviamos este correo para informarle de que se acaba de apuntar a la lista de espera de la actividad " + tituloActividad + ". En cuanto haya una plaza disponible se le apuntará automáticamente."
    emisor = settings.EMAIL_HOST_USER
    send_mail(asunto, cuerpo, emisor, [emailUsuario], fail_silently=False, )


def enviarCorreoBorrarseListaEspera(emailUsuario, tituloActividad):
    asunto = "Borrarse de la lista de espera"
    cuerpo = "Le enviamos este correo para informarle de que se acaba de borrar de la lista de espera de la actividad " + tituloActividad
    emisor = settings.EMAIL_HOST_USER
    send_mail(asunto, cuerpo, emisor, [emailUsuario], fail_silently=False, )


def enviarCorreoApuntarseActividadAutomaticamente(emailUsuario, tituloActividad):
    asunto = "Apuntarse a una actividad"
    cuerpo = "Le enviamos este correo para informarle de que se le ha apuntado automáticamente a una actividad ya que estaba el primero en la lista de espera y se ha quedado una plaza libre. La actividad en cuestión es " + tituloActividad
    emisor = settings.EMAIL_HOST_USER
    send_mail(asunto, cuerpo, emisor, [emailUsuario], fail_silently=False, )


def actividad(request, titulo):
    # Creamos el 'contexto' (Diccionario Python) de la vista en donde almacenaremos aquellos elementos que queramos mostrar
    # en la vista
    contexto = {}
    # Guardamos el usuario, si es administrador y si ha iniciado sesión en el contexto
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    # Creamos la actividad consultando a la base de datos con el título de la actividad y la guardamos en el contexto
    actividadBD = modelos.Actividad.objects.get(titulo = titulo)
    contexto['actividad'] = actividadBD
    # Nos quedamos con datos de interés de la actividad que serán necesarios para la vista como las plazas totales, 
    # las ocupadas y las plazas libres
    plazasTotal = actividadBD.numeroPlazas
    plazasOcupadas = modelos.UsuarioActividad.objects.filter(actividad = actividadBD).count()
    plazasLibres = plazasTotal - plazasOcupadas
    # Decimos que no hay plazas libres
    # Guardamos las plazas disponibles en el contexto
    contexto['plazasLibres'] = plazasLibres
    if(usuario is not None):
        # Si se ha iniciado sesión
        # Creamos el usuario consultando la base de datos con el usuario que se ha iniciado sesión
        usuarioBD = modelos.Usuario.objects.get(usuario = usuario)
        # Consultamos si el usuario se ha apuntado a la actividad que se está visitando
        usuarioActividad = modelos.UsuarioActividad.objects.filter(usuario = usuarioBD, actividad = actividadBD).count()
        # Consultamos si el usuario se ha apuntado a la lista de esperada de la actividad que se está visitando
        listaEsperaUsuarioActividad = modelos.ListaEsperaUsuarioActividad.objects.filter(usuario = usuarioBD, actividad = actividadBD).count()
        # Decimos inicialmente que no está apuntado a la actividad ni a la lista de espera
        apuntado = False
        apuntadoListaEspera = False
        if(usuarioActividad > 0):
            # Si se ha apuntado a la actividad decimos que lo ha hecho
            apuntado = True
        if(listaEsperaUsuarioActividad > 0):
            # Si se ha apuntado a la lista de espera de la actividad decimos que lo ha hecho
            apuntadoListaEspera = True
        # Guardamos en el contexto donde está apuntado el usuario
        contexto['apuntado'] = apuntado
        contexto['apuntadoListaEspera'] = apuntadoListaEspera
    if(request.method == 'POST' and inicioSesion):
        # Si se ha pulsado en un botón de apuntarse o borrarse de una actividad, apuntarse a la lista de espera y 
        # se ha iniciado sesión
        if('apuntarseActividad' in request.POST):
            # Si ha pulsado en el botón para apuntarse a la actividad consultamos si se ha apuntado
            vecesApuntado = modelos.UsuarioActividad.objects.filter(usuario = usuarioBD, actividad = actividadBD).count()
            if(vecesApuntado == 0):
                # Si no se ha apuntado a la actividad le apuntamos
                usuarioActividad = modelos.UsuarioActividad(usuario = usuarioBD, actividad = actividadBD)
                usuarioActividad.save()
                # Enviamos un email para notificárselo
                enviarCorreoApuntarseActividad(str(usuarioBD.email), str(actividadBD.titulo))
                # Le redirigimos a la página de la actividad otra vez y ya le aparecerá que está apuntado
                return redirect('actividad', titulo = titulo)
            else:
                # Si ya está apuntado le redirigimos a la página de la actividad otra vez
                return redirect('actividad', titulo = titulo)
        elif('borrarseActividad' in request.POST):
            # Si ha pulsado en el botónd de borrarse de la actividad borramos al usario de la actividad y le enviamos un email 
            # para informale
            modelos.UsuarioActividad.objects.filter(usuario = usuarioBD, actividad = actividadBD).delete()
            enviarCorreoBorrarseActividad(str(usuarioBD.email), str(actividadBD.titulo))
            # Vemos el número de usuarios apuntados a la lista de espera
            numUsuariosListaEspera = modelos.ListaEsperaUsuarioActividad.objects.filter(actividad = actividadBD).count()
            if(numUsuariosListaEspera > 0):
                # Si hay usuarios apuntados a la lista de espera vemos quien es el primer usuario apuntado a la lista 
                # de espera y nos quedamos con ese usuario 
                primerUsuarioListaEspera = modelos.ListaEsperaUsuarioActividad.objects.filter(actividad = actividadBD).order_by('fecha')[0]
                usuarioListaEspera = modelos.ListaEsperaUsuarioActividad.objects.filter(usuario = primerUsuarioListaEspera.usuario, actividad = primerUsuarioListaEspera.actividad)
                # Apuntamos al usuario a la actividad, le borramos de la lista de espera y le mandamos un email para comunicárselo
                usuarioActividad = modelos.UsuarioActividad(usuario = primerUsuarioListaEspera.usuario, actividad = actividadBD)
                usuarioActividad.save()
                usuarioListaEspera.delete()
                enviarCorreoApuntarseActividadAutomaticamente(str(primerUsuarioListaEspera.usuario.email), str(actividadBD))
            # Redirigimos al usuario que se ha borrado de la actividad a la página de la actividad para que vea que se ha borrado
            # correctamente de la actividad
            return redirect('actividad', titulo = titulo)
        elif('botonApuntarseListaEspera' in request.POST):
            # Si se ha pulsado en el botón de apuntarse a la lista de espera le apuntamos a la lista de espera
            listaEsperaUsuarioActividad = modelos.ListaEsperaUsuarioActividad(usuario = usuarioBD, actividad = actividadBD)
            listaEsperaUsuarioActividad.save()
            # Le enviamos un email para notificárselo
            enviarCorreoApuntarseListaEspera(str(usuarioBD.email), str(actividadBD.titulo))
            # Le redirigimos a la página de la actividad para que vea que ha sido apuntado a la lista de espera
            return redirect('actividad', titulo = titulo)
        elif('botonBorrarseListaEspera' in request.POST):
            # Si se ha pulsado el botón de borrarse de la lista de espera de la actividad le borramos
            modelos.ListaEsperaUsuarioActividad.objects.filter(usuario = usuarioBD, actividad = actividadBD).delete()
            # Le enviamos un email para notificárselo
            enviarCorreoBorrarseListaEspera(str(usuarioBD.email), str(actividadBD.titulo))
            # Le redirigimos a la página de la actividad para que vea que ha sido borrado de la lista de espera
            return redirect('actividad', titulo = titulo)
    # Guardamos en el contexto la url de los archivos multimedia por si es necesario acceder a alguno de ellos
    contexto['MEDIA_URL'] = MEDIA_URL
    # Guardamos en el contexto los párrafos de la descripción de la actividad para mostrarlos en la página de la actividad
    lineas = actividadBD.descripcion.splitlines()
    contexto['lineas'] = lineas
    # Recuperamos de la sesión el diccionario con un índice numérico y las actividades para hacer los enlaces de anterior 
    # y siguiente
    if(not request.session.get('diccionarioActividades')):
        # Si no está en la sesión lo creamos de nuevo
        diccionarioActividades = {}
        actividades = modelos.Actividad.objects.order_by('-fecha')
        for i in range(0, len(actividades)):
            diccionarioActividades[i] = str(actividades[i].titulo)
    else:
        # Si está en la sesión lo recuperamos
        diccionarioActividades = request.session.get('diccionarioActividades')
    # Nos quedamos con el índice numérico de la actividad en la que estamos recorriendo el diccionario
    actividadActual = None
    for c, v in diccionarioActividades.items():
        if(v == titulo):
            actividadActual = int(c)
            break
    # Nos quedamos con el número total de actividades
    totalActividades = len(diccionarioActividades.keys())
    if(actividadActual == totalActividades-1):
        # Si estamos en la última actividad decimos que no hay siguiente y lo guardamos en el contexto
        haySiguiente = False
        contexto['haySiguiente'] = haySiguiente
    else:
        # Si no estamos en la última actividad hay siguiente
        # Nos quedamos con el ínidice de la siguiente, consultamos el título de la siguiente y lo guardamos en el contexto
        actividadSiguiente = actividadActual+1
        tituloSiguiente = diccionarioActividades.get(str(actividadSiguiente))
        contexto['tituloSiguiente'] = tituloSiguiente
        # Decimos que hay siguiente y lo guardamos en el contexto
        haySiguiente = True
        contexto['haySiguiente'] = haySiguiente
    if(actividadActual == 0):
        # Si estamos en la primera actividad decimos que no hay una actividad anterior y lo guardamos en el contexto
        hayAnterior = False
        contexto['hayAnterior'] = hayAnterior
    else:
        # Si no estamos en la primera actividad hay anterior
        # Nos quedamos el ínidice de la anterior, consultamos el título de la anterior y lo guardamos en el contexto
        actividadAnterior = actividadActual-1
        tituloAnterior = diccionarioActividades.get(str(actividadAnterior))
        contexto['tituloAnterior'] = tituloAnterior
        # Decimos que hay anterior y lo guardamos en el contexto
        hayAnterior = True
        contexto['hayAnterior'] = hayAnterior
    # Renderizamos la página de la actividad
    return render(request, "actividad.html", contexto)


def noticias(request):
    # Creamos el 'contexto' (Diccionario Python) de la vista en donde almacenaremos aquellos elementos que queramos mostrar
    # en la vista
    contexto = {}
    # Guardamos el usuario, si es administrador y si ha iniciado sesión en el contexto
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    # Consultamos las noticias a la base de datos ordenadas de más recientes a más antiguas y las guardamos en una variable
    noticias = modelos.Noticia.objects.order_by('-fecha')
    # Determinamos el número de actividades por página
    objetos_paginacion = 5
    # Paginamos las noticias por la cantidad determinada anteriormente
    paginator = Paginator(noticias, objetos_paginacion)
    # Nos quedamos con la página en la que estamos y guardamos en el contexto la página. La página puede ser None ya que la
    # primera vez que entramos se ven las noticias de la primera página pero no hay un valor de página
    pagina = request.GET.get('page')
    if(pagina is not None):
        contexto['paginaActual'] = int(pagina)
    # Nos quedamos con las noticias de la página en la que estamos y lo guardamos en el contexto
    noticias_paginadas = paginator.get_page(pagina)
    contexto['noticias_paginadas'] = noticias_paginadas
    # Nos quedamos con el número de páginas en total
    numero_paginas = math.ceil(noticias.count()/objetos_paginacion)
    # Creamos una lista con el número de páginas que hay y lo guardamos en el contexto
    paginas = [i for i in range(1, numero_paginas+1)]
    contexto['paginas'] = paginas
    # Para hacer la paginación vemos si la página que estamos viendo es de las primeras, de las intermedias o de las finales
    # a fin de dar un formato u otro a la hora de mostrar la página en cada uno de esos intervalos
    tipoInicio = False
    tipoMedio = False
    tipoFin = False
    # Si hay más de 5 páginas y una difencia de más de 2 páginas con la quinta haremos paginación. En caso mostramos 
    # todas las páginas
    if(numero_paginas > 5 and (numero_paginas - 5) > 2):
        # Si estamos en una página inferior a 5 o es la primera vez que entramos en las actividades consideramos 
        # que estamos al inicio de las páginas
        if((pagina is None) or (pagina is not None and int(pagina) < 5)):
            # Marcamos que estamos al inicio, creamos un lista con el rango de las páginas y lo guardamos en el contexto
            tipoInicio = True
            rango_inicio = [i for i in range(1, 6)]
            contexto['rango_inicio'] = rango_inicio
        # Si estamos en una página mayor a 5 y quedan más de 3 páginas por ver consideramos que estamos en una zona media
        # de las páginas
        elif(pagina is not None and int(pagina) >= 5 and int(pagina) < numero_paginas-3):
            # Marcamos que estamos en la zona media, creamos un lista con el rango de las páginas y lo guardamos 
            # en el contexto
            tipoMedio = True
            rango_medio = [i for i in range(int(pagina)-1, int(pagina)+2)]
            contexto['rango_medio'] = rango_medio
        # Si estamos en una de las 4 últimas páginas consideramos que estamos en la zona final de las páginas
        elif(pagina is not None and int(pagina) >= numero_paginas-3):
            # Marcamos que estamos en la zona final, creamos un lista con el rango de las páginas y lo guardamos 
            # en el contexto
            tipoFin = True
            rango_fin = [i for i in range(numero_paginas-3, numero_paginas+1)]
            contexto['rango_fin'] = rango_fin
            # Nos quedamos con la página de la mitad entre la primera del rango final y la primera página. Así hay un enlace
            # a una página intermedia
            pagina_media = math.ceil((rango_fin[0]+1)/2)
            contexto['pagina_media'] = pagina_media
    # Guardamos en el contexto las variables para saber en que zona de las páginas estamos
    contexto['tipoInicio'] = tipoInicio
    contexto['tipoMedio'] = tipoMedio
    contexto['tipoFin'] = tipoFin
    # Renderizamos la página de las noticias paginadas
    return render(request, "noticias.html", contexto)


def noticia(request, titulo):
    # Creamos el 'contexto' (Diccionario Python) de la vista en donde almacenaremos aquellos elementos que queramos mostrar
    # en la vista
    contexto = {}
    # Guardamos el usuario, si es administrador y si ha iniciado sesión en el contexto
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    # Consultamos la noticia que el usuario desea ver y la guardamos en el contexto
    noticia = modelos.Noticia.objects.get(titulo = titulo)
    contexto['noticia'] = noticia
    # Separamos los párrafos del texto de la noticia para mostrarlos y lo guardamos en el contexto
    lineas = noticia.texto.splitlines()
    contexto['lineas'] = lineas
    # Guardamos en el contexto la url de los archivos multimedia por si es necesario consultar alguno en la vista
    contexto['MEDIA_URL'] = MEDIA_URL
    # Renderizamos la página de la noticia
    return render(request, "noticia.html", contexto)


def empleo(request):
    # Creamos el 'contexto' (Diccionario Python) de la vista en donde almacenaremos aquellos elementos que queramos mostrar
    # en la vista
    contexto = {}
    # Guardamos el usuario, si es administrador y si ha iniciado sesión en el contexto
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    # Consultamos las ofertas de empleo a la base de datos ordenadas de más recientes a más antiguas y las guardamos en 
    # una variable
    ofertasEmpleo = modelos.OfertaEmpleo.objects.order_by('-fecha')
    # Determinamos el número de ofertas de empleo por página
    objetos_paginacion = 5
    # Paginamos las actividades por la cantidad determinada anteriormente
    paginator = Paginator(ofertasEmpleo, objetos_paginacion)
    # Nos quedamos con la página en la que estamos y guardamos en el contexto la página. La página puede ser None ya que la
    # primera vez que entramos se ven las actividades de la primera página pero no hay un valor de página
    pagina = request.GET.get('page')
    if(pagina is not None):
        contexto['paginaActual'] = int(pagina)
    # Nos quedamos con las ofertas de empleo de la página en la que estamos y lo guardamos en el contexto
    ofertasEmpleo_paginadas = paginator.get_page(pagina)
    contexto['ofertasEmpleo_paginadas'] = ofertasEmpleo_paginadas
    # Nos quedamos con el número de páginas en total
    numero_paginas = math.ceil(ofertasEmpleo.count()/objetos_paginacion)
    # Creamos una lista con el número de páginas que hay y lo guardamos en el contexto
    paginas = [i for i in range(1, numero_paginas+1)]
    contexto['paginas'] = paginas
    # Para hacer la paginación vemos si la página que estamos viendo es de las primeras, de las intermedias o de las finales
    # a fin de dar un formato u otro a la hora de mostrar la página en cada uno de esos intervalos
    tipoInicio = False
    tipoMedio = False
    tipoFin = False
    # Si hay más de 5 páginas y una difencia de más de 2 páginas con la quinta haremos paginación. En caso mostramos 
    # todas las páginas
    if(numero_paginas > 5 and (numero_paginas - 5) > 2):
        # Si estamos en una página inferior a 5 o es la primera vez que entramos en las actividades consideramos 
        # que estamos al inicio de las páginas
        if((pagina is None) or (pagina is not None and int(pagina) < 5)):
            # Marcamos que estamos al inicio, creamos un lista con el rango de las páginas y lo guardamos en el contexto
            tipoInicio = True
            rango_inicio = [i for i in range(1, 6)]
            contexto['rango_inicio'] = rango_inicio
        # Si estamos en una página mayor a 5 y quedan más de 3 páginas por ver consideramos que estamos en una zona media
        # de las páginas
        elif(pagina is not None and int(pagina) >= 5 and int(pagina) < numero_paginas-3):
            # Marcamos que estamos en la zona media, creamos un lista con el rango de las páginas y lo guardamos 
            # en el contexto
            tipoMedio = True
            rango_medio = [i for i in range(int(pagina)-1, int(pagina)+2)]
            contexto['rango_medio'] = rango_medio
        # Si estamos en una de las 4 últimas páginas consideramos que estamos en la zona final de las páginas
        elif(pagina is not None and int(pagina) >= numero_paginas-3):
            # Marcamos que estamos en la zona final, creamos un lista con el rango de las páginas y lo guardamos 
            # en el contexto
            tipoFin = True
            rango_fin = [i for i in range(numero_paginas-3, numero_paginas+1)]
            contexto['rango_fin'] = rango_fin
            # Nos quedamos con la página de la mitad entre la primera del rango final y la primera página. Así hay un enlace
            # a una página intermedia
            pagina_media = math.ceil((rango_fin[0]+1)/2)
            contexto['pagina_media'] = pagina_media
    # Guardamos en el contexto las variables para saber en que zona de las páginas estamos
    contexto['tipoInicio'] = tipoInicio
    contexto['tipoMedio'] = tipoMedio
    contexto['tipoFin'] = tipoFin
    # Renderizamos la página de las ofertas de empleo paginadas
    return render(request, "empleo.html", contexto)


def ofertaEmpleo(request, titulo):
    # Creamos el 'contexto' (Diccionario Python) de la vista en donde almacenaremos aquellos elementos que queramos mostrar
    # en la vista
    contexto = {}
    # Guardamos el usuario, si es administrador y si ha iniciado sesión en el contexto
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    # Consultamos la oferta de empleo que el usuario desea ver y la guardamos en el contexto
    ofertaEmpleo = modelos.OfertaEmpleo.objects.get(titulo = titulo)
    contexto['ofertaEmpleo'] = ofertaEmpleo
    # Separamos los párrafos del texto de la oferta de empleo para mostrarlos y lo guardamos en el contexto
    lineas = ofertaEmpleo.texto.splitlines()
    contexto['lineas'] = lineas
    # Guardamos en el contexto la url de los archivos multimedia por si es necesario consultar alguno en la vista
    contexto['MEDIA_URL'] = MEDIA_URL
    # Renderizamos la página de la oferta de empleo
    return render(request, "ofertaEmpleo.html", contexto)


def acuerdosEmpresas(request):
    # Creamos el 'contexto' (Diccionario Python) de la vista en donde almacenaremos aquellos elementos que queramos mostrar
    # en la vista
    contexto = {}
    # Guardamos el usuario, si es administrador y si ha iniciado sesión en el contexto
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    # Consultamos los acuerdos con empresas a la base de datos y los guardamos en una variable. Esa variable la guardamos a
    # a su vez en el contexto
    acuerdos = modelos.AcuerdosEmpresas.objects.all()
    contexto['acuerdos'] = acuerdos
    # Guardamos en el contexto la url de los archivos multimedia por si es necesario consultar alguno en la vista
    contexto['MEDIA_URL'] = MEDIA_URL
    # Renderizamos la página de los acuerdos con empresas
    return render(request, "acuerdosEmpresas.html", contexto)


def acuerdoEmpresa(request, nombre):
    # Creamos el 'contexto' (Diccionario Python) de la vista en donde almacenaremos aquellos elementos que queramos mostrar
    # en la vista
    contexto = {}
    # Guardamos el usuario, si es administrador y si ha iniciado sesión en el contexto
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    # Consultamos el acuerdo con empresa que el usuario desea ver y la guardamos en el contexto
    acuerdo = modelos.AcuerdosEmpresas.objects.get(nombre = nombre)
    contexto['acuerdo'] = acuerdo
    # Separamos los párrafos del texto del acuerdo con empresa para mostrarlos y lo guardamos en el contexto
    lineas = acuerdo.texto.splitlines()
    contexto['lineas'] = lineas
    # Guardamos en el contexto la url de los archivos multimedia por si es necesario consultar alguno en la vista
    contexto['MEDIA_URL'] = MEDIA_URL
    # Renderizamos la página del acuerdo con empresa
    return render(request, "acuerdoEmpresa.html", contexto)


def revistaIngenio(request):
    # Creamos el 'contexto' (Diccionario Python) de la vista en donde almacenaremos aquellos elementos que queramos mostrar
    # en la vista
    contexto = {}
    # Guardamos el usuario, si es administrador y si ha iniciado sesión en el contexto
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    # Consultamos las revistas almacenadas en la base de datos ordenadas por su número de mayor a menor a fin de mostrar las
    # más recientes primero y las guardamos en el contexto
    revistas = modelos.RevistaIngenio.objects.order_by('-numero')
    contexto['revistas'] = revistas
    # Guardamos el número de revista mayor, pues será la revista más reciente, a fin de destacarla en la vista para 
    # que sea más fácil de ver para los usuarios
    mayorNumero = revistas[0].numero
    contexto['mayorNumero'] = mayorNumero
    # Guardamos en el contexto la url de los archivos multimedia por si es necesario consultar alguno en la vista
    contexto['MEDIA_URL'] = MEDIA_URL
    # Renderizamos la página de la Revista Ingenio
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
    # Creamos el 'contexto' (Diccionario Python) de la vista en donde almacenaremos aquellos elementos que queramos mostrar
    # en la vista
    contexto = {}
    # Guardamos el usuario, si es administrador y si ha iniciado sesión en el contexto
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    # Consultamos los datos del presidente, los formateamos para mostrarlos y los guardamos en el contexto
    datosPresidente = modelos.Usuario.objects.get(juntaRectora = 'Presidente')
    presidente = 'D. ' + datosPresidente.nombre + ' ' + datosPresidente.apellidos
    contexto['presidente'] = presidente
    # Consultamos los datos del vicepresidente, los formateamos para mostrarlos y los guardamos en el contexto
    datosVicepresidente = modelos.Usuario.objects.get(juntaRectora = 'Vicepresidente')
    vicepresidente = 'D. ' + datosVicepresidente.nombre + ' ' + datosVicepresidente.apellidos
    contexto['vicepresidente'] = vicepresidente
    # Consultamos los datos del secretario, los formateamos para mostrarlos y los guardamos en el contexto
    datosSecretario = modelos.Usuario.objects.get(juntaRectora = 'Secretario')
    secretario = 'D. ' + datosSecretario.nombre + ' ' + datosSecretario.apellidos
    contexto['secretario'] = secretario
    # Consultamos los datos del tesorero, los formateamos para mostrarlos y los guardamos en el contexto
    datosTesorero = modelos.Usuario.objects.get(juntaRectora = 'Tesorero')
    tesorero = 'D. ' + datosTesorero.nombre + ' ' + datosTesorero.apellidos
    contexto['tesorero'] = tesorero
    # Consultamos los datos de los vocales, los formateamos para mostrarlos y los guardamos en el contexto
    datosVocales = modelos.Usuario.objects.filter(juntaRectora = 'Vocal')
    vocales = ['D. ' + vocal.nombre + ' ' + vocal.apellidos for vocal in datosVocales]
    contexto['vocales'] = vocales
    # Renderizamos la página de la Junta Rectora
    return render(request, "juntaRectora.html", contexto)


def historia(request):
    contexto = {}
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    return render(request, "historia.html", contexto)


def misActividades(request):
    # Creamos el 'contexto' (Diccionario Python) de la vista en donde almacenaremos aquellos elementos que queramos mostrar
    # en la vista
    contexto = {}
    # Guardamos el usuario, si es administrador y si ha iniciado sesión en el contexto
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    if(usuario is not None):
        # Si hay un usuario con el que se ha iniciado sesión creamos el objeto usuario de la base de datos con el que se ha iniciado sesión
        usuarioBD = modelos.Usuario.objects.get(usuario = usuario)
        # Con el usuario creado anteriormente nos quedamos con las actividades a las que se ha apuntado el usuario consultado
        # la tabla Usuario - Actividad que tiene un usuario y la actividad a la que se ha apuntado. Las ordenamos por fecha,
        # de la más reciente a la más antigua
        actividades_apuntado = modelos.UsuarioActividad.objects.filter(usuario = usuarioBD).order_by('-actividad__fecha')
        # Determinamos el número de actividades por página
        objetos_paginacion = 5
        # Paginamos las actividades por la cantidad determinada anteriormente
        paginator = Paginator(actividades_apuntado, objetos_paginacion)
        # Nos quedamos con la página en la que estamos y guardamos en el contexto la página. La página puede ser None ya que la
        # primera vez que entramos se ven las actividades de la primera página pero no hay un valor de página
        pagina = request.GET.get('page')
        if(pagina is not None):
            contexto['paginaActual'] = int(pagina)
        # Nos quedamos con las actividades de la página en la que estamos y lo guardamos en el contexto
        mis_actividades_paginadas = paginator.get_page(pagina)
        contexto['mis_actividades_paginadas'] = mis_actividades_paginadas
        # Nos quedamos con el número de páginas en total
        numero_paginas = math.ceil(actividades_apuntado.count()/objetos_paginacion)
        # Creamos una lista con el número de páginas que hay y lo guardamos en el contexto
        paginas = [i for i in range(1, numero_paginas+1)]
        contexto['paginas'] = paginas
        # Para hacer la paginación vemos si la página que estamos viendo es de las primeras, de las intermedias o de las finales
        # a fin de dar un formato u otro a la hora de mostrar la página en cada uno de esos intervalos
        tipoInicio = False
        tipoMedio = False
        tipoFin = False
        # Si hay más de 5 páginas y una difencia de más de 2 páginas con la quinta haremos paginación. En caso mostramos 
        # todas las páginas
        if(numero_paginas > 5 and (numero_paginas - 5) > 2):
            # Si estamos en una página inferior a 5 o es la primera vez que entramos en las actividades consideramos 
            # que estamos al inicio de las páginas
            if((pagina is None) or (pagina is not None and int(pagina) < 5)):
                # Marcamos que estamos al inicio, creamos un lista con el rango de las páginas y lo guardamos en el contexto
                tipoInicio = True
                rango_inicio = [i for i in range(1, 6)]
                contexto['rango_inicio'] = rango_inicio
            # Si estamos en una página mayor a 5 y quedan más de 3 páginas por ver consideramos que estamos en una zona media
            # de las páginas
            elif(pagina is not None and int(pagina) >= 5 and int(pagina) < numero_paginas-3):
                # Marcamos que estamos en la zona media, creamos un lista con el rango de las páginas y lo guardamos 
                # en el contexto
                tipoMedio = True
                rango_medio = [i for i in range(int(pagina)-1, int(pagina)+2)]
                contexto['rango_medio'] = rango_medio
            # Si estamos en una de las 4 últimas páginas consideramos que estamos en la zona final de las páginas
            elif(pagina is not None and int(pagina) >= numero_paginas-3):
                # Marcamos que estamos en la zona final, creamos un lista con el rango de las páginas y lo guardamos 
                # en el contexto
                tipoFin = True
                rango_fin = [i for i in range(numero_paginas-3, numero_paginas+1)]
                contexto['rango_fin'] = rango_fin
                # Nos quedamos con la página de la mitad entre la primera del rango final y la primera página. Así hay un enlace
                # a una página intermedia
                pagina_media = math.ceil((rango_fin[0]+1)/2)
                contexto['pagina_media'] = pagina_media
        # Guardamos en el contexto las variables para saber en que zona de las páginas estamos
        contexto['tipoInicio'] = tipoInicio
        contexto['tipoMedio'] = tipoMedio
        contexto['tipoFin'] = tipoFin
    # Renderizamos la página de las actividades a las que está apuntado un usuario paginadas
    return render(request, "misActividades.html", contexto)


def perfil(request):
    # Creamos el 'contexto' (Diccionario Python) de la vista en donde almacenaremos aquellos elementos que queramos mostrar
    # en la vista o que necesitaremos en las vistas
    contexto = {}
    # Guardamos el usuario, si es administrador y si ha iniciado sesión en el contexto
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    # Para saber si el usuario quiere editar algún campo creamos una variable para cada campo que será iniciada a False y 
    # si pulsa en editar un campo se pondrá a True
    editarNombre = False
    editarApellidos = False
    editarComunicaciones = False
    editarCuentaBancaria = False
    editarEmail = False
    editarTelefono = False
    editarDireccionPostal = False
    editarEmpresa = False
    editarContraseña = False
    # Creamos una lista para almacenar los errores que pueda hacer el usuario a la hora de editar un campo
    errores = []
    # Si el usuario ha pulsado un botón de editar
    if(request.method == 'POST'):
        # Editar el nombre
        if('editarNombrePerfil.x' in request.POST):
            # Si ha pulsado en el botón de editar el nombre se pone a True la variable para mostrar la vista con la opción
            # de editarlo
            editarNombre = True
        elif('guardarNombrePerfil.x' in request.POST):
            # Si se ha pulsado en guardar el nuevo nombre, lo guardamos en una variable para analizarlo
            nuevoNombre = request.POST['inputNuevoNombre']
            if(nuevoNombre == ''):
                # Si el nombre está vacío añadimos el error a la lista
                errores.append('Debe introducir un nombre')
            else:
                # En caso de que no haya errores cambiamos el nombre por el nuevo
                modelos.Usuario.objects.filter(usuario = usuario).update(nombre = nuevoNombre)
                # Decimos que ya no estamos editando el nombre y limpiamos la lista de errores por si hay alguno almacenado
                editarNombre = False
                errores.clear()
        elif('cancelarNombrePerfil.x' in request.POST):
            # Si ha pulsado en el botón de cancelar el cambio decimos que ya no estamos editando el nombre
            editarNombre = False
        # Editar los apellidos
        elif('editarApellidosPerfil.x' in request.POST):
            # Si ha pulsado en el botón de editar los apellidos se pone a True la variable para mostrar la vista con la opción
            # de editarlos
            editarApellidos = True
        elif('guardarApellidosPerfil.x' in request.POST):
            # Si se ha pulsado en guardar los nuevos apellidos, los guardamos en una variable para analizarlos
            nuevosApellidos = request.POST['inputNuevosApellidos']
            if(nuevosApellidos == ''):
                # Si los apellidos están vacíos añadimos el error a la lista
                errores.append('Debe introducir unos apellidos')
            else:
                # En caso de que no haya errores cambiamos los apellidos por los nuevos
                modelos.Usuario.objects.filter(usuario = usuario).update(apellidos = nuevosApellidos)
                # Decimos que ya no estamos editando los apellidos y limpiamos la lista de errores por si hay alguno almacenado
                editarApellidos = False
                errores.clear()
        elif('cancelarApellidosPerfil.x' in request.POST):
            # Si ha pulsado en el botón de cancelar el cambio decimos que ya no estamos editando los apellidos
            editarApellidos = False
        # Editar la cuenta bancaria
        elif('editarCuentaBancariaPerfil.x' in request.POST):
            # Si ha pulsado en el botón de editar la cuenta bancaria se pone a True la variable para mostrar 
            # la vista con la opción de editarla
            editarCuentaBancaria = True
        elif('guardarCuentaBancariaPerfil.x' in request.POST):
            # Si se ha pulsado en guardar la nueva cuenta bancaria, la guardamos en una variable para analizarla
            nuevaCuentaBancaria = request.POST['inputNuevaCuentaBancaria']
            if(nuevaCuentaBancaria == ''):
                # Si la cuenta bancaria está vacía añadimos el error a la lista
                errores.append('Debe introducir una cuenta bancaria')
            elif(not nuevaCuentaBancaria.startswith('ES')):
                # Si la cuenta bancaria no empieza por ES añadimos el error a la lista
                errores.append('La cuenta bancaria debe empezar por ES')
            else:
                # En caso de que no haya errores cambiamos la cuenta bancaria por la nueva
                modelos.Usuario.objects.filter(usuario = usuario).update(cuentaBancaria = nuevaCuentaBancaria)
                # Decimos que ya no estamos editando la cuenta bancaria y limpiamos la lista de errores por si hay 
                # alguno almacenado
                editarCuentaBancaria = False
                errores.clear()
        elif('cancelarCuentaBancariaPerfil.x' in request.POST):
            # Si ha pulsado en el botón de cancelar el cambio decimos que ya no estamos editando la cuenta bancaria
            editarCuentaBancaria = False
        # Editar el email
        elif('editarEmailPerfil.x' in request.POST):
            # Si ha pulsado en el botón de editar el email se pone a True la variable para mostrar la vista con la opción
            # de editarlo
            editarEmail = True
        elif('guardarEmailPerfil.x' in request.POST):
            # Si se ha pulsado en guardar el nuevo email, lo guardamos en una variable para analizarlo
            nuevoEmail = request.POST['inputNuevoEmail']
            if(nuevoEmail == ''):
                # Si el email está vacío añadimos el error a la lista
                errores.append('Debe introducir el nuevo email')
            elif(not validate_email(email_address=nuevoEmail)):
                # Con esta librería de Python comprobamos que el email existe y si no existe añadimos el error a la lista
                errores.append('Introduzca un formato de email válido')
            else:
                # En caso de que no haya errores cambiamos el email por el nuevo
                modelos.Usuario.objects.filter(usuario = usuario).update(email = nuevoEmail)
                # Decimos que ya no estamos editando el email y limpiamos la lista de errores por si hay alguno almacenado
                editarEmail = False
                errores.clear()
        elif('cancelarEmailPerfil.x' in request.POST):
            # Si ha pulsado en el botón de cancelar el cambio decimos que ya no estamos editando el email
            editarEmail = False
        # Editar el telefono
        elif('editarTelefonoPerfil.x' in request.POST):
            # Si ha pulsado en el botón de editar el teléfono se pone a True la variable para mostrar la vista con la opción
            # de editarlo
            editarTelefono = True
        elif('guardarTelefonoPerfil.x' in request.POST):
            # Si se ha pulsado en guardar el nuevo teléfono, lo guardamos en una variable para analizarlo
            nuevoTelefono = request.POST['inputNuevoTelefono']
            if(nuevoTelefono == ''):
                # Si el teléfono está vacío añadimos el error a la lista
                errores.append('Introduzca el nuevo teléfono')
            elif((not nuevoTelefono.startswith('6')) and (not nuevoTelefono.startswith('7'))):
                # Si el teléfono no empieza por 6 o por 7 añadimos el error a la lista
                errores.append('El teléfono debe empezar por 6 o por 7')
            else:
                # En caso de que no haya errores cambiamos el teléfono por el nuevo
                modelos.Usuario.objects.filter(usuario = usuario).update(telefono = nuevoTelefono)
                # Decimos que ya no estamos editando el teléfono y limpiamos la lista de errores por si hay alguno almacenado
                editarTelefono = False
                errores.clear()
        elif('cancelarTelefonoPerfil.x' in request.POST):
            # Si ha pulsado en el botón de cancelar el cambio decimos que ya no estamos editando el teléfono
            editarDireccionPostal = False
        # Editar la dirección
        elif('editarDireccionPostalPerfil.x' in request.POST):
            # Si ha pulsado en el botón de editar la dirección postal se pone a True la variable para mostrar la vista 
            # con la opción de editarla
            editarDireccionPostal = True
        elif('guardarDireccionPostalPerfil.x' in request.POST):
            # Si se ha pulsado en guardar la nueva dirección postal, la guardamos en una variable para analizarla
            nuevaDireccionPostal = request.POST['inputNuevaDireccionPostal']
            if(nuevaDireccionPostal == ''):
                # Si la dirección postal está vacía añadimos el error a la lista
                errores.append('Introduce la nueva dirección postal')
            else:
                # En caso de que no haya errores cambiamos la dirección postal por la nueva
                modelos.Usuario.objects.filter(usuario = usuario).update(direccionPostal = nuevaDireccionPostal)
                # Decimos que ya no estamos editando la dirección postal y limpiamos la lista de errores por si 
                # hay alguno almacenado
                editarDireccionPostal = False
                errores.clear()
        elif('cancelarDireccionPostalPerfil.x' in request.POST):
            # Si ha pulsado en el botón de cancelar el cambio decimos que ya no estamos editando la dirección postal
            editarTelefono = False
        # Editar la empresa
        if('editarEmpresaPerfil.x' in request.POST):
            # Si ha pulsado en el botón de editar la empresa se pone a True la variable para mostrar la vista con la opción
            # de editarla
            editarEmpresa = True
        elif('guardarEmpresaPerfil.x' in request.POST):
            # Si se ha pulsado en guardar la nueva empresa, la guardamos en una variable para analizarla
            nuevaEmpresa = request.POST['inputNuevaEmpresa']
            if(nuevaEmpresa == ''):
                # Si la empresa está vacía añadimos el error a la lista
                errores.append('Introduce la nueva empresa')
            else:
                # En caso de que no haya errores cambiamos la empresa por la nueva
                modelos.Usuario.objects.filter(usuario = usuario).update(empresa = nuevaEmpresa)
                # Decimos que ya no estamos editando la empresa y limpiamos la lista de errores por si hay alguno almacenado
                editarEmpresa = False
                errores.clear()
        elif('cancelarEmpresaPerfil.x' in request.POST):
            # Si ha pulsado en el botón de cancelar el cambio decimos que ya no estamos editando la empresa
            editarEmpresa = False
        # Editar las comunicaciones
        elif('editarComunicacionesPerfil.x' in request.POST):
            # Si ha pulsado en el botón de editar las comunicaciones se pone a True la variable para mostrar la vista 
            # con la opción de editarlo
            editarComunicaciones = True
        elif('guardarComunicacionesPerfil.x' in request.POST):
            # Si se ha pulsado en guardar las comunicaciones
            if('inputNuevasComunicaciones' in request.POST):
                # Si se ha seleccionado que haya comunicaciones cambiamos la opción para que nos lleguen comunicaciones
                modelos.Usuario.objects.filter(usuario = usuario).update(comunicaciones = True)
            else:
                # Si se ha seleccionado que no haya comunicaciones cambiamos la opción para que no nos lleguen
                # más comunicaciones
                modelos.Usuario.objects.filter(usuario = usuario).update(comunicaciones = False)
            # Decimos que ya no estamos editando las comunicaciones
            editarComunicaciones = False
        elif('cancelarComunicacionesPerfil.x' in request.POST):
            # Si ha pulsado en el botón de cancelar el cambio decimos que ya no estamos editando las comunicaciones
            editarComunicaciones = False
        # Editar la contraseña
        elif('botonCambiarContraseña' in request.POST):
            # Si ha pulsado en el botón de editar la contraseña se pone a True la variable para mostrar la vista 
            # con la opción de editarlo
            editarContraseña = True
        elif('guardarNuevaContraseña.x' in request.POST):
            # Si se ha pulsado en guardar la nueva contraseña, guardamos la contraseña y la confirmación de la contraseña
            # para analizarlas
            nuevaContraseña = request.POST['inputNuevaContraseña']
            confirmacionContraseña = request.POST['inputConfirmacionContraseña']
            if(nuevaContraseña != confirmacionContraseña):
                # Si la contraseña y la confirmación no coinciden añadimos el error a la lista
                errores.append('La nueva contraseña y su confirmación deben coincidir')
            else:
                # En el caso de que sean iguales la contraseña y su confirmación analizamos la nueva contraseña
                # Recuperamos la antigua contraseña que tenía el usuario
                antiguaContraseña = modelos.Usuario.objects.get(usuario = usuario).contraseña
                # Vemos si la nueva contraseña contiene al menos una mayúscula y un número con las expresiones regulares
                # de la librería de Python
                contieneMayuscula = re.search("[A-Z]", nuevaContraseña)
                contieneNumero = re.search("[0-9]", nuevaContraseña)
                if(nuevaContraseña == antiguaContraseña):
                    # Si la nueva contraseña es igual a la antigua añadimos el error a la lista
                    errores.append('La nueva contraseña no puede ser igual que la anterior')
                elif(len(nuevaContraseña) < 8):
                    # Si la nueva contraseña tiene menos de 8 caracteres añadimos el error a la lista
                    errores.append('La nueva contraseña debe contener más de 8 caracteres')
                elif(not contieneMayuscula):
                    # Si la nueva contraseña no contiene al menos una letra mayúscula añadimos el error a la lista
                    errores.append('La nueva contraseña debe contener alguna letra mayúscula')
                elif(not contieneNumero):
                    # Si la nueva contraseña no contiene al menos un número añadimos el error a la lista
                    errores.append('La nueva contraseña debe contener algún número')
                else:
                    # # En caso de que no haya errores cambiamos la contraseña por la nueva
                    modelos.Usuario.objects.filter(usuario = usuario).update(contraseña = nuevaContraseña)
                    # Decimos que ya no estamos editando la contraseña y limpiamos la lista de errores por si hay 
                    # alguno almacenado
                    editarContraseña = False
                    errores.clear()
        elif('cancelarNuevaContraseña.x' in request.POST):
            # Si ha pulsado en el botón de cancelar el cambio decimos que ya no estamos editando la contraseña
            editarContraseña = False
    # Guardamos en el contexto las variables para saber que campo se está editando
    contexto['editarNombre'] = editarNombre
    contexto['editarApellidos'] = editarApellidos
    contexto['editarComunicaciones'] = editarComunicaciones
    contexto['editarCuentaBancaria'] = editarCuentaBancaria
    contexto['editarEmail'] = editarEmail
    contexto['editarTelefono'] = editarTelefono
    contexto['editarDireccionPostal'] = editarDireccionPostal
    contexto['editarEmpresa'] = editarEmpresa
    contexto['editarContraseña'] = editarContraseña
    # Guardamos en el contexto la lista de errores. Si está vacía no se mostrará ninguno y si hay alguno se mostrará
    contexto['errores'] = errores
    if(usuario is not None):
        # Si se ha iniciado sesión guardamos el usuario con el que se ha iniciado sesión
        usuarioLogin = usuario
        # Guardamos los datos almacenados del usuario en una variable
        usuario = modelos.Usuario.objects.get(usuario = usuarioLogin)
        # Guardamos en el contexto los elementos del usuario que queremos mostrarle de su perfil
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
    # Renderizamos la página del perfil del usuario
    return render(request, "perfil.html", contexto)


def login(request):
    # Creamos el 'contexto' (Diccionario Python) de la vista en donde almacenaremos aquellos elementos que queramos mostrar
    # en la vista
    contexto = {}
    # Guardamos el usuario, si es administrador y si ha iniciado sesión en el contexto
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    # Vemos si el usuario ha pulsado el botón de iniciar sesión
    if(request.method == 'POST'):
        # Si lo ha pulsado guardamos los datos del formulario
        formulario = request.POST
        # Nos quedamos con el usuario introducido
        usuarioFormulario = formulario['usuario']
        # Hacemos un try para ver si el usuario introducido es correcto. Si no lo es lanzamos el error en la página de login
        try:
            usuarioBD = modelos.Usuario.objects.get(usuario=usuarioFormulario)
        except ObjectDoesNotExist:
            error = "El usuario es incorrecto"
            contexto['error'] = error
            return render(request, "login.html", contexto)
        # Nos quedamos con la contraseña introducida en el formulario
        contraseña = formulario['contraseña']
        if(not (contraseña == usuarioBD.contraseña)):
            # Si la contraseña no es igual a la almacenada guardamos el error en el contexto y lanzamos el error en 
            # la página de login
            error = "La contraseña es incorrecta"
            contexto['error'] = error
            return render(request, "login.html", contexto)
        else:
            # Si no ha habido errores guardamos en la sesión que se ha iniciado sesión y el usuario
            inicioSesion = True
            request.session['inicioSesion'] = inicioSesion
            request.session['usuario'] = usuarioBD.usuario
            if(str(usuarioBD.tipo)=='Administrador'):
                # Si el usuario es administrados guardamos en la sesión que es administrador
                request.session['esAdministrador'] = True
            else:
                # Si el usuario no es administrados guardamos en la sesión que no es administrador
                request.session['esAdministrador'] = False
            # Al haber ido todo bien redirigimos al usuario a la página de éxito para que sepa que ha ido todo bien
            return redirect('exitoLogin')
    # Renderizamos la página de login
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


def recuperarContraseña(request):
    # Creamos el 'contexto' (Diccionario Python) de la vista en donde almacenaremos aquellos elementos que queramos mostrar
    # en la vista
    contexto = {}
    # Guardamos el usuario, si es administrador y si ha iniciado sesión en el contexto
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    # Vemos si el usuario ha pulsado en enviar los datos para recuperar la contraseña
    if(request.method == 'POST'):
        # Si lo ha pulsado guardamos los datos del formulario
        formulario = request.POST
        # Nos quedamos con el usuario introducido
        usuarioFormulario = formulario['inputUsuario']
        # Hacemos un try para ver si el usuario introducido es correcto. Si no lo es lanzamos el error en la página
        try:
            usuarioBD = modelos.Usuario.objects.get(usuario=usuarioFormulario)
        except ObjectDoesNotExist:
            error = "El usuario es incorrecto"
            contexto['error'] = error
            return render(request, "recuperarContraseña.html", contexto)
        # Guardamos la nueva contraseña y la confirmación de esta que se ha introducido
        nuevaContraseña = request.POST['inputNuevaContraseña']
        confirmacionContraseña = request.POST['inputConfirmacionContraseña']
        if(nuevaContraseña != confirmacionContraseña):
            # Si las contraseñas no coinciden guardamos el error y lo mostramos en la página
            error = "La nueva contraseña y su confirmación deben coincidir"
            contexto['error'] = error
            return render(request, "recuperarContraseña.html", contexto)
        else:
            # Si las contraseñas coinciden consultamos la antigua contraseña y la guardamos
            antiguaContraseña = modelos.Usuario.objects.get(usuario = usuarioFormulario).contraseña
            # Vemos si la nueva contraseña contiene al menos una mayúscula y un numero mediante la librería de expresiones
            # regulares
            contieneMayuscula = re.search("[A-Z]", nuevaContraseña)
            contieneNumero = re.search("[0-9]", nuevaContraseña)
            if(len(nuevaContraseña) < 8):
                # Si la longitud de la nueva contraseña es menor que 8 almacenamos el error y lo mostramos en la página
                error = 'La nueva contraseña debe contener más de 8 caracteres'
                contexto['error'] = error
                return render(request, "recuperarContraseña.html", contexto)
            elif(nuevaContraseña == antiguaContraseña):
                # Si la nueva contraseña es igual a la anterior almacenamos el error y lo mostramos en la página
                error = 'La nueva contraseña no puede ser igual que la anterior'
                contexto['error'] = error
                return render(request, "recuperarContraseña.html", contexto)
            elif(not contieneMayuscula):
                # Si la nueva contraseña no contiene al menos una mayúscula almacenamos el error y lo mostramos en la página
                error = 'La nueva contraseña debe contener alguna letra mayúscula'
                contexto['error'] = error
                return render(request, "recuperarContraseña.html", contexto)
            elif(not contieneNumero):
                # Si la nueva contraseña no contiene al menos un número almacenamos el error y lo mostramos en la página
                error = 'La nueva contraseña debe contener algún número'
                contexto['error'] = error
                return render(request, "recuperarContraseña.html", contexto)
            else:
                # Si no ha habido ningún error actualizamos la contraseña con la nueva y redirigimos a la página de éxito
                # para decir al usuario que ha ido todo bien
                modelos.Usuario.objects.filter(usuario = usuarioFormulario).update(contraseña = nuevaContraseña)
                return redirect('exitoRecuperarContraseña')
    # Renderizamos la página para recuperar la contraseña
    return render(request, "recuperarContraseña.html", contexto)


def exitoRecuperarContraseña(request):
    contexto = {}
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    return render(request, "exitoRecuperarContraseña.html", contexto)


def logout(request):
    # Creamos el 'contexto' (Diccionario Python) de la vista en donde almacenaremos aquellos elementos que queramos mostrar
    # en la vista
    contexto = {}
    # Guardamos en la sesión que el usuario es None y si es administrador y si ha iniciado sesión como False
    request.session['usuario'] = None
    request.session['esAdministrador'] = False
    request.session['inicioSesion'] = False
    # Guardamos el usuario, si es administrador y si ha iniciado sesión con los nuevos valores en el contexto
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    # Renderizamos la página de que se ha cerrado la sesión
    return render(request, "logout.html", contexto)


def formularioAltaUsuario(request):
    # Creamos el 'contexto' (Diccionario Python) de la vista en donde almacenaremos aquellos elementos que queramos mostrar
    # en la vista
    contexto = {}
    # Guardamos el usuario, si es administrador y si ha iniciado sesión en el contexto
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    # Creamos la variable del formulario con el tipo de formulario que es y lo guardamos en el contexto
    formUsuario = formularios.FormularioAltaUsuario(request.POST, request.FILES or None)
    contexto['formUsuario'] = formUsuario
    # Vemos si se ha recibido en la request el Post del formulario, en caso afirmativo es que se han enviado los datos con el
    # botón de enviar
    if(request.method == 'POST'):
        if(formUsuario.is_valid()):
            # Guardamos los datos y los archivos recibidos en la variable del formulario creada anteriormente
            formUsuario = formularios.FormularioAltaUsuario(request.POST, request.FILES)
            # Si es valido creamos el objeto usuario
            usuario = formUsuario.save(commit=False)
            # Nos quedamos el nombre y los apellidos del usuario
            nombre = usuario.nombre
            apellidos = usuario.apellidos
            # Guardamos el usuario en la base de datos y ponemos el formulario en blanco
            formUsuario.save()
            formUsuario = formularios.FormularioAltaUsuario()
            # Redirigimos a la página de éxito pues ha ido todo bien
            return redirect('exitoAltaUsuario', nombre=nombre, apellidos=apellidos)
        else:
            # En caso contrario vemos los errores que hay y los guardamos en el contexto para mostrarlos en la vista
            if('__all__' in formUsuario.errors.keys()):
                errores = [error for error in formUsuario.errors['__all__']]
                contexto['errores'] = errores
            else:
                errores = [error for lsErrores in formUsuario.errors.values() for error in lsErrores]
                contexto['errores'] = errores
    # Renderizamos la página del formulario con este en blanco o con los errores que haya
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
    # Creamos el 'contexto' (Diccionario Python) de la vista en donde almacenaremos aquellos elementos que queramos mostrar
    # en la vista
    contexto = {}
    # Guardamos el usuario, si es administrador y si ha iniciado sesión en el contexto
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    # Creamos la variable del formulario con el tipo de formulario que es y lo guardamos en el contexto
    formActividad = formularios.FormularioAltaActividad(request.POST, request.FILES or None)
    contexto['formActividad'] = formActividad
    # Vemos si se ha recibido en la request el Post del formulario, en caso afirmativo es que se han enviado los datos con el
    # botón de enviar
    if(request.method == 'POST'):
        # Guardamos los datos y los archivos recibidos en la variable del formulario creada anteriormente
        formActividad = formularios.FormularioAltaActividad(request.POST, request.FILES)
        # Preguntamos si es válido con la comprobación que se hace en el fichero 'forms.py'
        if(formActividad.is_valid()):
            # Si es valido creamos el objeto actividad
            actividad = formActividad.save(commit=False)
            # Nos quedamos el título y la descripción de la actividad
            titulo = actividad.titulo
            descripcion = actividad.descripcion
            # Guardamos la actividad en la base de datos y ponemos el formulario en blanco
            formActividad.save()
            formActividad = formularios.FormularioAltaActividad()
            # Enviamos los correos con el título y la descripción de la actividad a los usuarios que tengan las comunicaciones
            # activadas y publicamos un Tweet con el título
            enviarCorreosConActividad(str(titulo), str(descripcion))
            publicarTweetActividad(str(titulo))
            # Redirigimos a la página de éxito pues ha ido todo bien
            return redirect('exitoAltaActividad', titulo = titulo)
        else:
            # En caso contrario vemos los errores que hay y los guardamos en el contexto para mostrarlos en la vista
            if('__all__' in formActividad.errors.keys()):
                errores = [error for error in formActividad.errors['__all__']]
                contexto['errores'] = errores
            else:
                errores = [error for lsErrores in formActividad.errors.values() for error in lsErrores]
                contexto['errores'] = errores
    # Renderizamos la página del formulario con este en blanco o con los errores que haya
    return render(request, "formularioAltaActividad.html", contexto)


def publicarTweetNoticia(titulo):
    api_twitter = twitter.Api(consumer_key = 'XSPvc9U4HgUm2dfqoY9WBvtHI', 
        consumer_secret = 'manhSe3L3mnjKHQjMu3QtUtDBQSlqX29217dyjB7FA6gE4THT4',
        access_token_key = '1327583260348739590-6uTs3sucXoMRV4UyIJ0Tr2EdhOiSR0',
        access_token_secret = 'YHlo610QHMmU5cE7CVDAfR1GeAmWcbyuHvdcAPyONUP7O')
    texto_tweet = 'Tenemos una nueva noticia que contaros: ' + titulo
    api_twitter.PostUpdate(status = texto_tweet)


def formularioAltaNoticia(request):
    # Creamos el 'contexto' (Diccionario Python) de la vista en donde almacenaremos aquellos elementos que queramos mostrar
    # en la vista
    contexto = {}
    # Guardamos el usuario, si es administrador y si ha iniciado sesión en el contexto
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    # Creamos la variable del formulario con el tipo de formulario que es y lo guardamos en el contexto
    formNoticia = formularios.FormularioAltaNoticia(request.POST, request.FILES or None)
    contexto['formNoticia'] = formNoticia
    # Vemos si se ha recibido en la request el Post del formulario, en caso afirmativo es que se han enviado los datos con el
    # botón de enviar
    if(request.method == 'POST'):
        # Guardamos los datos y los archivos recibidos en la variable del formulario creada anteriormente
        formNoticia = formularios.FormularioAltaNoticia(request.POST, request.FILES)
        # Preguntamos si es válido con la comprobación que se hace en el fichero 'forms.py'
        if(formNoticia.is_valid()):
            # Si es valido creamos el objeto noticia
            noticia = formNoticia.save(commit=False)
            # Nos quedamos el título de la noticia
            titulo = noticia.titulo
            # Guardamos la noticia en la base de datos y ponemos el formulario en blanco
            formNoticia.save()
            formNoticia = formularios.FormularioAltaNoticia()
            # Publicamos un Tweet con el título de la noticia
            publicarTweetNoticia(str(titulo))
            # Redirigimos a la página de éxito pues ha ido todo bien
            return redirect('exitoAltaNoticia', titulo = titulo)
        else:
            # En caso contrario vemos los errores que hay y los guardamos en el contexto para mostrarlos en la vista
            if('__all__' in formNoticia.errors.keys()):
                errores = [error for error in formNoticia.errors['__all__']]
                contexto['errores'] = errores
            else:
                errores = [error for lsErrores in formNoticia.errors.values() for error in lsErrores]
                contexto['errores'] = errores
    # Renderizamos la página del formulario con este en blanco o con los errores que haya
    return render(request, "formularioAltaNoticia.html", contexto)


def formularioAltaOfertaEmpleo(request):
    # Creamos el 'contexto' (Diccionario Python) de la vista en donde almacenaremos aquellos elementos que queramos mostrar
    # en la vista
    contexto = {}
    # Guardamos el usuario, si es administrador y si ha iniciado sesión en el contexto
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    # Creamos la variable del formulario con el tipo de formulario que es y lo guardamos en el contexto
    formOfertaEmpleo = formularios.FormularioAltaOfertaEmpleto(request.POST, request.FILES or None)
    contexto['formOfertaEmpleo'] = formOfertaEmpleo
    # Vemos si se ha recibido en la request el Post del formulario, en caso afirmativo es que se han enviado los datos con el
    # botón de enviar
    if(request.method == 'POST'):
        # Guardamos los datos y los archivos recibidos en la variable del formulario creada anteriormente
        formOfertaEmpleo = formularios.FormularioAltaOfertaEmpleto(request.POST, request.FILES)
        # Preguntamos si es válido con la comprobación que se hace en el fichero 'forms.py'
        if(formOfertaEmpleo.is_valid()):
            # Si es valido creamos el objeto oferta de empleo
            ofertaEmpleo = formOfertaEmpleo.save(commit=False)
            # Nos quedamos el título de la oferta de empleo
            titulo = ofertaEmpleo.titulo
            # Guardamos la oferta en la base de datos y ponemos el formulario en blanco
            formOfertaEmpleo.save()
            formOfertaEmpleo = formularios.FormularioAltaOfertaEmpleto()
            # Redirigimos a la página de éxito pues ha ido todo bien
            return redirect('exitoAltaOfertaEmpleo', titulo = titulo)
        else:
            # En caso contrario vemos los errores que hay y los guardamos en el contexto para mostrarlos en la vista
            if('__all__' in formOfertaEmpleo.errors.keys()):
                errores = [error for error in formOfertaEmpleo.errors['__all__']]
                contexto['errores'] = errores
            else:
                errores = [error for lsErrores in formOfertaEmpleo.errors.values() for error in lsErrores]
                contexto['errores'] = errores
    # Renderizamos la página del formulario con este en blanco o con los errores que haya
    return render(request, "formularioAltaOfertaEmpleo.html", contexto)


def formularioAltaDatosDeContacto(request):
    # Creamos el 'contexto' (Diccionario Python) de la vista en donde almacenaremos aquellos elementos que queramos mostrar
    # en la vista
    contexto = {}
    # Guardamos el usuario, si es administrador y si ha iniciado sesión en el contexto
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    # Creamos la variable del formulario con el tipo de formulario que es y lo guardamos en el contexto
    formDatosContacto = formularios.FormularioAltaDatosContacto(request.POST, request.FILES or None)
    contexto['formDatosContacto'] = formDatosContacto
    # Vemos si se ha recibido en la request el Post del formulario, en caso afirmativo es que se han enviado los datos con el
    # botón de enviar
    if(request.method == 'POST'):
        # Guardamos los datos y los archivos recibidos en la variable del formulario creada anteriormente
        formDatosContacto = formularios.FormularioAltaDatosContacto(request.POST, request.FILES)
        # Preguntamos si es válido con la comprobación que se hace en el fichero 'forms.py'
        if(formDatosContacto.is_valid()):
            # Si es valido creamos el objeto datos de contacto
            datosContacto = formDatosContacto.save(commit=False)
            # Nos quedamos el teléfono y el email de los datos
            telefono = datosContacto.telefono
            email = datosContacto.email
            # Guardamos los datos en la base de datos y ponemos el formulario en blanco
            formDatosContacto.save()
            formDatosContacto = formularios.FormularioAltaDatosContacto()
            # Redirigimos a la página de éxito pues ha ido todo bien
            return redirect('exitoAltaDatosContacto', telefono = telefono, email = email)
        else:
            # En caso contrario vemos los errores que hay y los guardamos en el contexto para mostrarlos en la vista
            if('__all__' in formDatosContacto.errors.keys()):
                errores = [error for error in formDatosContacto.errors['__all__']]
                contexto['errores'] = errores
            else:
                errores = [error for lsErrores in formDatosContacto.errors.values() for error in lsErrores]
                contexto['errores'] = errores
    # Renderizamos la página del formulario con este en blanco o con los errores que haya
    return render(request, "formularioAltaDatosDeContacto.html", contexto)


def formularioAltaRevistaIngenio(request):
    # Creamos el 'contexto' (Diccionario Python) de la vista en donde almacenaremos aquellos elementos que queramos mostrar
    # en la vista
    contexto = {}
    # Guardamos el usuario, si es administrador y si ha iniciado sesión en el contexto
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    # Creamos la variable del formulario con el tipo de formulario que es y lo guardamos en el contexto
    formRevistaIngenio = formularios.FormularioAltaRevistaIngenio(request.POST, request.FILES or None)
    contexto['formRevistaIngenio'] = formRevistaIngenio
    # Vemos si se ha recibido en la request el Post del formulario, en caso afirmativo es que se han enviado los datos con el
    # botón de enviar
    if(request.method == 'POST'):
        # Guardamos los datos y los archivos recibidos en la variable del formulario creada anteriormente
        formRevistaIngenio = formularios.FormularioAltaRevistaIngenio(request.POST, request.FILES)
        # Preguntamos si es válido con la comprobación que se hace en el fichero 'forms.py'
        if(formRevistaIngenio.is_valid()):
            # Si es valido creamos el objeto revista
            revista = formRevistaIngenio.save(commit=False)
            # Nos quedamos el número de la revista
            numero = revista.numero
            # Guardamos la revista en la base de datos y ponemos el formulario en blanco
            formRevistaIngenio.save()
            formRevistaIngenio = formularios.FormularioAltaRevistaIngenio()
            # Redirigimos a la página de éxito pues ha ido todo bien
            return redirect('exitoAltaRevistaIngenio', numero = numero)
        else:
            # En caso contrario vemos los errores que hay y los guardamos en el contexto para mostrarlos en la vista
            if('__all__' in formRevistaIngenio.errors.keys()):
                errores = [error for error in formRevistaIngenio.errors['__all__']]
                contexto['errores'] = errores
            else:
                errores = [error for lsErrores in formRevistaIngenio.errors.values() for error in lsErrores]
                contexto['errores'] = errores
    # Renderizamos la página del formulario con este en blanco o con los errores que haya
    return render(request, "formularioAltaRevistaIngenio.html", contexto)


def formularioAltaAcuerdoEmpresa(request):
    # Creamos el 'contexto' (Diccionario Python) de la vista en donde almacenaremos aquellos elementos que queramos mostrar
    # en la vista
    contexto = {}
    # Guardamos el usuario, si es administrador y si ha iniciado sesión en el contexto
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    # Creamos la variable del formulario con el tipo de formulario que es y lo guardamos en el contexto
    formAcuerdo = formularios.FormularioAltaAcuerdoEmpresa(request.POST, request.FILES or None)
    contexto['formAcuerdo'] = formAcuerdo
    # Vemos si se ha recibido en la request el Post del formulario, en caso afirmativo es que se han enviado los datos con el
    # botón de enviar
    if(request.method == 'POST'):
        # Guardamos los datos y los archivos recibidos en la variable del formulario creada anteriormente
        formAcuerdo = formularios.FormularioAltaAcuerdoEmpresa(request.POST, request.FILES)
        # Preguntamos si es válido con la comprobación que se hace en el fichero 'forms.py'
        if(formAcuerdo.is_valid()):
            # Si es valido creamos el objeto acuerdo con empresa
            acuerdoEmpresa = formAcuerdo.save(commit=False)
            # Nos quedamos el nombre del acuerdo
            nombre = acuerdoEmpresa.nombre
            # Guardamos al acuerdo en la base de datos y ponemos el formulario en blanco
            formAcuerdo.save()
            formAcuerdo = formularios.FormularioAltaAcuerdoEmpresa()
            # Redirigimos a la página de éxito pues ha ido todo bien
            return redirect('exitoAltaAcuerdoEmpresa', nombre = nombre)
        else:
            # En caso contrario vemos los errores que hay y los guardamos en el contexto para mostrarlos en la vista
            if('__all__' in formAcuerdo.errors.keys()):
                errores = [error for error in formAcuerdo.errors['__all__']]
                contexto['errores'] = errores
            else:
                errores = [error for lsErrores in formAcuerdo.errors.values() for error in lsErrores]
                contexto['errores'] = errores
    # Renderizamos la página del formulario con este en blanco o con los errores que haya
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


def exitoAltaDatosContacto(request, telefono, email):
    contexto = {}
    usuario = request.session.get('usuario')
    esAdministrador = request.session.get('esAdministrador')
    inicioSesion = request.session.get('inicioSesion')
    contexto['usuario'] = usuario
    contexto['esAdministrador'] = esAdministrador
    contexto['inicioSesion'] = inicioSesion
    contexto['telefono'] = telefono
    contexto['email'] = email
    return render(request, "exitoAltaDatosContacto.html", contexto)
