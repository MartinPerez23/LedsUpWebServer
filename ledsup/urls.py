from django.urls import include, path
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'showroom', views.ShowroomViewSet, basename='showroom')
router.register(r'dispositivo', views.DispositivoViewSet, basename='dispositivo')

app_name = 'ledsup'
urlpatterns = [

    path('lista_dispositivos/', views.ListDispositivosPage.as_view(), name='lista_dispositivos'),
    path('lista_showroom/', views.ListShowroomPage.as_view(), name='lista_showroom'),
    path('lista_showroom/probar/', views.ProbarDispositivoView.as_view(), name='probar_dispositivo'),

    path('showroom/', views.ShowroomPage.as_view(), name='showroom'),
    path('showroom/color', views.ColorAction.as_view(), name='color'),
    path('showroom/scroll', views.ScrollAction.as_view(), name='scroll'),
    path('showroom/estrellas', views.EstrellasAction.as_view(), name='estrellas'),
    path('showroom/scan', views.ScanAction.as_view(), name='scan'),

    path('api/', include(router.urls), name='api'),
    path('autenticado/', views.AutenticadoPage.as_view(), name='autenticado'),
    path('descarga/', views.DescargaPage.as_view(), name='descarga'),
    path('dispositivo/create/', views.DispositivoCreate.as_view(), name='crear_dispositivo'),
    path('dispositivo/<int:pk>/', views.DispositivoUpdate.as_view(), name='editar_dispositivo'),
    path('dispositivo/<int:pk>/delete/', views.DispositivoDelete.as_view(), name='eliminar_dispositivo'),

    path('showroom/create/', views.ShowroomCreate.as_view(), name='crear_showroom'),
    path('showroom/<int:pk>/', views.ShowroomUpdate.as_view(), name='editar_showroom'),
    path('showroom/<int:pk>/delete/', views.ShowroomDelete.as_view(), name='eliminar_showroom'),

    path('ordendispositivosenshowroom/<int:pk>/', views.OrdenDispositivosEnShowroomUpdate.as_view(),
         name='editar_orden_dispositivos_en_showroom'),

]
