from django.contrib import admin
from .models import Servicio, HorarioDisponible, Reserva


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "duracion_minutos", "precio", "activo")
    list_filter = ("activo",)
    search_fields = ("nombre",)


@admin.register(HorarioDisponible)
class HorarioDisponibleAdmin(admin.ModelAdmin):
    list_display = ("dia_semana", "hora_inicio", "hora_fin")
    list_filter = ("dia_semana",)


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ("nombre_cliente", "servicio", "fecha", "hora", "estado")
    list_filter = ("estado", "fecha", "servicio")
    search_fields = ("nombre_cliente", "email_cliente", "telefono_cliente")
    list_editable = ("estado",)
    date_hierarchy = "fecha"
