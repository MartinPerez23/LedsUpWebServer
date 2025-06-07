from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from oauth2_provider.contrib.rest_framework import TokenHasScope
from .forms import ContactForm, ErrorUpdateForm
from .models import Producto, TipoProducto, Evento, Errores
from .serializers import ErroresSerializer


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
        if estado:
            queryset = queryset.filter(estado=estado)
        return queryset.order_by('-fecha_creacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['listado_tipos_productos'] = TipoProducto.objects.get_queryset()
        context['listado_productos'] = Producto.objects.get_queryset()
        context['estado_actual'] = self.request.GET.get('estado', '')
        context['opciones_estado'] = Errores._meta.get_field('estado').choices

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


############################################   API   ############################################

class ErroresViewSet(viewsets.ModelViewSet):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated, TokenHasScope]
    required_scopes = ['errors']

    queryset = Errores.objects.all().order_by('-fecha_creacion')
    serializer_class = ErroresSerializer

    def create(self, request, *args, **kwargs):
        print("HEADERS:", dict(request.headers))
        print("USER:", request.user)
        print("AUTH:", request.auth)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
