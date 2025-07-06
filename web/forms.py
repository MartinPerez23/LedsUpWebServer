from django import forms
from django.conf import settings
from django.contrib.auth.models import Group
from django.core.mail import send_mail

from .models import Errores


class ContactForm(forms.Form):
    class_text = 'w-full bg-[#1E293B] text-white border border-gray-700 rounded-lg p-2 focus:border-cyan-400 focus:outline-none'

    nombre = forms.CharField(widget=forms.TextInput(attrs={'class': class_text}))
    apellido = forms.CharField(widget=forms.TextInput(attrs={'class': class_text}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': class_text}))
    mensaje = forms.CharField(widget=forms.Textarea(attrs={'class': class_text}))

    def send_email(self):
        subject = 'Nuevo mensaje de contacto'
        message = (
            f"Nombre: {self.cleaned_data['nombre']}\n"
            f"Apellido: {self.cleaned_data['apellido']}\n"
            f"Correo: {self.cleaned_data['email']}\n\n"
            f"Mensaje:\n{self.cleaned_data['mensaje']}"
        )
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [settings.EMAIL_HOST_USER]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        admin_group = Group.objects.filter(name="Administrador Web").first()
        if admin_group:
            self.fields['asignado_a'].queryset = admin_group.user_set.all()
        else:
            self.fields['asignado_a'].queryset = self.fields['asignado_a'].queryset.none()
