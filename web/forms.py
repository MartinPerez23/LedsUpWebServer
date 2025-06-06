from django import forms

from .models import Errores


class ContactForm(forms.Form):
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    apellido = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    mensaje = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass


class ErrorUpdateForm(forms.ModelForm):
    class Meta:
        model = Errores
        fields = ['asignado_a', 'estado', 'comentarios']
        widgets = {
            'comentarios': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'asignado_a': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }
