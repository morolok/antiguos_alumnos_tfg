from django import forms
from django.utils.safestring import mark_safe
import antiguos_alumnos_tfg.settings as settings
import gestionBD.models as modelos
from datetime import datetime


class FormularioAltaUsuario(forms.ModelForm):
    dni = forms.CharField(label='Dni', widget=forms.TextInput(attrs={'placeholder': '12345678X', 'maxlength': '9', 'pattern': '^[0-9]{8}[A-Z]', 'title': '8 dígitos y una letra mayúscula'}), required=True)
    contraseña = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    confirmacionContraseña = forms.CharField(label='Confirmación de la contraseña', widget=forms.PasswordInput)
    fechaNacimiento = forms.DateField(label='Fecha de nacimiento', widget=forms.DateInput(attrs={'placeholder': 'dd/mm/aaaa', 'maxlength': '10', 'pattern': '(0[1-9]|[12][0-9]|3[01])[/](0[1-9]|1[012])[/](19|20)\d\d'}), required=True)
    cuentaBancaria = forms.CharField(label='Cuenta bancaria', widget=forms.TextInput(attrs={'placeholder': 'ES2144445555667777777777', 'max_length': '24'}), required=True)
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'usuario@dominio.extension'}), required=True)
    telefono = forms.CharField(label='Teléfono', widget=forms.TextInput(attrs={'patterns': '^[6-7]{1}[0-9]{8}', 'placeholder': '654732897', 'max_length': '9'}), required=True)
    
    class Meta:
        model = modelos.Usuario
        fields = ['nombre', 'apellidos', 'dni', 'fechaNacimiento', 'cuentaBancaria', 'email', 'telefono', 'direccionPostal',
            'usuario', 'contraseña', 'confirmacionContraseña', 'tipo', 'titulacion', 'promocion', 'añoFinalizacion', 'empresa', 
            'comunicaciones', 'juntaRectora']
        labels = {'nombre': 'Nombre', 'apellidos': 'Apellidos', 'direccionPostal': 'Dirección postal', 'usuario': 'Usuario', 
            'tipo': 'Tipo', 'titulacion': 'Titulación', 'promocion': 'Promoción', 'añoFinalizacion': 'Año de finalización', 
            'empresa': 'Empresa', 'comunicaciones': 'Comunicaciones de las actividades', 'juntaRectora': 'Puesto en la junta rectora'}

    def clean(self):
        usuario = self.cleaned_data
        errores = []

        dniUsuario = usuario.get('dni')
        usuarios = modelos.Usuario.objects.filter(dni=dniUsuario)
        if(usuarios.exists()):
            errores.append('Ya existe un usuario con el dni ' + dniUsuario)

        contraseña = usuario.get('contraseña')
        confirmacionContraseña = usuario.get('confirmacionContraseña')

        if(contraseña != confirmacionContraseña):
            errores.append('La confirmación de la contraseña debe ser igual a la contraseña')

        cuentaBancaria = usuario.get('cuentaBancaria')
        if(not cuentaBancaria.startswith('ES21')):
            errores.append('La cuenta bancaria debe empezar por ES21')
        
        if(len(errores) != 0):
            raise forms.ValidationError(errores)

        return usuario


class FormularioAltaRevistaIngenio(forms.ModelForm):
    numero = forms.IntegerField(min_value=1, label = 'Número', required=True)
    fichero = forms.FileField(label='Fichero', required=True)
    fecha = forms.DateField(label='Fecha', widget=forms.DateInput(attrs={'placeholder': 'dd/mm/aaaa', 'maxlength': '10', 'pattern': '(0[1-9]|[12][0-9]|3[01])[/](0[1-9]|1[012])[/](19|20)\d\d'}), required=True)
    
    class Meta:
        model = modelos.RevistaIngenio
        fields = ['numero', 'imagen', 'fichero', 'fecha', 'tablaContenido']
        labels = {'imagen': 'Imagen', 'tablaContenido': 'Tabla de contenidos'}
    
    def clean(self):
        revista = self.cleaned_data
        errores = []
        
        numeroRevista = revista.get('numero')
        revistas = modelos.RevistaIngenio.objects.filter(numero=numeroRevista)
        if(revistas.exists()):
            errores.append('Ya hay una revista con el número ' + str(numeroRevista))

        if(len(errores) != 0):
            raise forms.ValidationError(errores)
        
        return revista


class FormularioAltaActividad(forms.ModelForm):

    fecha = forms.DateField(label='Fecha de la actividad', widget=forms.DateInput(attrs={'placeholder': 'dd/mm/aaaa', 'maxlength': '10', 'pattern': '(0[1-9]|[12][0-9]|3[01])[/](0[1-9]|1[012])[/](19|20)\d\d'}))
    fechaSolicitudesInicio = forms.DateField(label='Fecha de inicio de las solicitudes', widget=forms.DateInput(attrs={'placeholder': 'dd/mm/aaaa', 'maxlength': '10', 'pattern': '(0[1-9]|[12][0-9]|3[01])[/](0[1-9]|1[012])[/](19|20)\d\d'}))
    fechaSolicitudesFin = forms.DateField(label='Fecha de fin de las solicitudes', widget=forms.DateInput(attrs={'placeholder': 'dd/mm/aaaa', 'maxlength': '10', 'pattern': '(0[1-9]|[12][0-9]|3[01])[/](0[1-9]|1[012])[/](19|20)\d\d'}))
    hora = forms.TimeField(label='Hola de la actividad', widget=forms.TimeInput(attrs={'placeholder': 'HH:mm', 'pattern': '([01]?[0-9]|2[0-3]):[0-5][0-9]', 'maxlength': '5'}))
    numeroPlazas = forms.IntegerField(label='Número de plazas', min_value=1)

    class Meta:
        model = modelos.Actividad
        fields = ['titulo', 'descripcion', 'imagen', 'fecha', 'hora', 'numeroPlazas', 'fechaSolicitudesInicio', 
            'fechaSolicitudesFin', 'fichero', 'tipoActividad']

    def clean(self):
        actividad = self.cleaned_data
        errores = []

        tituloActividad = actividad.get('titulo')
        actividades = modelos.Actividad.objects.filter(titulo=tituloActividad)
        if(actividades.exists()):
            errores.append('Ya hay una actividad con ese título')
        
        if(len(errores) != 0):
            raise forms.ValidationError(errores)
        
        return actividad


class FormularioAltaNoticia(forms.ModelForm):

    fecha = forms.DateField(label='Fecha de la noticia', widget=forms.DateInput(attrs={'placeholder': 'dd/mm/aaaa', 'maxlength': '10', 'pattern': '(0[1-9]|[12][0-9]|3[01])[/](0[1-9]|1[012])[/](19|20)\d\d'}))

    class Meta:
        model = modelos.Noticia
        fields = ['titulo', 'texto', 'fecha', 'enlace', 'fichero', 'imagen']

    def clean(self):
        noticia = self.cleaned_data
        errores = []

        tituloNoticia = noticia.get('titulo')
        noticias = modelos.Noticia.objects.filter(titulo=tituloNoticia)
        if(noticias.exists()):
            errores.append('Ya hay una noticia con ese título')

        if(len(errores) != 0):
            raise forms.ValidationError(errores)

        return noticia









