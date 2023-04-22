# Generated by Django 4.1.7 on 2023-04-22 14:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Caja",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="Nombre")),
                (
                    "balance",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        default=0,
                        max_digits=8,
                        verbose_name="Total",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Usuario",
                    ),
                ),
            ],
            options={
                "verbose_name": "caja",
                "verbose_name_plural": "cajas",
            },
        ),
        migrations.CreateModel(
            name="Movement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(verbose_name="Fecha")),
                ("desc", models.CharField(max_length=25, verbose_name="Concepto")),
                (
                    "qty",
                    models.DecimalField(
                        decimal_places=2, max_digits=7, verbose_name="Monto"
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("IN", "Ingreso"), ("OUT", "Egreso")],
                        max_length=3,
                        verbose_name="Tipo de movimiento",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("ACTIVE", "ACTIVO"), ("CANCELED", "CANCELADO")],
                        default="ACTIVE",
                        editable=False,
                        max_length=10,
                        verbose_name="Estatus",
                    ),
                ),
                (
                    "created_at",
                    models.DateField(auto_now_add=True, verbose_name="Creado en"),
                ),
                (
                    "modified_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Ultima modificacion"
                    ),
                ),
                (
                    "caja",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="caja.caja",
                        verbose_name="Caja",
                    ),
                ),
            ],
            options={
                "verbose_name": "movimiento",
                "verbose_name_plural": "movimientos",
                "ordering": ("-date",),
            },
        ),
    ]
