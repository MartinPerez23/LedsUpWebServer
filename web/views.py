from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from .forms import ContactForm
from .models import Producto, TipoProducto, Galeria


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


class GalleryPage(generic.ListView):
    template_name = 'web/galeria.html'
    context_object_name = 'gallery_list'

    def get_queryset(self):
        return Galeria.objects.get_queryset()

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
