from django.contrib import admin
import gestionBD.models as modelos

# Register your models here.

admin.site.register(modelos.JuntaRectora)
admin.site.register(modelos.Titulacion)
admin.site.register(modelos.TipoActividad)
admin.site.register(modelos.TipoUsuario)
admin.site.register(modelos.Usuario)
admin.site.register(modelos.Noticia)
admin.site.register(modelos.Actividad)
admin.site.register(modelos.DatosDeContacto)
admin.site.register(modelos.OfertaEmpleo)
admin.site.register(modelos.RevistaIngenio)
admin.site.register(modelos.AcuerdosEmpresas)
admin.site.register(modelos.UsuarioActividad)
admin.site.register(modelos.ListaEsperaUsuarioActividad)
admin.site.register(modelos.OfertaEmpleoTitulacion)