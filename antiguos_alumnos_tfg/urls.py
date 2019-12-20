"""antiguos_alumnos_tfg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

#C:\Users\carlo\Documents\Carlos Mata Blasco\Universidad\Django\antiguos_alumnos_tfg


from django.contrib import admin
from django.urls import path
from antiguos_alumnos_tfg.views import saludo, inicio, asociacion, actividades, noticias

urlpatterns = [
    path('admin/', admin.site.urls),
    path('saludo/', saludo),
    path('index/', inicio, name='inicio'),
    path('asociacion/', asociacion, name='asociacion'),
    path('actividades/', actividades, name='actividades'),
    path('noticias/', noticias, name='noticias'),
]