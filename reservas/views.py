from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Servicio, Reserva
from .forms import ReservaForm


def catalogo(request):
    servicios = Servicio.objects.filter(activo=True)
    return render(request, "reservas/catalogo.html", {"servicios": servicios})


def reservar(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id, activo=True)

    if request.method == "POST":
        form = ReservaForm(request.POST)
        if form.is_valid():
            fecha = form.cleaned_data["fecha"]
            hora = form.cleaned_data["hora"]

            if fecha < timezone.localdate():
                messages.error(request, "No puedes reservar en una fecha pasada.")
            elif Reserva.existe_conflicto(servicio, fecha, hora):
                messages.error(request, "Ese horario ya está ocupado para este servicio. Por favor elige otro.")
            else:
                reserva = form.save(commit=False)
                reserva.servicio = servicio
                reserva.save()
                return redirect("confirmacion", reserva_id=reserva.id)
    else:
        form = ReservaForm()

    return render(request, "reservas/reservar.html", {"servicio": servicio, "form": form})


def confirmacion(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    return render(request, "reservas/confirmacion.html", {"reserva": reserva})


@login_required
def panel_reservas(request):
    reservas = Reserva.objects.all().select_related("servicio")
    return render(request, "reservas/panel.html", {"reservas": reservas})


@login_required
def cambiar_estado(request, reserva_id, nuevo_estado):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    if nuevo_estado in ["pendiente", "confirmada", "cancelada"]:
        reserva.estado = nuevo_estado
        reserva.save()
        messages.success(request, f"Reserva actualizada a: {nuevo_estado}")
    return redirect("panel_reservas")
