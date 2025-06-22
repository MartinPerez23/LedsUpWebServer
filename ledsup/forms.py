from django import forms

from .models import Dispositivo, OrdenDispositivosEnShowroom, Showroom


class DispositivoForm(forms.ModelForm):
    class Meta:
        class_text = "w-full px-3 py-2 rounded-md bg-[#0D1117] text-white border border-gray-700 focus:outline-none focus:ring-2 focus:ring-[#0FF6FF]"
        model = Dispositivo
        fields = ['nombre_dispositivo',
                  'numero_ip',
                  'universo',
                  'tamano_paquetes',
                  'matriz_x',
                  'matriz_y',
                  'tipo_led']
        widgets = {
            'nombre_dispositivo': forms.TextInput(attrs={'class': class_text}),
            'numero_ip': forms.TextInput(attrs={'class': class_text}),
            'universo': forms.NumberInput(attrs={'class': class_text}),
            'tamano_paquetes': forms.NumberInput(attrs={'class': class_text}),
            'matriz_x': forms.NumberInput(attrs={'class': class_text}),
            'matriz_y': forms.NumberInput(attrs={'class': class_text}),
            'tipo_led': forms.Select(attrs={'class': class_text}),
        }


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
        queryset=Dispositivo.objects.none(),
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
