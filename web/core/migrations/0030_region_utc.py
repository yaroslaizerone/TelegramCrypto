# Generated by Django 4.1.6 on 2023-03-12 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_persontable_num_rows_alter_person_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='utc',
            field=models.CharField(default=' ', max_length=6, verbose_name='Часовой пояс UTC'),
            preserve_default=False,
        ),
    ]