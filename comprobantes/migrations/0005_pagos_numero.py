# Generated by Django 3.2 on 2022-03-21 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comprobantes', '0004_factura_cosecha'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagos',
            name='numero',
            field=models.CharField(default='0', max_length=255),
        ),
    ]
