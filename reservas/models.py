from django.db import models
from datetime import datetime, timedelta


class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    duracion_minutos = models.PositiveIntegerField(help_text="Duración del servicio en minutos")
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} (${self.precio})"


class HorarioDisponible(models.Model):
    DIAS_SEMANA = [
        (0, "Lunes"),
        (1, "Martes"),
        (2, "Miércoles"),
        (3, "Jueves"),
        (4, "Viernes"),
        (5, "Sábado"),
        (6, "Domingo"),
    ]

    dia_semana = models.IntegerField(choices=DIAS_SEMANA)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        ordering = ["dia_semana", "hora_inicio"]
        verbose_name = "Horario disponible"
        verbose_name_plural = "Horarios disponibles"

    def __str__(self):
        return f"{self.get_dia_semana_display()}: {self.hora_inicio} - {self.hora_fin}"


class Reserva(models.Model):
    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("confirmada", "Confirmada"),
        ("cancelada", "Cancelada"),
    ]

    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name="reservas")
    nombre_cliente = models.CharField(max_length=100)
    email_cliente = models.EmailField()
    telefono_cliente = models.CharField(max_length=20)
    fecha = models.DateField()
    hora = models.TimeField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default="pendiente")
    notas = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["fecha", "hora"]

    def __str__(self):
        return f"{self.nombre_cliente} - {self.servicio.nombre} - {self.fecha} {self.hora}"

    def hora_fin(self):
        inicio = datetime.combine(self.fecha, self.hora)
        fin = inicio + timedelta(minutes=self.servicio.duracion_minutos)
        return fin.time()

    @classmethod
    def existe_conflicto(cls, servicio, fecha, hora, excluir_id=None):
        """
        Verifica si ya existe una reserva que se solape con el horario solicitado.
        Esta es la lógica clave para evitar dobles reservas.
        """
        inicio_nuevo = datetime.combine(fecha, hora)
        fin_nuevo = inicio_nuevo + timedelta(minutes=servicio.duracion_minutos)

        reservas_del_dia = cls.objects.filter(
            fecha=fecha,
            servicio=servicio,
        ).exclude(estado="cancelada")

        if excluir_id:
            reservas_del_dia = reservas_del_dia.exclude(id=excluir_id)

        for r in reservas_del_dia:
            inicio_existente = datetime.combine(r.fecha, r.hora)
            fin_existente = inicio_existente + timedelta(minutes=r.servicio.duracion_minutos)

            if inicio_nuevo < fin_existente and fin_nuevo > inicio_existente:
                return True

        return False
