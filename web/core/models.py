from django.db import models
from django.contrib.postgres.fields import ArrayField
from core.constants import PersonTableStatus, GENDER_CHOICES
import requests
from django.conf import settings

class PersonTag(models.Model):
    name = models.CharField(verbose_name='Название тега', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Теги'
        verbose_name_plural = 'Теги'


class Region(models.Model):
    name = models.CharField(verbose_name='Регион', max_length=100)
    utc = models.CharField(verbose_name='Часовой пояс UTC', max_length=6)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(verbose_name='Страна', max_length=30)

    def __str__(self):
        return self.name


class PersonTable(models.Model):
    file = models.FileField(upload_to='person-table/%Y/%m/', verbose_name='Файл таблицы')
    columns = ArrayField(models.CharField(max_length=1000), verbose_name='Столбцы таблицы')
    status = models.SmallIntegerField(choices=PersonTableStatus.STATUS_CHOICES, default=PersonTableStatus.STATUS_NEW, verbose_name='Статус')
    num_rows = models.PositiveIntegerField(null=True, blank=True, verbose_name='Количество строк')

    class Meta:
        verbose_name = 'Загруженная таблица'
        verbose_name_plural = 'Загруженные таблицы'

class PersonStatusLV(models.Model):
    status_id = models.PositiveIntegerField(verbose_name='ID статуса')
    name = models.CharField(verbose_name='Название статуса', max_length=100)

    def fetch_statuses(cls):
        url = f'https://statk.leadvertex.ru/api/admin/getStatusList.html?token={settings.LEAD_VERTEX_API_KEY}'
        response = requests.get(url)
        status_data = response.json()
        cls.objects.update_or_create(
            status_id=111,
            defaults={'name': 'Не использовано'}
        )
        for status_id, status_info in status_data.items():
            cls.objects.update_or_create(
                status_id=status_id,
                defaults={'name': status_info['name']}
            )

class Person(models.Model):
    last_name = models.CharField(verbose_name='Фамилия', max_length=30, blank=True)
    first_name = models.CharField(verbose_name='Имя', max_length=30, blank=True)
    middle_name = models.CharField(verbose_name='Отчество', max_length=30, blank=True)
    email = models.EmailField(verbose_name='Электронная почта', blank=True)
    phone = models.CharField(verbose_name='Номер телефона', max_length=11, blank=True, unique=True)
    birth_date = models.DateField(verbose_name='Дата рождения', blank=True, null=True)
    address = models.CharField(verbose_name='Адрес', max_length=255, blank=True)
    city = models.CharField(verbose_name='Город', max_length=30, blank=True)
    region = models.ForeignKey(Region, verbose_name='Регион', on_delete=models.SET_NULL, blank=True, null=True)
    country = models.ForeignKey(Country, verbose_name='Страна', on_delete=models.SET_NULL, blank=True, null=True)
    tags = models.ManyToManyField(PersonTag, verbose_name='Теги', blank=True)
    comment = models.CharField(verbose_name='Комментарий', max_length=255, blank=True)
    person_table = models.ForeignKey(PersonTable, verbose_name='Загруженная таблица', on_delete=models.SET_NULL, blank=True, null=True)
    status = models.ForeignKey(PersonStatusLV, verbose_name='Статус', on_delete=models.SET_NULL, blank=True, null=True)
    gender = models.CharField(verbose_name='Пол', max_length=1, choices=GENDER_CHOICES, blank=True)

    def save(self, *args, **kwargs):
        self.last_name = self.last_name[:30]
        self.first_name = self.first_name[:30]
        self.middle_name = self.middle_name[:30]
        self.email = self.email[:50]
        self.address = self.address[:255]
        self.city = self.city[:30]
        self.comment = self.comment[:255]

        try:
            super().save(*args, **kwargs)
        except Exception as e:
            print(f"Ошибка при сохранении объекта: {e}")

    class Meta:
        verbose_name = 'Данные абонента'
        verbose_name_plural = 'Данные абонента'

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'


class PersonUsage(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, blank=True, verbose_name='Абонент')
    date_of_use = models.DateTimeField('Дата использования')

    def __str__(self):
        if self.person:
            return f'Использование данных абонента {self.person.last_name} {self.person.first_name} {self.date_of_use}'
        else:
            return f'Использование данных абонента (нет данных)'

class TaskStatus(models.Model):
    task_id = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)