from django.contrib import admin

from .models import Receta


@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'publicada', 'fecha_publicacion']
    list_editable = ['publicada']
    list_filter = ['publicada']
    search_fields = ['titulo', 'autor']
