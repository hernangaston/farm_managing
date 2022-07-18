# Generated by Django 3.2 on 2022-05-16 18:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comprobantes', '0011_auto_20220516_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresarepresentada',
            name='usuario',
            field=models.ManyToManyField(related_name='empresa_repr', to=settings.AUTH_USER_MODEL),
        ),
    ]
