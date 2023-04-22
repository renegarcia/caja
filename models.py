from django.db import models
from django.utils.translation import gettext_lazy as _
from django.shortcuts import reverse


class Caja(models.Model):
    name = models.CharField(_("Nombre"), max_length=50)
    balance = models.DecimalField(
        _("Total"), max_digits=8, decimal_places=2, null=False, blank=True, default=0
    )
    user = models.ForeignKey(
        "auth.User", verbose_name=_("Usuario"), on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _("caja")
        verbose_name_plural = _("cajas")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("caja:caja_detail", kwargs={"pk": self.pk})


class Movement(models.Model):
    IN = "IN"
    OUT = "OUT"
    TYPE = (
        (IN, _("Ingreso")),
        (OUT, _("Egreso")),
    )
    ACTIVE = "ACTIVE"
    CANCELED = "CANCELED"
    STATUS = (
        (ACTIVE, _("ACTIVO")),
        (CANCELED, _("CANCELADO")),
    )
    caja = models.ForeignKey("Caja", verbose_name=_("Caja"), on_delete=models.CASCADE)
    date = models.DateField(_("Fecha"), auto_now=False, auto_now_add=False)
    desc = models.CharField(_("Concepto"), max_length=25)
    # comment = models.TextField(_("Comentario"), null=True, blank=True)
    qty = models.DecimalField(_("Monto"), max_digits=7, decimal_places=2)
    type = models.CharField(_("Tipo de movimiento"), max_length=3, choices=TYPE)
    status = models.CharField(
        _("Estatus"),
        max_length=10,
        default=ACTIVE,
        choices=STATUS,
        editable=False,
    )
    created_at = models.DateField(_("Creado en"), auto_now=False, auto_now_add=True)
    modified_at = models.DateTimeField(
        _("Ultima modificacion"), auto_now=True, auto_now_add=False
    )

    class Meta:
        verbose_name = _("movimiento")
        verbose_name_plural = _("movimientos")
        ordering = ("-date",)

    def __str__(self):
        return self.desc

    def cancel(self):
        self.status = Movement.CANCELED
        self.save()

    def is_canceled(self):
        return self.status == Movement.CANCELED

    def get_cancel_url(self):
        return reverse("caja:movement_cancel", kwargs={"pk": self.pk})
