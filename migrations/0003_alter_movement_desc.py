# Generated by Django 4.1.7 on 2023-05-05 01:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("caja", "0002_alter_caja_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="movement",
            name="desc",
            field=models.CharField(max_length=80, verbose_name="Concepto"),
        ),
    ]