# Generated by Django 3.2 on 2022-04-20 19:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mercaderias', '0014_auto_20220419_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartadeportedescargada',
            name='contrato',
            field=models.ForeignKey(blank=True, default='DEPOSITO', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='mercaderias.contratomercaderia'),
        ),
    ]
