# Generated by Django 4.2.6 on 2023-11-15 18:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bars_calculation", "0009_detailedcalculationcfrhs_bending_capacity_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="detailedcalculationcfrhs",
            name="buckling_curve",
            field=models.CharField(),
        ),
    ]