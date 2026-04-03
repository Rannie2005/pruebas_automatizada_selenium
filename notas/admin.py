from django.contrib import admin
from .models import Nota

@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_creacion', 'fecha_actualizacion')
    search_fields = ('titulo', 'contenido')
    list_filter = ('fecha_creacion',)