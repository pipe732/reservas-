from django.urls import path
from . import views

urlpatterns = [
    path("", views.catalogo, name="catalogo"),
    path("reservar/<int:servicio_id>/", views.reservar, name="reservar"),
    path("confirmacion/<int:reserva_id>/", views.confirmacion, name="confirmacion"),
    path("panel/", views.panel_reservas, name="panel_reservas"),
    path("panel/reserva/<int:reserva_id>/<str:nuevo_estado>/", views.cambiar_estado, name="cambiar_estado"),
]
