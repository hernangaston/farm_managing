# Generated by Django 3.2 on 2022-05-16 18:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comprobantes', '0011_auto_20220516_1520'),
        ('mercaderias', '0017_alter_cartadeporte_establecimiento'),
    ]

    operations = [
        migrations.AddField(
            model_name='plansiembra',
            name='titular',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comprobantes.empresarepresentada'),
        ),
    ]
