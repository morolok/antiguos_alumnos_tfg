from django.http import HttpResponse
from django.template import Template, Context
from django.template import loader
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