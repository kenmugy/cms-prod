# Generated by Django 3.1.2 on 2020-11-23 08:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20201122_2011'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OrderHistory',
        ),
    ]
