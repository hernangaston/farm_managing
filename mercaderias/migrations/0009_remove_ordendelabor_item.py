# Generated by Django 3.2 on 2022-04-06 21:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mercaderias', '0008_ordendelabor_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordendelabor',
            name='item',
        ),
    ]
