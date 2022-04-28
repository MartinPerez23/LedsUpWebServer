from django.urls import path

from . import views

app_name = 'web'
urlpatterns = [

    path('', views.IndexVista.as_view(), name='index'),
]
