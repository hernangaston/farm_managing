# Generated by Django 3.2 on 2022-05-17 10:35

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comprobantes', '0013_auto_20220516_1614'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='empresarepresentada',
            name='usuario',
        ),
        migrations.AddField(
            model_name='empresarepresentada',
            name='usuario',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
