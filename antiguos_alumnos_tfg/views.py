from django.http import HttpResponse
from django.template import Template, Context
from django.template import loader
from django.shortcuts import render


def saludo(request):

    return HttpResponse("Pagina del TFG")


def inicio(request):

	return render(request, "index.html")