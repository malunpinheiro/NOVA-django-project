from django.contrib import admin
from .models import Perfume, Mistura


@admin.register(Perfume)
class PerfumeAdmin(admin.ModelAdmin):
    list_display = ("nome", "familia", "preco", "destaque")
    list_filter = ("familia", "destaque")
    search_fields = ("nome", "notas")


@admin.register(Mistura)
class MisturaAdmin(admin.ModelAdmin):
    list_display = ("nome", "criador", "criado_em")
    list_filter = ("criador",)