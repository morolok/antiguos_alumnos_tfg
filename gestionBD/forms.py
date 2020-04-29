from django import forms
import antiguos_alumnos_tfg.settings as settings
import gestionBD.models as modelos
from datetime import datetime

class FormularioAltaUsuario(forms.ModelForm):
    contraseña = forms.CharField(widget=forms.PasswordInput)
    confirmacionContraseña = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = modelos.Usuario
        fields = ['nombre', 'apellidos', 'dni', 'fechaNacimiento', 'cuentaBancaria', 'email', 'telefono', 'direccionPostal',
            'usuario', 'contraseña', 'confirmacionContraseña', 'tipo', 'titulacion', 'promocion', 'añoFinalizacion', 'empresa', 
            'comunicaciones', 'juntaRectora']

class FormularioAltaRevistaIngenio(forms.ModelForm):
    numero = forms.IntegerField(min_value=1, label = "Número", required=True)
    fichero = forms.FileField(label="Fichero", required=True)
    fecha = forms.DateField(label="Fecha", widget=forms.DateInput(attrs={'placeholder': 'dd/mm/aaaa'}), required=True)
    
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