from django import forms
import gestionBD.models as modelos

class FormularioAltaUsuario(forms.ModelForm):
    contraseña = forms.CharField(widget=forms.PasswordInput)
    confirmacionContraseña = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = modelos.Usuario
        fields = ['nombre', 'apellidos', 'dni', 'fechaNacimiento', 'cuentaBancaria', 'email', 'telefono', 'direccionPostal',
            'usuario', 'contraseña', 'confirmacionContraseña', 'tipo', 'titulacion', 'promocion', 'añoFinalizacion', 'empresa', 
            'comunicaciones', 'juntaRectora']