from django.contrib import admin

from .models import Receta


@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'fecha_publicacion']
    search_fields = ['titulo', 'autor']
