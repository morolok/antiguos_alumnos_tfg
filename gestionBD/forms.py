from django import forms
from django.utils.safestring import mark_safe
import antiguos_alumnos_tfg.settings as settings
import gestionBD.models as modelos
from datetime import datetime
import hashlib
import os

class FormularioAltaUsuario(forms.ModelForm):
    dni = forms.CharField(label='Dni', widget=forms.TextInput(attrs={'placeholder': '12345678X', 'maxlength': '9', 'pattern': '^[0-9]{8}[A-Z]', 'title': '8 dígitos y una letra mayúscula'}))
    contraseña = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    confirmacionContraseña = forms.CharField(label='Confirmación de la contraseña', widget=forms.PasswordInput)
    fechaNacimiento = forms.DateField(label='Fecha de nacimiento', widget=forms.DateInput(attrs={'placeholder': 'dd/mm/aaaa', 'maxlength': '10', 'pattern': '(0[1-9]|[12][0-9]|3[01])[/](0[1-9]|1[012])[/](19|20)\d\d'}))
    cuentaBancaria = forms.CharField(label='Cuenta bancaria', widget=forms.TextInput(attrs={'placeholder': 'ES2144445555667777777777', 'max_length': '24'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'usuario@dominio.extension'}))
    telefono = forms.CharField(label='Teléfono', widget=forms.TextInput(attrs={'patterns': '^[6-7]{1}[0-9]{8}', 'placeholder': '654732897', 'max_length': '9'}))
    
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

        contraseña = usuario.get('contraseña')
        confirmacionContraseña = usuario.get('confirmacionContraseña')

        if(contraseña != confirmacionContraseña):
            errores.append('La confirmación de la contraseña debe ser igual a la contraseña')

        cuentaBancaria = usuario.get('cuentaBancaria')
        if(not cuentaBancaria.startswith('ES21')):
            errores.append('La cuenta bancaria debe empezar por ES21')
        
        if(len(errores) != 0):
            raise forms.ValidationError(errores)

        salt = os.urandom(32)
        contraseñaCifrada = hashlib.pbkdf2_hmac('sha256', contraseña.encode('utf-8'), salt, 1, dklen=256)
        confirmacionContraseñaCifrada = hashlib.pbkdf2_hmac('sha256', confirmacionContraseña.encode('utf-8'), salt, 1, dklen=256)
        usuario['contraseña'] = contraseñaCifrada
        usuario['confirmacionContraseña'] = confirmacionContraseñaCifrada

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
        
        numeroRevista = revista.get('numero')
        revistas = modelos.RevistaIngenio.objects.filter(numero=numeroRevista)
        if(revistas.exists()):
            raise forms.ValidationError("Ya hay una revista con el número " + str(numeroRevista))
        
        return revista