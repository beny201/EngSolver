# Generated by Django 4.2.6 on 2023-11-05 15:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bars_calculation", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="calculationcfrhs",
            name="limit_deformation",
            field=models.FloatField(default=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="profilerhs",
            name="A",
            field=models.FloatField(help_text="Cross-section area [mm^2]"),
        ),
        migrations.AlterField(
            model_name="profilerhs",
            name="G",
            field=models.FloatField(help_text="Nominal weight per [kg/m]"),
        ),
        migrations.AlterField(
            model_name="profilerhs",
            name="Iy",
            field=models.FloatField(help_text="Moment of inertia about the Y [mm^4]"),
        ),
        migrations.AlterField(
            model_name="profilerhs",
            name="Iz",
            field=models.FloatField(help_text="Moment of inertia about the Z [mm^4]"),
        ),
        migrations.AlterField(
            model_name="profilerhs",
            name="Wply",
            field=models.FloatField(help_text="plastic_section Wply [mm^3]"),
        ),
        migrations.AlterField(
            model_name="profilerhs",
            name="Wplz",
            field=models.FloatField(help_text="plastic_section Wplz [mm^3]"),
        ),
    ]