from django import forms

from .models import Errores


class ContactForm(forms.Form):
    class_text = 'w-full bg-[#1E293B] text-white border border-gray-700 rounded-lg p-2 focus:border-cyan-400 focus:outline-none'

    nombre = forms.CharField(widget=forms.TextInput(attrs={'class': class_text}))
    apellido = forms.CharField(widget=forms.TextInput(attrs={'class': class_text}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': class_text}))
    mensaje = forms.CharField(widget=forms.Textarea(attrs={'class': class_text}))

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass


class ErrorUpdateForm(forms.ModelForm):
    class Meta:
        class_text = "w-full px-3 py-2 rounded-md bg-[#0D1117] text-white border border-gray-700"

        model = Errores
        fields = ['asignado_a', 'estado', 'comentarios']
        widgets = {
            'comentarios': forms.Textarea(attrs={'rows': 4, 'class': class_text}),
            'asignado_a': forms.Select(attrs={'class': class_text}),
            'estado': forms.Select(attrs={'class': class_text}),
        }
