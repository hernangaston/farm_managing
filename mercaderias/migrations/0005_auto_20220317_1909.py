# Generated by Django 3.2 on 2022-03-17 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mercaderias', '0004_alter_campo_hectareas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartadeporte',
            name='cosecha',
            field=models.CharField(choices=[('2015/2016', '2015/2016'), ('2016/2017', '2016/2017'), ('2017/2018', '2017/2018'), ('2018/2019', '2018/2019'), ('2019/2020', '2019/2020'), ('2020/2021', '2020/2021'), ('2021/2022', '2021/2022'), ('2022/2023', '2022/2023'), ('2023/2024', '2023/2024'), ('2024/2025', '2024/2025')], default='2021/2022', max_length=255),
        ),
        migrations.AlterField(
            model_name='contratomercaderia',
            name='cosecha',
            field=models.CharField(choices=[('2015/2016', '2015/2016'), ('2016/2017', '2016/2017'), ('2017/2018', '2017/2018'), ('2018/2019', '2018/2019'), ('2019/2020', '2019/2020'), ('2020/2021', '2020/2021'), ('2021/2022', '2021/2022'), ('2022/2023', '2022/2023'), ('2023/2024', '2023/2024'), ('2024/2025', '2024/2025')], max_length=60),
        ),
        migrations.AlterField(
            model_name='plansiembra',
            name='campania',
            field=models.CharField(choices=[('2015/2016', '2015/2016'), ('2016/2017', '2016/2017'), ('2017/2018', '2017/2018'), ('2018/2019', '2018/2019'), ('2019/2020', '2019/2020'), ('2020/2021', '2020/2021'), ('2021/2022', '2021/2022'), ('2022/2023', '2022/2023'), ('2023/2024', '2023/2024'), ('2024/2025', '2024/2025')], max_length=60),
        ),
    ]
