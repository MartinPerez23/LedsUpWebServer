from django.utils.deprecation import MiddlewareMixin

class DisableCSRFOnWebview(MiddlewareMixin):
    def process_request(self, request):
        if request.headers.get('X-From-Webview') == 'true':
            setattr(request, '_dont_enforce_csrf_checks', True)
