import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from oauth2_provider.contrib.rest_framework import TokenHasScope
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .forms import ContactForm, ErrorUpdateForm
from .models import Producto, Evento, Errores, TipoProducto
from .serializers import ErroresSerializer


def get_context():
    return {
        "HCAPTCHA_SITE_KEY": settings.HCAPTCHA_SITE_KEY,
        "listado_tipos_productos": TipoProducto.objects.all(),
        "listado_productos": Producto.objects.all(),
    }


def custom_400(request, exception):
    return render(request, "400.html", context=get_context(), status=400)


def custom_403(request, exception):
    return render(request, "403.html", context=get_context(), status=403)


def custom_404(request, exception):
    return render(request, "404.html", context=get_context(), status=404)


def custom_500(request):
    return render(request, "500.html", context=get_context(), status=500)


class IndexVista(generic.ListView):
    template_name = 'web/index.html'
    context_object_name = 'lista_ultimos_productos'

    def get_queryset(self):
        return Producto.objects.filter(
            fecha_creacion__lte=timezone.now()
        ).order_by('-fecha_creacion')[:5]


class ContactFormView(generic.FormView):
    template_name = 'web/contacto.html'
    form_class = ContactForm
    success_url = reverse_lazy('web:contact')

    def form_valid(self, form):
        if getattr(settings, "HCAPTCHA_ENABLED", True):
            hcaptcha_response = self.request.POST.get('h-captcha-response')
            data = {
                'secret': settings.HCAPTCHA_SECRET_KEY,
                'response': hcaptcha_response
            }

            r = requests.post('https://hcaptcha.com/siteverify', data=data)
            resultado = r.json()

            if resultado.get('success'):
                try:
                    form.send_email()
                    messages.success(self.request, 'Mensaje enviado, ¡gracias por contactar con nosotros!')

                    return super().form_valid(form)

                except Exception:
                    messages.error(self.request, f'Error al enviar el mensaje. Intentelo nuevamente mas tarde.')
                    return self.form_invalid(form)

            else:
                form.add_error(None, "Validación hCaptcha fallida")
                return self.form_invalid(form)

        return self.form_invalid(form)


class EventsPage(generic.ListView):
    template_name = 'web/eventos.html'
    context_object_name = 'events_list'

    def get_queryset(self):
        return Evento.objects.get_queryset()


class ProductDetailsPage(generic.DetailView):
    template_name = 'web/producto.html'
    model = Producto


class ErroresListView(LoginRequiredMixin, generic.ListView):
    model = Errores
    template_name = 'web/lista_errores.html'
    context_object_name = 'errores'

    def get_queryset(self):
        queryset = super().get_queryset()
        estado = self.request.GET.get('estado')
        asignado = self.request.GET.get('asignado')

        if estado:
            queryset = queryset.filter(estado=estado)

        if asignado:
            queryset = queryset.filter(asignado_a_id=asignado)

        return queryset.order_by('-fecha_creacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        opciones_asignado_a = [(user.id, user.username) for user in User.objects.filter(is_staff=True)]

        context['estado_actual'] = self.request.GET.get('estado', '')
        context['opciones_estado'] = Errores._meta.get_field('estado').choices
        context['asignado_actual'] = self.request.GET.get('asignado', '')
        context['opciones_asignado_a'] = opciones_asignado_a

        return context


class DetalleErrorView(LoginRequiredMixin, generic.DetailView):
    model = Errores
    template_name = 'web/detalle_error.html'
    context_object_name = 'error'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ErrorUpdateForm(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ErrorUpdateForm(request.POST, instance=self.object)
        if form.is_valid():
            form.save()
            messages.success(request, "Cambios guardados correctamente")
        else:
            messages.error(request, "Hay errores en el formulario.")
        return redirect('web:lista_errores')


############################################   API   ############################################

class ErroresViewSet(viewsets.ModelViewSet):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated, TokenHasScope]
    required_scopes = ['errors']

    queryset = Errores.objects.all().order_by('-fecha_creacion')
    serializer_class = ErroresSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


@require_GET
@ensure_csrf_cookie
def csrf_token_view(request):
    return JsonResponse({'detail': 'CSRF cookie set'})
