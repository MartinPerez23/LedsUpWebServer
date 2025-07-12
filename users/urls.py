from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from . import views

urlpatterns = [
                  path('', include('django.contrib.auth.urls')),
                  path('signup/', views.SignUpView.as_view(), name='user_signup'),
                  path('profile/edit/', views.UserProfileUpdateView.as_view(), name='user_profile'),
                  path('profile/delete/', views.UserDeleteView.as_view(), name='user_delete'),
                  path('logout/', views.logout_closeWS, name="logout"),
                  path('login/', views.LoginConHCaptchaView.as_view(), name='login'),
                  path('oauth2/userinfo/', views.UserInfoGet.as_view(), name='user_info'),
                  path('activar/<uid>/<token>/', views.activar_cuenta, name='activar_cuenta'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
