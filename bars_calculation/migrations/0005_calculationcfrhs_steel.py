# Generated by Django 4.2.6 on 2023-11-05 18:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bars_calculation", "0004_calculationcfrhs_country"),
    ]

    operations = [
        migrations.AddField(
            model_name="calculationcfrhs",
            name="steel",
            field=models.CharField(
                choices=[("S235", "S235"), ("S275", "S275"), ("S355", "S355")],
                default=100,
            ),
            preserve_default=False,
        ),
    ]
