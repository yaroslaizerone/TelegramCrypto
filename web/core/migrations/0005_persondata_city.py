# Generated by Django 4.1.6 on 2023-02-15 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_persondata_birth_date_alter_persondata_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='persondata',
            name='city',
            field=models.CharField(blank=True, max_length=50, verbose_name='Город'),
        ),
    ]