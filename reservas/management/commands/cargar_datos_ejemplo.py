from django.core.management.base import BaseCommand
from reservas.models import Servicio


class Command(BaseCommand):
    help = "Carga servicios de ejemplo para probar el sistema"

    def handle(self, *args, **options):
        servicios = [
            {"nombre": "Corte clásico", "descripcion": "Corte de cabello tradicional con máquina y tijera", "duracion_minutos": 30, "precio": 15000},
            {"nombre": "Corte + barba", "descripcion": "Corte de cabello y arreglo de barba completo", "duracion_minutos": 50, "precio": 25000},
            {"nombre": "Afeitado clásico", "descripcion": "Afeitado tradicional con toalla caliente y navaja", "duracion_minutos": 25, "precio": 18000},
        ]
        for s in servicios:
            obj, creado = Servicio.objects.get_or_create(nombre=s["nombre"], defaults=s)
            if creado:
                self.stdout.write(self.style.SUCCESS(f"Creado: {obj.nombre}"))
            else:
                self.stdout.write(f"Ya existía: {obj.nombre}")
