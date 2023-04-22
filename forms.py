from .models import Movement
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django import forms


class MovementForm(ModelForm):
    class Meta:
        model = Movement
        exclude = ("status",)
        widgets = {
            "date": forms.DateInput(
                format=("%Y-%m-%d"),
                attrs={
                    "class": "form-control",
                    "placeholder": _("Elegir fecha"),
                    "type": "date",
                },
            ),
            "caja": forms.HiddenInput(),
        }
