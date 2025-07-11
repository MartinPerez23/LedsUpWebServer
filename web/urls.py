from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'errores', views.ErroresViewSet, basename='errores')

app_name = 'web'
urlpatterns = [

                  path('', views.IndexVista.as_view(), name='index'),
                  path("productos/<int:pk>/", views.ProductDetailsPage.as_view(), name="productDetails"),
                  path("eventos", views.EventsPage.as_view(), name="events"),
                  path("contacto", views.ContactFormView.as_view(), name="contact"),
                  path('errores/', views.ErroresListView.as_view(), name='lista_errores'),
                  path('errores/<int:pk>/', views.DetalleErrorView.as_view(), name='detalle_error'),
                  path('api/', include(router.urls), name='api'),
                  path("csrf/", views.csrf_token_view, name="csrf"),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
