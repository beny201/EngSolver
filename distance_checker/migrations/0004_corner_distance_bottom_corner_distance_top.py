# Generated by Django 4.2.6 on 2023-10-22 05:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('distance_checker', '0003_alter_corner_bolt_grade_alter_corner_girder_height'),
    ]

    operations = [
        migrations.AddField(
            model_name='corner',
            name='distance_bottom',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='corner',
            name='distance_top',
            field=models.IntegerField(default=0),
        ),
    ]