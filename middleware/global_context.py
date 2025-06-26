from django.conf import settings

from web.models import TipoProducto, Producto


class GlobalVariablesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_template_response(self, request, response):
        # Agrega variables al contexto global
        response.context_data = response.context_data or {}
        response.context_data['HCAPTCHA_SITE_KEY'] = settings.HCAPTCHA_SITE_KEY
        response.context_data['listado_tipos_productos'] = TipoProducto.objects.all()
        response.context_data['listado_productos'] = Producto.objects.all()
        return response
