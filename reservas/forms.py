from django import forms
from .models import Reserva


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ["nombre_cliente", "email_cliente", "telefono_cliente", "fecha", "hora", "notas"]
        widgets = {
            "nombre_cliente": forms.TextInput(attrs={"class": "form-control", "placeholder": "Tu nombre completo"}),
            "email_cliente": forms.EmailInput(attrs={"class": "form-control", "placeholder": "tu@email.com"}),
            "telefono_cliente": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej: 3001234567"}),
            "fecha": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "hora": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "notas": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Alguna preferencia o comentario (opcional)"}),
        }
