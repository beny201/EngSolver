# Generated by Django 4.2.6 on 2023-10-19 17:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('distance_checker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Corner',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('name', models.TextField(default='Corner', max_length=50)),
                ('girder_angle', models.FloatField(default=14.5)),
                ('girder_height', models.IntegerField(default=14.5)),
                ('t_flange_girder', models.IntegerField(default=20)),
                ('column_width', models.IntegerField(default=900)),
                ('t_flange_column', models.IntegerField(default=20)),
                ('t_plate_connection', models.IntegerField(default=20)),
                (
                    'bolt_grade',
                    models.IntegerField(
                        choices=[('8_8', '8.8'), ('10_9', '10.9')], default='8_8'
                    ),
                ),
                ('bolt_diameter', models.IntegerField(default=30)),
                ('last_modified_date', models.DateField(auto_now=True)),
                ('created_date', models.DateField(auto_now_add=True)),
                (
                    'author',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
