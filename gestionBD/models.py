from django.db import models

# Create your models here.

class JuntaRectora(models.Model):
    puesto = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.puesto

class Titulacion(models.Model):
    nombre = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.nombre

class TipoActividad(models.Model):
    tipo = models.CharField(max_length=30, primary_key=True)

    def __str__(self):
        return self.tipo

class TipoUsuario(models.Model):
    tipo = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.tipo

class Usuario(models.Model):
    nombre = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=50)
    dni = models.CharField(max_length=9, primary_key=True)
    fechaNacimiento = models.DateField()
    cuentaBancaria = models.CharField(max_length=24)
    email = models.EmailField()
    telefono = models.CharField(max_length=9)
    direccionPostal = models.TextField()
    usuario = models.CharField(max_length=20)
    contraseña = models.CharField(max_length=256)
    tipo = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)
    titulacion = models.ForeignKey(Titulacion, on_delete=models.CASCADE)
    promocion = models.CharField(max_length=11)
    añoFinalizacion = models.CharField(max_length=4)
    empresa = models.CharField(max_length=150)
    comunicaciones = models.BooleanField()
    juntaRectora = models.ForeignKey(JuntaRectora, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre + " " + self.apellidos + " - " + self.dni

class Noticia(models.Model):
    titulo = models.CharField(max_length=50)
    texto = models.TextField()
    fecha = models.DateTimeField()
    enlace = models.CharField(max_length=256, null=True, blank=True)

class Actividad(models.Model):
    titulo = models.CharField(max_length=50, primary_key=True)
    descripcion = models.CharField(max_length=1024)
    textoReseña = models.TextField()
    imagen = models.ImageField(upload_to='images', max_length=256)
    fecha = models.DateField()
    hora = models.CharField(max_length=5)
    enlaceAlbum = models.CharField(max_length=256, null=True, blank=True)
    tipoActividad = models.ForeignKey(TipoActividad, on_delete=models.CASCADE)

class DatosDeContacto(models.Model):
    telefono = models.CharField(max_length=9)
    email = models.EmailField()
    horario = models.TextField()
    horarioEspecial = models.TextField()
    ubicacion = models.CharField(max_length=100, null=True, blank=True)
    facebook = models.CharField(max_length=256, null=True, blank=True)
    twitter = models.CharField(max_length=256, null=True, blank=True)
    instagram = models.CharField(max_length=256, null=True, blank=True)

class OfertaEmpleo(models.Model):
    titulo = models.CharField(max_length=200, primary_key=True)
    texto = models.TextField()
    contacto = models.CharField(max_length=100, null=True, blank=True)
    perfil = models.CharField(max_length=100)
    fecha = models.DateField()
    titulaciones = models.CharField(max_length=24)

class RevistaIngenio(models.Model):
    numero = models.IntegerField(primary_key=True)
    imagen = models.ImageField(upload_to='images', max_length=256, null=True, blank=True)
    fichero = models.FileField(upload_to='files')
    fecha = models.DateField()
    tablaContenido = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return "Revista número " + str(self.numero)

class AcuerdosEmpresas(models.Model):
    nombre = models.CharField(max_length=100)
    fichero = models.FileField(upload_to='files')
    texto = models.TextField(null=True, blank=True)

class UsuarioActividad(models.Model):
    dniUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    #dniUsuario = models.CharField(max_length=9, null=False)
    #actividad = models.CharField(max_length=50, null=False)

class OfertaEmpleoTitulacion(models.Model):
    #ofertaEmpleo = models.CharField(max_length=200, null=False)
    ofertaEmpleo = models.ForeignKey(OfertaEmpleo, on_delete=models.CASCADE)
    titulacion = models.ForeignKey(Titulacion, on_delete=models.CASCADE)
