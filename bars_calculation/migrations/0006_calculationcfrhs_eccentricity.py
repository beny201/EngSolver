# Generated by Django 4.2.6 on 2023-11-05 18:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bars_calculation", "0005_calculationcfrhs_steel"),
    ]

    operations = [
        migrations.AddField(
            model_name="calculationcfrhs",
            name="eccentricity",
            field=models.FloatField(default=100),
            preserve_default=False,
        ),
    ]
