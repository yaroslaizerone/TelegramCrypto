# Generated by Django 4.1.6 on 2023-02-15 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_city_country_region_remove_persondata_zip_code_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='persondata',
            name='city',
        ),
        migrations.AlterField(
            model_name='persondata',
            name='address',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Адрес'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='persondata',
            name='first_name',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='Имя'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='persondata',
            name='last_name',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='Фамилия'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='persondata',
            name='middle_name',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='Отчество'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='persondata',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=20, verbose_name='Номер телефона'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='City',
        ),
    ]
