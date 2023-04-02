# Generated by Django 4.1.6 on 2023-02-15 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_persondata_birth_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='persondata',
            name='comment',
            field=models.CharField(blank=True, max_length=255, verbose_name='Комментарий'),
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
