from django import forms
from django.core.exceptions import ValidationError
from .models import Dispositivo, OrdenDispositivosEnShowroom, Showroom



class DispositivoForm(forms.ModelForm):
    class Meta:
        class_text = "w-full px-3 py-2 rounded-md bg-[#0D1117] text-white border border-gray-700 focus:outline-none focus:ring-2 focus:ring-[#0FF6FF]"
        model = Dispositivo
        fields = [
            'nombre_dispositivo',
            'numero_ip',
            'universo',
            'tamano_paquetes',
            'matriz_x',
            'matriz_y',
            'tipo_led'
        ]
        widgets = {
            'nombre_dispositivo': forms.TextInput(attrs={'class': class_text}),
            'numero_ip': forms.TextInput(attrs={'class': class_text}),
            'universo': forms.NumberInput(attrs={'class': class_text}),
            'tamano_paquetes': forms.NumberInput(attrs={'class': class_text}),
            'matriz_x': forms.NumberInput(attrs={'class': class_text}),
            'matriz_y': forms.NumberInput(attrs={'class': class_text}),
            'tipo_led': forms.Select(attrs={'class': class_text}),
        }

    def clean(self):
        cleaned_data = super().clean()
        ip = cleaned_data.get("numero_ip")
        universo = cleaned_data.get("universo")

        if ip and universo:
            if Dispositivo.objects.filter(numero_ip=ip, universo=universo).exists():
                raise ValidationError("Ya existe un dispositivo con esa IP y ese universo.")

        return cleaned_data


class OrdenDispositivoForm(forms.ModelForm):
    class Meta:
        model = OrdenDispositivosEnShowroom
        fields = ['orden']
        widgets = {
            'orden': forms.Select(
                attrs={
                    'class': "w-full px-3 py-2 rounded-md bg-[#0D1117] text-white border border-gray-700 focus:outline-none focus:ring-2 focus:ring-[#0FF6FF]"}),
        }


class ShowroomForm(forms.ModelForm):
    dispositivos = forms.ModelMultipleChoiceField(
        queryset=Dispositivo.objects.none(),  # Esto lo cargarás en la view con form.fields['dispositivos'].queryset
        widget=forms.SelectMultiple(attrs={
            'class': 'w-full px-3 py-2 rounded-md bg-[#1E1E2F] text-white border border-gray-700 focus:outline-none focus:ring-2 focus:ring-[#0FF6FF] h-40',
            'size': '10',
        }),
        required=False,
    )

    class Meta:
        model = Showroom
        fields = ['nombre_showroom', 'dispositivos']
        widgets = {
            'nombre_showroom': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 rounded-md bg-[#1E1E2F] text-white border border-gray-700 focus:outline-none focus:ring-2 focus:ring-[#0FF6FF]',
                'placeholder': 'Ingrese nombre del showroom',
                'autocomplete': 'off',
            }),
        }

    def clean_dispositivos(self):
        dispositivos = self.cleaned_data.get('dispositivos')
        if dispositivos:
            primera_ip = dispositivos[0].numero_ip
            for disp in dispositivos:
                if disp.numero_ip != primera_ip:
                    raise ValidationError("Todos los dispositivos seleccionados deben tener la misma IP (interfaz DMX).")
        return dispositivos
