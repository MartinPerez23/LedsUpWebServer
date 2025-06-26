from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

        class_text = 'w-full bg-[#1E293B] text-white border border-gray-700 rounded-lg p-2 focus:border-cyan-400 focus:outline-none'

        widgets = {
            'username': forms.TextInput(attrs={'class': class_text}),
            'email': forms.EmailInput(attrs={'class': class_text}),
            'first_name': forms.TextInput(attrs={'class': class_text}),
            'last_name': forms.TextInput(attrs={'class': class_text}),
        }
        help_texts = {
            'username': None,
        }


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full bg-[#1E293B] text-white border border-gray-700 rounded-lg p-2 focus:border-cyan-400 focus:outline-none'
        }),
        label='Correo electrónico'
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email'] + list(UserCreationForm.Meta.fields)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].help_text = None

        for field_name, field in self.fields.items():
            if 'class' in field.widget.attrs:
                field.widget.attrs[
                    'class'] += ' w-full bg-[#1E293B] text-white border border-gray-700 rounded-lg p-2 focus:border-cyan-400 focus:outline-none'
            else:
                field.widget.attrs[
                    'class'] = 'w-full bg-[#1E293B] text-white border border-gray-700 rounded-lg p-2 focus:border-cyan-400 focus:outline-none'
