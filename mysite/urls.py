"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from oauth2_provider import urls as oauth2_urls

handler400 = 'web.views.custom_400'
handler403 = 'web.views.custom_403'
handler404 = 'web.views.custom_404'
handler500 = 'web.views.custom_500'

urlpatterns = [

    path('', include('web.urls')),
    path('', include('users.urls')),
    path('ledsup/', include('ledsup.urls')),
    path('admin/', admin.site.urls, name='admin'),
    path('o/', include(oauth2_urls)),

]
