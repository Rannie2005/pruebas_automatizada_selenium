from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('notas.urls')),
    path('accounts/login/', RedirectView.as_view(url='/login/', permanent=True)),
]