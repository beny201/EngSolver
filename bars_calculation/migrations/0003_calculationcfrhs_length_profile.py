# Generated by Django 4.2.6 on 2023-11-05 16:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bars_calculation", "0002_calculationcfrhs_limit_deformation_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="calculationcfrhs",
            name="length_profile",
            field=models.FloatField(default=100),
            preserve_default=False,
        ),
    ]
