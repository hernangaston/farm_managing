# Generated by Django 3.2 on 2022-05-16 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mercaderias', '0016_auto_20220422_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartadeporte',
            name='establecimiento',
            field=models.CharField(default='', max_length=255),
        ),
    ]