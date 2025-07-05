import requests
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from oauth2_provider.contrib.rest_framework import OAuth2Authentication, TokenHasScope
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import CustomUserChangeForm, CustomUserCreationForm


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

        if resultado.get('success'):
            return super().form_valid(form)
        else:
            form.add_error(None, "Validación hCaptcha fallida")
            return self.form_invalid(form)


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
