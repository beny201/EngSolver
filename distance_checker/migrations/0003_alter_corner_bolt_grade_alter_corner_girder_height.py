# Generated by Django 4.2.6 on 2023-10-19 19:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('distance_checker', '0002_corner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='corner',
            name='bolt_grade',
            field=models.TextField(
                choices=[('8_8', '8.8'), ('10_9', '10.9')], default='8_8'
            ),
        ),
        migrations.AlterField(
            model_name='corner',
            name='girder_height',
            field=models.IntegerField(default=400),
        ),
    ]
