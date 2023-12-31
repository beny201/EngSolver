# Generated by Django 4.2.6 on 2023-11-15 18:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bars_calculation", "0008_detailedcalculationcfrhs_calculationcfrhs_detailed"),
    ]

    operations = [
        migrations.AddField(
            model_name="detailedcalculationcfrhs",
            name="bending_capacity",
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="calculationcfrhs",
            name="detailed",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="bars_calculation.detailedcalculationcfrhs",
            ),
        ),
    ]
