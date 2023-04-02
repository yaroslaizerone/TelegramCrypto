# Generated by Django 4.1.6 on 2023-03-10 07:59

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_person_person_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persontable',
            name='columns',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1000), size=None, verbose_name='Столбцы таблицы'),
        ),
        migrations.AlterField(
            model_name='persontable',
            name='file',
            field=models.FileField(upload_to='person-table/%Y/%m/', verbose_name='Файл таблицы'),
        ),
        migrations.AlterField(
            model_name='persontable',
            name='status',
            field=models.SmallIntegerField(choices=[(0, 'Новый'), (1, 'Сопоставлено'), (2, 'Обрабатывается'), (3, 'Выполнено')], default=0, verbose_name='Статус'),
        ),
    ]