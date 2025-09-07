from django.contrib import admin
from .models import Premio, Numero

@admin.register(Premio)
class PremioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'descripcion')
    list_filter = ('categoria',)
    search_fields = ('nombre',)

@admin.register(Numero)
class NumeroAdmin(admin.ModelAdmin):
    list_display = ('valor', 'hoja', 'disponible', 'nombre_completo', 'telefono', 'gmail')
    list_editable = ('disponible', 'nombre_completo', 'telefono', 'gmail')
    search_fields = ('valor', 'nombre_completo', 'telefono', 'gmail')
    list_filter = ('hoja', 'disponible')
    ordering = ('valor',)
