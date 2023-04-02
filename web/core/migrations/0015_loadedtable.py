# Generated by Django 4.1.6 on 2023-02-19 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_delete_loadedtable'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoadedTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/%Y/%m/', verbose_name='Файл таблицы')),
                ('columns', models.TextField(verbose_name='Столбцы таблицы')),
                ('status', models.CharField(choices=[('U', 'Unprocessed'), ('M', 'Mapping'), ('P', 'Processed')], default='U', max_length=1, verbose_name='Статус')),
                ('field_mappings', models.JSONField(blank=True, null=True, verbose_name='Сопоставление полей')),
            ],
            options={
                'verbose_name': 'Загруженная таблица',
                'verbose_name_plural': 'Загруженные таблицы',
            },
        ),
    ]