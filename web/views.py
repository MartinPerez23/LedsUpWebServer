from django.utils import timezone
from django.views import generic

from .models import Producto, TipoProducto


class IndexVista(generic.ListView):

    template_name = 'web/index.html'
    context_object_name = 'lista_ultimos_productos'

    def get_queryset(self):

        return Producto.objects.filter(
            fecha_creacion__lte=timezone.now()
        ).order_by('-fecha_creacion')[:5]

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(IndexVista, self).get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        context['listado_tipos_productos'] = TipoProducto.objects.get_queryset()
        context['listado_productos'] = Producto.objects.get_queryset()
        return context
