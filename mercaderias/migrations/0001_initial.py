# Generated by Django 3.2 on 2022-01-17 20:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('comprobantes', '0003_empresarepresentada'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CartaDePorte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(blank=True, max_length=255, null=True)),
                ('ctg', models.CharField(blank=True, max_length=255, null=True)),
                ('renspa', models.CharField(blank=True, max_length=255, null=True)),
                ('fecha', models.DateField(blank=True, null=True)),
                ('grano', models.CharField(blank=True, max_length=255, null=True)),
                ('tipo', models.CharField(blank=True, max_length=255, null=True)),
                ('cosecha', models.CharField(blank=True, max_length=255, null=True)),
                ('contrato', models.CharField(blank=True, max_length=255, null=True)),
                ('pesada_en_destino', models.BooleanField(blank=True, null=True)),
                ('kgs_estimados', models.BooleanField(blank=True, null=True)),
                ('declaracion_calidad', models.BooleanField(blank=True, null=True)),
                ('conforme', models.BooleanField(blank=True, null=True)),
                ('condicional', models.BooleanField(blank=True, null=True)),
                ('peso_bruto', models.CharField(blank=True, max_length=255, null=True)),
                ('peso_tara', models.CharField(blank=True, max_length=255, null=True)),
                ('peso_neto', models.CharField(blank=True, max_length=255, null=True)),
                ('observaciones', models.CharField(blank=True, max_length=255, null=True)),
                ('direccion_procedencia', models.CharField(blank=True, max_length=255, null=True)),
                ('localidad_procedencia', models.CharField(blank=True, max_length=255, null=True)),
                ('provincia_procedencia', models.CharField(blank=True, max_length=255, null=True)),
                ('kilometros', models.CharField(blank=True, max_length=255, null=True)),
                ('tarifa', models.CharField(blank=True, max_length=255, null=True)),
                ('tarifa_referencia', models.CharField(blank=True, max_length=255, null=True)),
                ('declaracion_juarada_nombre', models.CharField(blank=True, max_length=255, null=True)),
                ('declaracion_juarada_dni', models.CharField(blank=True, max_length=255, null=True)),
                ('docfile', models.FileField(blank=True, null=True, upload_to='cp_nuevas')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Corredor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('cuit', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Destinatario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('cuit', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Entregador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('cuit', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Intermediario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('cuit', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='IntermediarioFlete',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('cuit', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='MercadoATermino',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('cuit', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='RemitenteComercial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('cuit', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transportista',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('cuit', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Destino',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('cuit', models.CharField(max_length=255)),
                ('codigo_de_planta', models.CharField(max_length=255)),
                ('direccion', models.CharField(max_length=255)),
                ('localidad', models.CharField(max_length=255)),
                ('provincia', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('destinatario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mercaderias.destinatario')),
            ],
        ),
        migrations.CreateModel(
            name='ContratoMercaderia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_contrato', models.DateField()),
                ('nro_comprador', models.CharField(max_length=20)),
                ('nro_vendedor', models.CharField(max_length=20)),
                ('tipo_contrato', models.CharField(choices=[('FIJAR', 'A fijar'), ('FORWARD', 'Forward'), ('DISPONIBLE', 'Disponible')], max_length=100)),
                ('producto', models.CharField(choices=[('SOJA', 'soja'), ('MAIZ', 'ma??z'), ('TRIGO', 'trigo'), ('GIRASOL', 'girasol'), ('SORGO', 'sorgo')], default='SOJA', max_length=20)),
                ('kilos_pactados', models.PositiveBigIntegerField()),
                ('cosecha', models.CharField(choices=[('2020/2021', '2020/2021'), ('2021/2022', '2021/2022'), ('2022/2023', '2022/2023'), ('2023/2024', '2023/2024'), ('2024/2025', '2024/2025')], max_length=60)),
                ('precio', models.PositiveIntegerField()),
                ('fecha_inicio_cumplimiento', models.DateField()),
                ('fecha_fin_cumplimiento', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('comprador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mercaderias.destinatario')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comprobantes.empresarepresentada')),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Chofer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('apellido', models.CharField(max_length=255)),
                ('cuit', models.CharField(max_length=255)),
                ('patente_chasis', models.CharField(max_length=255)),
                ('patente_acoplado', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('transportista', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mercaderias.transportista')),
            ],
        ),
        migrations.CreateModel(
            name='CartaDePorteDescargada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kilos_descargados', models.IntegerField(blank=True, null=True)),
                ('kilos_merma', models.IntegerField(blank=True, default=0)),
                ('observaciones_descarga', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('contrato', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mercaderias.contratomercaderia')),
                ('cp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mercaderias.cartadeporte')),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='cartadeporte',
            name='chofer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mercaderias.chofer'),
        ),
        migrations.AddField(
            model_name='cartadeporte',
            name='corredor_comprador',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='corredorC', to='mercaderias.corredor'),
        ),
        migrations.AddField(
            model_name='cartadeporte',
            name='corredor_vendedor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='corredorV', to='mercaderias.corredor'),
        ),
        migrations.AddField(
            model_name='cartadeporte',
            name='destinatario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mercaderias.destinatario'),
        ),
        migrations.AddField(
            model_name='cartadeporte',
            name='destino',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mercaderias.destino'),
        ),
        migrations.AddField(
            model_name='cartadeporte',
            name='entregador',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mercaderias.entregador'),
        ),
        migrations.AddField(
            model_name='cartadeporte',
            name='intermediario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mercaderias.intermediario'),
        ),
        migrations.AddField(
            model_name='cartadeporte',
            name='intermediario_flete',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mercaderias.intermediarioflete'),
        ),
        migrations.AddField(
            model_name='cartadeporte',
            name='mercado_a_termino',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mercaderias.mercadoatermino'),
        ),
        migrations.AddField(
            model_name='cartadeporte',
            name='remitente_comercial',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mercaderias.remitentecomercial'),
        ),
        migrations.AddField(
            model_name='cartadeporte',
            name='titular',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comprobantes.empresarepresentada'),
        ),
        migrations.AddField(
            model_name='cartadeporte',
            name='transportista',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mercaderias.transportista'),
        ),
        migrations.AddField(
            model_name='cartadeporte',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
