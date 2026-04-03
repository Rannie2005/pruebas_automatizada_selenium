from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.lista_notas, name='lista_notas'),
    path('crear/', views.crear_nota, name='crear_nota'),
    path('editar/<int:nota_id>/', views.editar_nota, name='editar_nota'),
    path('eliminar/<int:nota_id>/', views.eliminar_nota, name='eliminar_nota'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    
    # URLs de recuperación de contraseña
    path('reset-password/', 
        auth_views.PasswordResetView.as_view(template_name='notas/reset_password.html'),
        name='password_reset'),
    path('reset-password/enviado/', 
        auth_views.PasswordResetDoneView.as_view(template_name='notas/reset_password_done.html'),
        name='password_reset_done'),
    path('reset-password/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='notas/reset_password_confirm.html'),
        name='password_reset_confirm'),
    path('reset-password/completo/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='notas/reset_password_complete.html'),
        name='password_reset_complete'),
]