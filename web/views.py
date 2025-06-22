from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from oauth2_provider.contrib.rest_framework import TokenHasScope
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET
from .forms import ContactForm, ErrorUpdateForm
from .models import Producto, TipoProducto, Evento, Errores
from .serializers import ErroresSerializer
from django.contrib.auth import logout
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class IndexVista(generic.ListView):
    template_name = 'web/index.html'
    context_object_name = 'lista_ultimos_productos'

    def get_queryset(self):
        return Producto.objects.filter(
            fecha_creacion__lte=timezone.now()
        ).order_by('-fecha_creacion')[:5]

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        context['listado_tipos_productos'] = TipoProducto.objects.get_queryset()
        context['listado_productos'] = Producto.objects.get_queryset()

        return context


class ContactFormView(generic.FormView):
    template_name = 'web/contacto.html'
    form_class = ContactForm
    success_url = reverse_lazy('web:contact')

    def form_valid(self, form):
        messages.success(self.request, 'Mensaje enviado, ¡gracias por contactar con nosotros!')
        form.send_email()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        context['listado_tipos_productos'] = TipoProducto.objects.get_queryset()
        context['listado_productos'] = Producto.objects.get_queryset()

        return context


class EventsPage(generic.ListView):
    template_name = 'web/eventos.html'
    context_object_name = 'events_list'

    def get_queryset(self):
        return Evento.objects.get_queryset()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        context['listado_tipos_productos'] = TipoProducto.objects.get_queryset()
        context['listado_productos'] = Producto.objects.get_queryset()

        return context


class ProductDetailsPage(generic.DetailView):
    template_name = 'web/producto.html'
    model = Producto

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['listado_tipos_productos'] = TipoProducto.objects.get_queryset()
        context['listado_productos'] = Producto.objects.get_queryset()

        return context


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
        context['now'] = timezone.now()
        context['listado_tipos_productos'] = TipoProducto.objects.get_queryset()
        context['listado_productos'] = Producto.objects.get_queryset()

        # Estados
        context['estado_actual'] = self.request.GET.get('estado', '')
        context['opciones_estado'] = Errores._meta.get_field('estado').choices

        # Solo usuarios staff
        from django.contrib.auth.models import User
        opciones_asignado_a = [(user.id, user.username) for user in User.objects.filter(is_staff=True)]
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
        context['now'] = timezone.now()
        context['listado_tipos_productos'] = TipoProducto.objects.get_queryset()
        context['listado_productos'] = Producto.objects.get_queryset()

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

############################################   API   ############################################

class ErroresViewSet(viewsets.ModelViewSet):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated, TokenHasScope]
    required_scopes = ['errors']

    queryset = Errores.objects.all().order_by('-fecha_creacion')
    serializer_class = ErroresSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class UserInfoGet(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated, TokenHasScope]
    required_scopes = ['user_info']

    def get(self, request, *args, **kwargs):
        user = request.user
        return Response({
            'user_name': user.username,
        })

@require_GET
@ensure_csrf_cookie
def csrf_token_view(request):
    return JsonResponse({'detail': 'CSRF cookie set'})
