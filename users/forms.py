from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


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
        widget=forms.EmailInput(),
        label='Correo electrónico'
    )

    username = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'maxlength': '20'}),
        label='Nombre de usuario'
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email'] + list(UserCreationForm.Meta.fields)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].help_text = None

        class_text = 'w-full bg-[#1E293B] text-white border border-gray-700 rounded-lg p-2 focus:border-cyan-400 focus:outline-none'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = class_text

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ya existe un usuario registrado con este correo electrónico.")
        return email


class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                "Esta cuenta no está activada. Revisá tu correo electrónico para activarla.",
                code='inactive',
            )