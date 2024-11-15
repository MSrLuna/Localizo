from django import forms
from .models import Usuario

class AddUserForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirmar Contraseña"
    )

    class Meta:
        model = Usuario
        fields = ['rut', 'nombre', 'email', 'telefono', 'direccion', 'password', 'rol']

        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.NumberInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'estado': forms.HiddenInput(),
            'rol': forms.HiddenInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden")

        return cleaned_data


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Tu nombre'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Tu correo electrónico'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Escribe tu mensaje', 'rows': 4}), required=True)
