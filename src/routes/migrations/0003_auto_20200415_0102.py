# Generated by Django 3.0.4 on 2020-04-15 01:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0002_auto_20200415_0047'),
    ]

    operations = [
        migrations.RenameField(
            model_name='route',
            old_name='across_sities',
            new_name='across_cities',
        ),
    ]
