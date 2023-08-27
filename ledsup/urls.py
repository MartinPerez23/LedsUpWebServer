from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'showroom', views.ShowroomViewSet, basename='showroom')
router.register(r'dispositivo', views.DispositivoViewSet, basename='dispositivo')

app_name = 'ledsup'
urlpatterns = [

    path('lista_dispositivos/', views.ListDispositivosPage.as_view(), name='lista_dispositivos'),
    path('lista_dispositivos/probar', views.ListDispositivosPage.probar_dispositivo, name='probar'),
    path('lista_showroom/', views.ListShowroomPage.as_view(), name='lista_showroom'),

    path('showroom/', views.ShowroomPage.as_view(), name='showroom'),
    path('showroom/color', views.ShowroomPage.color, name='color'),
    path('showroom/scroll', views.ShowroomPage.scroll, name='scroll'),
    path('showroom/estrellas', views.ShowroomPage.estrellas, name='estrellas'),
    path('showroom/scan', views.ShowroomPage.scan, name='scan'),

    path('api/', include(router.urls), name='api'),

    path('dispositivo/create/', views.DispositivoCreate.as_view(), name='crear_dispositivo'),
    path('dispositivo/<int:pk>/', views.DispositivoUpdate.as_view(), name='editar_dispositivo'),
    path('dispositivo/<int:pk>/delete/', views.DispositivoDelete.as_view(), name='eliminar_dispositivo'),

    path('showroom/create/', views.ShowroomCreate.as_view(), name='crear_showroom'),
    path('showroom/<int:pk>/', views.ShowroomUpdate.as_view(), name='editar_showroom'),
    path('showroom/<int:pk>/delete/', views.ShowroomDelete.as_view(), name='eliminar_showroom'),

    path('ordendispositivosenshowroom/<int:pk>/', views.OrdenDispositivosEnShowroomUpdate.as_view(), name='editar_orden_dispositivos_en_showroom'),

    path('wsremoteandlocal/<str:room_name>/', views.room, name='room'),

]
