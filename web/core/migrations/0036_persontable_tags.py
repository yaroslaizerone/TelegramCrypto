# Generated by Django 4.1.6 on 2023-04-04 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_person_person_usage'),
    ]

    operations = [
        migrations.AddField(
            model_name='persontable',
            name='tags',
            field=models.ManyToManyField(blank=True, to='core.persontag', verbose_name='Теги'),
        ),
    ]
