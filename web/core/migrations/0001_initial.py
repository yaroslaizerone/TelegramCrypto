# Generated by Django 4.1.6 on 2023-04-11 06:48

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Страна')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='Фамилия')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='Имя')),
                ('middle_name', models.CharField(blank=True, max_length=30, verbose_name='Отчество')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Электронная почта')),
                ('phone', models.CharField(blank=True, max_length=11, unique=True, verbose_name='Номер телефона')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('address', models.CharField(blank=True, max_length=255, verbose_name='Адрес')),
                ('product_info', models.CharField(blank=True, max_length=255, verbose_name='Информация о товаре')),
                ('city', models.CharField(blank=True, max_length=30, verbose_name='Город')),
                ('comment', models.CharField(blank=True, max_length=255, verbose_name='Комментарий')),
                ('gender', models.CharField(blank=True, choices=[('M', 'Мужской'), ('F', 'Женский'), ('U', 'Неопределен')], max_length=1, verbose_name='Пол')),
                ('random_uuid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='Случайный UUID')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.country', verbose_name='Страна')),
            ],
            options={
                'verbose_name': 'Данные абонента',
                'verbose_name_plural': 'Данные абонента',
            },
        ),
        migrations.CreateModel(
            name='PersonStatusLV',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_id', models.PositiveIntegerField(verbose_name='ID статуса')),
                ('name', models.CharField(max_length=100, verbose_name='Название статуса')),
            ],
        ),
        migrations.CreateModel(
            name='PersonTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название тега')),
            ],
            options={
                'verbose_name': 'Теги',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Регион')),
                ('utc', models.CharField(max_length=6, verbose_name='Часовой пояс UTC')),
            ],
        ),
        migrations.CreateModel(
            name='TaskStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.CharField(max_length=255, unique=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='PersonUsage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_use', models.DateTimeField(verbose_name='Дата использования')),
                ('person', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='core.person', verbose_name='Абонент')),
            ],
        ),
        migrations.CreateModel(
            name='PersonTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='person-table/%Y/%m/', verbose_name='Файл таблицы')),
                ('columns', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1000), size=None, verbose_name='Столбцы таблицы')),
                ('status', models.SmallIntegerField(choices=[(0, 'Новый'), (1, 'Сопоставлено'), (2, 'Обрабатывается'), (3, 'Выполнено')], default=0, verbose_name='Статус')),
                ('num_rows', models.PositiveIntegerField(blank=True, null=True, verbose_name='Количество строк')),
                ('tags', models.ManyToManyField(blank=True, to='core.persontag', verbose_name='Теги')),
            ],
            options={
                'verbose_name': 'Загруженная таблица',
                'verbose_name_plural': 'Загруженные таблицы',
            },
        ),
        migrations.AddField(
            model_name='person',
            name='person_table',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.persontable', verbose_name='Загруженная таблица'),
        ),
        migrations.AddField(
            model_name='person',
            name='person_usage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='related_person', to='core.personusage'),
        ),
        migrations.AddField(
            model_name='person',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.region', verbose_name='Регион'),
        ),
        migrations.AddField(
            model_name='person',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.personstatuslv', verbose_name='Статус'),
        ),
        migrations.AddField(
            model_name='person',
            name='tags',
            field=models.ManyToManyField(blank=True, to='core.persontag', verbose_name='Теги'),
        ),
    ]
