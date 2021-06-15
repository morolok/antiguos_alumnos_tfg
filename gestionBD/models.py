from django.db import models
from django.core.validators import URLValidator

# Create your models here.


class JuntaRectora(models.Model):
    puesto = models.CharField(max_length=20, primary_key=True, verbose_name='Puesto')

    class Meta:
        verbose_name = 'Junta Rectora'
        verbose_name_plural = 'Junta Rectora'

    def __str__(self):
        return self.puesto


class Titulacion(models.Model):
    nombre = models.CharField(max_length=100, primary_key=True, verbose_name='Titulación')

    class Meta:
        verbose_name = 'Titulación'
        verbose_name_plural = 'Titulaciones'

    def __str__(self):
        return self.nombre


class TipoActividad(models.Model):
    tipo = models.CharField(max_length=30, primary_key=True, verbose_name='Tipo de actividad')

    class Meta:
        verbose_name = 'Tipo de actividad'
        verbose_name_plural = 'Tipos de actividades'

    def __str__(self):
        return self.tipo


class EstadoActividad(models.Model):
    estado = models.CharField(max_length=50, primary_key=True, verbose_name='Estado de la actividad')

    class Meta:
        verbose_name = 'Estado de la actividad'
        verbose_name_plural = 'Estados de las actividades'

    def __str__(self):
        return self.estado


class TipoUsuario(models.Model):
    tipo = models.CharField(max_length=50, primary_key=True, verbose_name='Tipo de usuario')

    class Meta:
        verbose_name = 'Tipo de usuario'
        verbose_name_plural = 'Tipos de usuarios'

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
    usuario = models.CharField(max_length=20, unique=True, verbose_name='Usuario')
    contraseña = models.CharField(max_length=256, verbose_name='Contraseña')
    tipo = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE, verbose_name='Tipo de usuario')
    titulacion = models.ForeignKey(Titulacion, on_delete=models.CASCADE, verbose_name='Titulación')
    promocion = models.IntegerField(verbose_name='Promoción')
    añoFinalizacion = models.IntegerField(verbose_name='Año de finalización')
    empresa = models.CharField(max_length=150, verbose_name='Empresa')
    comunicaciones = models.BooleanField(verbose_name='Comunicaciones')
    juntaRectora = models.ForeignKey(JuntaRectora, on_delete=models.CASCADE, verbose_name='Junta rectora')

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.nombre + " " + self.apellidos + " - " + self.dni


class Noticia(models.Model):
    titulo = models.CharField(max_length=1024, primary_key=True, verbose_name='Título')
    texto = models.TextField(verbose_name='Texto')
    fecha = models.DateField(verbose_name='Fecha')
    enlace = models.URLField(null=True, blank=True, verbose_name='Enlace', validators=[URLValidator()])
    fichero = models.FileField(upload_to='files', blank=True, verbose_name='Fichero')
    imagen = models.ImageField(upload_to='images', blank=True, verbose_name='Imagen')

    class Meta:
        verbose_name = 'Noticia'
        verbose_name_plural = 'Noticias'

    def __str__(self):
        return self.titulo


class Actividad(models.Model):
    titulo = models.CharField(max_length=1024, primary_key=True, verbose_name='Título')
    descripcion = models.TextField(verbose_name='Descripción')
    textoReseña = models.TextField(null=True, blank=True, verbose_name='Texto de reseña')
    imagen = models.ImageField(upload_to='images', null=True, blank=True, verbose_name='Imagen')
    fecha = models.DateField(verbose_name='Fecha de la actividad')
    hora = models.TimeField(null=True, blank=True, verbose_name='Hora de la actividad')
    enlaceAlbum = models.URLField(null=True, blank=True, verbose_name='Enlace al album', validators=[URLValidator()])
    numeroPlazas = models.IntegerField(verbose_name='Número de plazas')
    fechaSolicitudesInicio = models.DateField(verbose_name='Fecha de inicio de las solicitudes')
    fechaSolicitudesFin = models.DateField(verbose_name='Fecha de fin de las solicitudes')
    fichero = models.FileField(upload_to='files', blank=True, verbose_name='Fichero')
    estadoActividad = models.ForeignKey(EstadoActividad, on_delete=models.CASCADE, verbose_name='Estado de la actividad')
    tipoActividad = models.ForeignKey(TipoActividad, on_delete=models.CASCADE, verbose_name='Tipo de actividad')

    class Meta:
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'

    def __str__(self):
        return self.titulo


class DatosDeContacto(models.Model):
    telefono = models.CharField(max_length=9, primary_key=True, verbose_name='Teléfono')
    email = models.EmailField(verbose_name='Email')
    horario = models.TextField(verbose_name='Horario')
    horarioEspecial = models.TextField(verbose_name='Horario especial')
    ubicacion = models.CharField(max_length=200, verbose_name='Ubicación')
    facebook = models.URLField(null=True, blank=True, verbose_name='Facebook', validators=[URLValidator()])
    twitter = models.URLField(null=True, blank=True, verbose_name='Twitter', validators=[URLValidator()])
    instagram = models.URLField(null=True, blank=True, verbose_name='Instagram', validators=[URLValidator()])

    class Meta:
        verbose_name = 'Datos de contacto'
        verbose_name_plural = 'Datos de contactos'
    
    def __str__(self):
        return self.telefono + ' - ' + self.email


class OfertaEmpleo(models.Model):
    titulo = models.CharField(max_length=1024, primary_key=True, verbose_name='Título')
    texto = models.TextField(null=True, blank=True, verbose_name='Texto')
    contacto = models.EmailField(null=True, blank=True, verbose_name='Contacto')
    perfil = models.CharField(max_length=1024, null=True, blank=True, verbose_name='Perfil')
    fecha = models.DateField(null=True, blank=True, verbose_name='Fecha')
    titulaciones = models.ManyToManyField(Titulacion, blank=True, verbose_name='Titulaciones')
    fichero = models.FileField(upload_to='files', null=True, blank=True, verbose_name='Fichero')

    class Meta:
        verbose_name = 'Oferta de empleo'
        verbose_name_plural = 'Ofertas de empleo'

    def __str__(self):
        return self.titulo


class RevistaIngenio(models.Model):
    numero = models.IntegerField(primary_key=True, verbose_name='Número')
    imagen = models.ImageField(upload_to='images', null=True, blank=True, verbose_name='Imagen')
    fichero = models.FileField(upload_to='files', verbose_name='Fichero')
    fecha = models.DateField(verbose_name='Fecha')
    tablaContenido = models.TextField(null=True, blank=True, verbose_name='Tabla de contenidos')

    class Meta:
        verbose_name = 'Revista Ingenio'
        verbose_name_plural = 'Revistas Ingenio'
    
    def __str__(self):
        return "Revista número " + str(self.numero)


class AcuerdosEmpresas(models.Model):
    nombre = models.CharField(max_length=1024, primary_key=True, verbose_name='Nombre')
    texto = models.TextField(null=True, blank=True, verbose_name='Texto')
    fichero = models.FileField(upload_to='files', null=True, blank=True, verbose_name='Fichero')
    imagen = models.ImageField(upload_to='images', null=True, blank=True, verbose_name='Imagen')

    class Meta:
        verbose_name = 'Acuerdos con empresas'
        verbose_name_plural = 'Acuerdos con empresas'
    
    def __str__(self):
        return self.nombre


class UsuarioActividad(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name='Usuario')
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, verbose_name='Actividad')
    #dniUsuario = models.CharField(max_length=9, null=False)
    #actividad = models.CharField(max_length=50, null=False)

    class Meta:
        verbose_name = 'Usuario actividad'
        verbose_name_plural = 'Usuarios actividades'
    
    def __str__(self):
        return str(self.usuario) + " - " + str(self.actividad)


class ListaEsperaUsuarioActividad(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name='Usuario')
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, verbose_name='Actividad')
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Lista de espera usuario actividad'
        verbose_name_plural = 'Lista de espera usuarios actividades'
    
    def __str__(self):
        return str(self.usuario) + " - " + str(self.actividad) + " - " + str(self.fecha)


class OfertaEmpleoTitulacion(models.Model):
    #ofertaEmpleo = models.CharField(max_length=200, null=False)
    ofertaEmpleo = models.ForeignKey(OfertaEmpleo, on_delete=models.CASCADE, verbose_name='Oferta de empleo')
    titulacion = models.ForeignKey(Titulacion, on_delete=models.CASCADE, verbose_name='Titulación')

    class Meta:
        verbose_name = 'Ofertas de empleo titulación'
        verbose_name_plural = 'Ofertas de empleo titulaciones'
