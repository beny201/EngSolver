# Generated by Django 4.2.6 on 2023-10-28 10:19

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('distance_checker', '0010_ridge'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ridge',
            old_name='distance_bottom',
            new_name='distance_left',
        ),
        migrations.RenameField(
            model_name='ridge',
            old_name='distance_top',
            new_name='distance_right',
        ),
    ]