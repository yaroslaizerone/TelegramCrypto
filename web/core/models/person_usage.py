from django.db import models


class PersonUsage(models.Model):
    person = models.ForeignKey('core.Person', on_delete=models.CASCADE, blank=True, verbose_name='Абонент')
    date_of_use = models.DateTimeField('Дата использования')

    def __str__(self):
        if self.person:
            return f'Использование данных абонента {self.person.last_name} {self.person.first_name} {self.date_of_use}'
        else:
            return f'Использование данных абонента (нет данных)'