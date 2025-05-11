from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'web'
urlpatterns = [

                  path('', views.IndexVista.as_view(), name='index'),
                  path("productos/<int:pk>/", views.ProductDetailsPage.as_view(), name="productDetails"),
                  path("galeria", views.GalleryPage.as_view(), name="gallery"),
                  path("contacto", views.ContactFormView.as_view(), name="contact"),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
