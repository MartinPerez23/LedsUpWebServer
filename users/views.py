import requests
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from oauth2_provider.contrib.rest_framework import OAuth2Authentication, TokenHasScope
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import CustomUserChangeForm, CustomUserCreationForm, CustomAuthenticationForm


class SignUpView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'registration/user_form.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        hcaptcha_response = self.request.POST.get('h-captcha-response')
        data = {
            'secret': settings.HCAPTCHA_SECRET_KEY,
            'response': hcaptcha_response
        }

        r = requests.post('https://hcaptcha.com/siteverify', data=data)
        resultado = r.json()

        if not resultado.get('success'):
            form.add_error(None, "Validación hCaptcha fallida")
            return self.form_invalid(form)

        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # Agregar a grupo predeterminado
        grupo, _ = Group.objects.get_or_create(name="Cliente")
        user.groups.add(grupo)

        # Enviar email de activación
        current_site = get_current_site(self.request)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        link = f"https://{current_site.domain}/activar/{uid}/{token}/"

        mensaje = render_to_string("registration/email_verificacion.html", {
            "user": user,
            "link": link,
        })

        send_mail(
            subject="Activa tu cuenta",
            message=mensaje,
            from_email="noreply@tusitio.com",
            recipient_list=[user.email],
            fail_silently=False,
        )

        messages.success(self.request, "Registro exitoso. Revisa tu correo para activar la cuenta.")
        return redirect(self.success_url)


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'registration/user_edit.html'
    success_url = reverse_lazy('user_profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'registration/user_confirm_delete.html'
    success_url = reverse_lazy('web:index')

    def get_object(self, queryset=None):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.dispositivo_set.all().delete()
        return super().delete(request, *args, **kwargs)


class UserInfoGet(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated, TokenHasScope]
    required_scopes = ['user_info']

    def get(self, request, *args, **kwargs):
        user = request.user
        return Response({
            'user_name': user.username,
        })


def logout_closeWS(request):
    user_id = request.user.id
    logout(request)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user_id}",
        {
            "type": "kick_user"
        }
    )

    return redirect('login')


class LoginConHCaptchaView(LoginView):
    template_name = 'registration/login.html'
    form_class = CustomAuthenticationForm

    def form_valid(self, form):
        hcaptcha_response = self.request.POST.get('h-captcha-response')
        data = {
            'secret': settings.HCAPTCHA_SECRET_KEY,
            'response': hcaptcha_response
        }

        r = requests.post('https://hcaptcha.com/siteverify', data=data)
        resultado = r.json()

        if resultado.get('success'):
            return super().form_valid(form)
        else:
            form.add_error(None, "Validación hCaptcha fallida")
            return self.form_invalid(form)


def activar_cuenta(request, uid, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Tu cuenta ha sido activada correctamente. Ya podés iniciar sesión.")
        return redirect('login')
    else:
        messages.error(request, "El enlace es inválido o ha expirado.")
        return redirect('register')
