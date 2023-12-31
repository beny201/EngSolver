# Generated by Django 4.2.6 on 2023-10-06 17:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='BoltStandard',
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
                ('title', models.TextField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='NutStandard',
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
                ('title', models.TextField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='WasherStandard',
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
                ('title', models.TextField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Washer',
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
                ('name', models.TextField(max_length=50)),
                ('thickness_washer', models.FloatField()),
                ('width_washer', models.FloatField()),
                ('diameter', models.IntegerField()),
                (
                    'standard',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='distance_checker.washerstandard',
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='Nut',
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
                ('name', models.TextField(max_length=50)),
                ('thickness_nut', models.FloatField()),
                ('width_nut', models.FloatField()),
                ('diameter', models.IntegerField()),
                (
                    'standard',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='distance_checker.nutstandard',
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='Bolt',
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
                ('name', models.TextField(max_length=50)),
                ('thickness_bolt_head', models.FloatField()),
                ('width_bolt_head', models.FloatField()),
                ('length', models.IntegerField()),
                ('diameter', models.IntegerField()),
                ('thread_length', models.FloatField()),
                (
                    'standard',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='distance_checker.boltstandard',
                    ),
                ),
            ],
        ),
    ]
