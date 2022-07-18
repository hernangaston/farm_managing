# Generated by Django 3.2 on 2022-06-06 18:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comprobantes', '0016_alter_factura_cosecha'),
        ('mercaderias', '0019_campo_empresa'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hectareas', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('campo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mercaderias.campo')),
                ('propietario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comprobantes.proveedor')),
            ],
            options={
                'verbose_name': 'Lote',
                'verbose_name_plural': 'Lotes',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Arrendamiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateField(blank=True, null=True)),
                ('fecha_fin', models.DateField(blank=True, null=True)),
                ('toneladas_x_ha', models.IntegerField(blank=True, null=True)),
                ('descripcion', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('arrendador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comprobantes.proveedor')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comprobantes.empresarepresentada')),
                ('lote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mercaderias.lote')),
            ],
            options={
                'verbose_name': 'Contrato de Arrendamiento',
                'verbose_name_plural': 'Arrendamientos',
                'managed': True,
            },
        ),
    ]