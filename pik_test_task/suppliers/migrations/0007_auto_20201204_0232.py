# Generated by Django 3.1.4 on 2020-12-03 23:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('suppliers', '0006_auto_20201204_0111'),
    ]

    operations = [
        migrations.RenameField(
            model_name='servicearea',
            old_name='services',
            new_name='types',
        ),
    ]