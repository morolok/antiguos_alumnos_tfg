from django.db import models

# Create your models here.

class Usuario(models.Model):
    ASOCIADO = 'ASOCIADO'
    GESTOR = 'GESTOR'
    ADMINISTRADOR = 'ADMINISTRADOR'
    TIPO_USUARIO = (
        (ASOCIADO, u'Asociado'),
        (GESTOR, u'Gestor'),
        (ADMINISTRADOR, u'Administrador')
    )

    NO = 'NO'
    PRESIDENTE = 'PRESIDENTE'
    VICEPRESIDENTE = 'VICEPRESIDENTE'
    SECRETARIO = 'SECRETARIO'
    TESORERO = 'TESORERO'
    VOCAL = 'VOCAL'
    PUESTO_JUNTA_RECTORA = (
        (NO, u'No'),
        (PRESIDENTE, u'Presidente'),
        (VICEPRESIDENTE, u'Vicepresidente'),
        (SECRETARIO, u'Secretario'),
        (TESORERO, u'Tesorero'),
        (VOCAL, u'Vocal')
    )

    nombre = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=50)
    dni = models.CharField(max_length=9, primary_key=True)
    fechaNacimiento = models.DateField()
    cuentaBancaria = models.CharField(max_length=24)
    email = models.EmailField()
    telefono = models.CharField(max_length=9)
    direccionPostal = models.CharField(max_length=100)
    usuario = models.CharField(max_length=20)
    contraseña = models.CharField(max_length=256)
    tipo = models.CharField(max_length=20, choices=TIPO_USUARIO)
    titulacion = models.CharField(max_length=100)
    promocion = models.CharField(max_length=11)
    añoFinalizacion = models.CharField(max_length=4)
    empresa = models.CharField(max_length=150)
    comunicaciones = models.BooleanField()
    juntaRectora = models.CharField(max_length=20, choices=PUESTO_JUNTA_RECTORA)

class Noticia(models.Model):
    titulo = models.CharField(max_length=50)
    texto = models.CharField(max_length=1024)
    fecha = models.DateTimeField()
    enlace = models.CharField(max_length=256)

class Actividad(models.Model):
    titulo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=1024)
    textoReseña = models.CharField(max_length=1024)
    imagen = models.ImageField(upload_to='images', max_length=256)

class DatosDeContacto(models.Model):
    telefono = models.CharField(max_length=9)
    email = models.EmailField()
    horario = models.CharField(max_length=100)
    horarioEspecial = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=100)
    facebook = models.CharField(max_length=256, null=True)
    twitter = models.CharField(max_length=256, null=True)
    instagram = models.CharField(max_length=256, null=True)

class JuntaRectora(models.Model):
    dniUsuario = models.CharField(max_length=9, primary_key=True)

class Titulacion(models.Model):
    AEROESPACIAL = 'AEROESPACIAL'
    CIVIL = 'CIVIL'
    TECNOLOGIAS_INDUSTRIALES = 'TECNOLOGIAS_INDUSTRIALES'
    QUIMICA = 'QUIMICA'
    TELECOMUNICACION = 'TELECOMUNICACION'
    ELECTRONICA_ROBOTICA_MECATRONICA = 'ELECTRONICA_ROBOTICA_MECATRONICA'
    ENERGIA = 'ENERGIA'
    ORGANIZACION_INDUSTRIAL = 'ORGANIZACION_INDUSTRIAL'
    NOMBRE_TITULACION = (
        (AEROESPACIAL, u'Ingeniería Aeroespacial'),
        (CIVIL, u'Ingeniería Civil'),
        (TECNOLOGIAS_INDUSTRIALES, u'Ingeniería de las Tecnologías Industriales'),
        (QUIMICA, u'Ingeniería Química'),
        (TELECOMUNICACION, u'Ingeniería de las Tecnologías de la Telecomunicación'),
        (ELECTRONICA_ROBOTICA_MECATRONICA, u'Ingeniería Electrónica, Robótica y Mecatrónica'),
        (ENERGIA, u'Ingeniería de la Energía'),
        (ORGANIZACION_INDUSTRIAL, u'Ingeniería de Organización Industrial')
    )

    nombre = models.CharField(max_length=100, choices=NOMBRE_TITULACION)

class TipoActividad(models.Model):
    VISITA_TECNICA = 'VISITA_TECNICA'
    VISITA_CULTURAL = 'VISITA_CULTURAL'
    CONFERENCIA = 'CONFERENCIA'
    EXPOSICION = 'EXPOSICION'
    PADEL = 'PADEL'
    TENIS = 'TENIS'
    GOLF = 'GOLF'
    SENDERISMO = 'SENDERISMO'
    BICICLETA = 'BICICLETA'
    REUNION_PROMOCION = 'REUNION_PROMOCION'
    CONCURSO = 'CONCURSO'
    ENCUENTRO_ASOCIADOS = 'ENCUENTRO_ASOCIADOS'
    CONCIERTO = 'CONCIERTO'
    ACTIVIDAD_FAMILIAR = 'ACTIVIDAD_FAMILIAR'
    CURSO = 'CURSO'
    OTRA = 'OTRA'
    TIPO_ACTIVIDAD = (
        (VISITA_TECNICA, u'Visita técnica'),
        (VISITA_CULTURAL, u'Visita cultural'),
        (CONFERENCIA, u'Conferencia'),
        (EXPOSICION, u'Exposición'),
        (PADEL, u'Pádel'),
        (TENIS, u'Tenis'),
        (GOLF, u'Golf'),
        (SENDERISMO, u'Senderismo'),
        (BICICLETA, u'Bicicleta'),
        (REUNION_PROMOCION, u'Reunión de promoción'),
        (CONCURSO, u'Concurso'),
        (ENCUENTRO_ASOCIADOS, u'Encuentro de asociados'),
        (CONCIERTO, u'Concierto'),
        (ACTIVIDAD_FAMILIAR, u'Actividad familiar'),
        (CURSO, u'Curso'),
        (OTRA, u'Otra')
    )

    tipo = models.CharField(max_length=30, choices=TIPO_ACTIVIDAD)

class OfertaEmpleo(models.Model):
    texto = models.CharField(max_length=1024)
    contacto = models.CharField(max_length=100)
    perfil = models.CharField(max_length=100)
    fecha = models.DateField()
    titulaciones = models.CharField(max_length=24)

class RevistaIngenio(models.Model):
    numero = models.IntegerField()
    imagen = models.ImageField(upload_to='images', max_length=256)
    fichero = models.FileField(upload_to='files')
    fecha = models.DateField()

class AcuerdosEmpresas(models.Model):
    nombre = models.CharField(max_length=100)
    fichero = models.FileField(upload_to='files')
