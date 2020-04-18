from django.contrib import admin

from gestionBD.models import Usuario, Noticia, Actividad, DatosDeContacto, OfertaEmpleo, RevistaIngenio, AcuerdosEmpresas, JuntaRectora, Titulacion, TipoActividad, UsuarioActividad, OfertaEmpleoTitulacion

# Register your models here.

admin.site.register(Usuario)
admin.site.register(Noticia)
admin.site.register(Actividad)
admin.site.register(DatosDeContacto)
admin.site.register(OfertaEmpleo)
admin.site.register(RevistaIngenio)
admin.site.register(AcuerdosEmpresas)
admin.site.register(JuntaRectora)
admin.site.register(Titulacion)
admin.site.register(TipoActividad)
admin.site.register(UsuarioActividad)
admin.site.register(OfertaEmpleoTitulacion)