# Generated by Django 4.1.6 on 2023-03-12 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_alter_person_city_alter_person_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='persontable',
            name='num_rows',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Количество строк'),
        ),
        migrations.AlterField(
            model_name='person',
            name='phone',
            field=models.CharField(blank=True, max_length=11, verbose_name='Номер телефона'),
        ),
    ]