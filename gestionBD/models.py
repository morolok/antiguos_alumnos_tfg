from django.db import models

# Create your models here.

class JuntaRectora(models.Model):
    puesto = models.CharField(max_length=20, primary_key=True, verbose_name='Puesto')

    def __str__(self):
        return self.puesto

class Titulacion(models.Model):
    nombre = models.CharField(max_length=100, primary_key=True, verbose_name='Titulación')

    def __str__(self):
        return self.nombre

class TipoActividad(models.Model):
    tipo = models.CharField(max_length=30, primary_key=True, verbose_name='Tipo de actividad')

    def __str__(self):
        return self.tipo

class TipoUsuario(models.Model):
    tipo = models.CharField(max_length=50, primary_key=True, verbose_name='Tipo de usuario')

    def __str__(self):
        return self.tipo

class Usuario(models.Model):
    nombre = models.CharField(max_length=30, verbose_name='Nombre')
    apellidos = models.CharField(max_length=50, verbose_name='Apellidos')
    dni = models.CharField(max_length=9, primary_key=True, verbose_name='Dni')
    fechaNacimiento = models.DateField(verbose_name='Fecha de nacimiento')
    cuentaBancaria = models.CharField(max_length=24, verbose_name='Cuenta bancaria')
    email = models.EmailField(verbose_name='Email')
    telefono = models.CharField(max_length=9, verbose_name='Teléfono')
    direccionPostal = models.TextField(verbose_name='Dirección postal')
    usuario = models.CharField(max_length=20, verbose_name='Usuario')
    contraseña = models.CharField(max_length=256, verbose_name='Contraseña')
    tipo = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)
    titulacion = models.ForeignKey(Titulacion, on_delete=models.CASCADE)
    promocion = models.CharField(max_length=11, verbose_name='Promoción')
    añoFinalizacion = models.CharField(max_length=4, verbose_name='Año de finalización')
    empresa = models.CharField(max_length=150, verbose_name='Empresa')
    comunicaciones = models.BooleanField(verbose_name='Comunicaciones')
    juntaRectora = models.ForeignKey(JuntaRectora, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre + " " + self.apellidos + " - " + self.dni

class Noticia(models.Model):
    titulo = models.CharField(max_length=50, verbose_name='Título')
    texto = models.TextField(verbose_name='Texto')
    fecha = models.DateTimeField(verbose_name='Fecha')
    enlace = models.CharField(max_length=256, null=True, blank=True, verbose_name='Enlace')

class Actividad(models.Model):
    titulo = models.CharField(max_length=50, primary_key=True, verbose_name='Título')
    descripcion = models.CharField(max_length=1024, verbose_name='Descripción')
    textoReseña = models.TextField(verbose_name='Texto de reseña')
    imagen = models.ImageField(upload_to='images', max_length=256, verbose_name='Imagen')
    fecha = models.DateField(verbose_name='Fecha')
    hora = models.CharField(max_length=5, verbose_name='Hora')
    enlaceAlbum = models.CharField(max_length=256, null=True, blank=True, verbose_name='Enlace al album')
    tipoActividad = models.ForeignKey(TipoActividad, on_delete=models.CASCADE)

class DatosDeContacto(models.Model):
    telefono = models.CharField(max_length=9, verbose_name='Teléfono')
    email = models.EmailField(verbose_name='Email')
    horario = models.TextField(verbose_name='Horario')
    horarioEspecial = models.TextField(verbose_name='Horario especial')
    ubicacion = models.CharField(max_length=100, null=True, blank=True, verbose_name='Ubicación')
    facebook = models.CharField(max_length=256, null=True, blank=True, verbose_name='Facebook')
    twitter = models.CharField(max_length=256, null=True, blank=True, verbose_name='Twitter')
    instagram = models.CharField(max_length=256, null=True, blank=True, verbose_name='Instagram')

class OfertaEmpleo(models.Model):
    titulo = models.CharField(max_length=200, primary_key=True, verbose_name='Título')
    texto = models.TextField(verbose_name='Texto')
    contacto = models.CharField(max_length=100, null=True, blank=True, verbose_name='Contacto')
    perfil = models.CharField(max_length=100, verbose_name='Perfil')
    fecha = models.DateField(verbose_name='Fecha')
    titulaciones = models.CharField(max_length=24, verbose_name='Titulaciones')

class RevistaIngenio(models.Model):
    numero = models.IntegerField(primary_key=True, verbose_name='Número')
    imagen = models.ImageField(upload_to='images', max_length=256, null=True, blank=True, verbose_name='Imagen')
    fichero = models.FileField(upload_to='files', verbose_name='Fichero')
    fecha = models.DateField(verbose_name='Fecha')
    tablaContenido = models.TextField(null=True, blank=True, verbose_name='Tabla de contenidos')
    
    def __str__(self):
        return "Revista número " + str(self.numero)

class AcuerdosEmpresas(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    fichero = models.FileField(upload_to='files', verbose_name='Fichero')
    texto = models.TextField(null=True, blank=True, verbose_name='Texto')

class UsuarioActividad(models.Model):
    dniUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    #dniUsuario = models.CharField(max_length=9, null=False)
    #actividad = models.CharField(max_length=50, null=False)

class OfertaEmpleoTitulacion(models.Model):
    #ofertaEmpleo = models.CharField(max_length=200, null=False)
    ofertaEmpleo = models.ForeignKey(OfertaEmpleo, on_delete=models.CASCADE)
    titulacion = models.ForeignKey(Titulacion, on_delete=models.CASCADE)
