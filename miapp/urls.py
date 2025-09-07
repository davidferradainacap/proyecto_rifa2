from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView, LoginView
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('numeros/', views.numeros, name='numeros'), # Hoja 1
    path('numeros/hoja2/', views.numeros_hoja2, name='numeros_hoja2'),
    path('numeros/hoja3/', views.numeros_hoja3, name='numeros_hoja3'),
    path('numeros/hoja4/', views.numeros_hoja4, name='numeros_hoja4'),
    path('admin-numeros/', views.panel_admin_numeros, name='admin_numeros'),
    path('premios/', views.premios, name='premios'),
    path('numero/<int:pk>/', views.numero_detalle, name='numero_detalle'),
    path('iniciar-ruleta/', views.iniciar_ruleta, name='iniciar_ruleta'),
    path('estado-ruleta/', views.estado_ruleta, name='estado_ruleta'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('contacto/', views.contacto, name='contacto'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)