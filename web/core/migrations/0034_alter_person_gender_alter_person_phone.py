# Generated by Django 4.1.6 on 2023-04-03 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_taskstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Мужской'), ('F', 'Женский'), ('U', 'Неопределен')], max_length=1, verbose_name='Пол'),
        ),
        migrations.AlterField(
            model_name='person',
            name='phone',
            field=models.CharField(blank=True, max_length=11, unique=True, verbose_name='Номер телефона'),
        ),
    ]