import time
import requests
import json
import pandas as pd
from core.utils import validate_data, parse_person_data, update_person
from core.models import Person, PersonTable, PersonUsage, PersonStatusLV
from core.constants import PersonTableStatus
from django.http import HttpResponse
from core.column_config import ColumnConfig
from django.db.models import Prefetch, Max
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
from django.db import transaction
from django.utils.timezone import now
from django.db.models import Value
from django.db.models.functions import Concat
from django.db.models.functions import Coalesce


class LeadVertexService:
    API_KEY = settings.LEAD_VERTEX_API_KEY
    ORDER_IDS_URL = 'https://statk.leadvertex.ru/api/admin/getOrdersIdsByCondition.html?token={}&phone={}'
    ORDER_DETAILS_URL = 'https://statk.leadvertex.ru/api/admin/getOrdersByIds.html?token={}&ids={}'

    @staticmethod
    def get_orders(phone_number):
        """Получает список заказов по номеру телефона."""
        url = LeadVertexService.ORDER_IDS_URL.format(LeadVertexService.API_KEY, phone_number)
        response = requests.get(url)
        order_ids = response.json()
        return order_ids

    @staticmethod
    def get_details(order_ids):
        """Получает детали заказа по первому (последнему) ID."""
        try:
            first_order_id = order_ids[0]
        except IndexError:
            print("Ошибка: список order_ids пуст")
            return None

        url = LeadVertexService.ORDER_DETAILS_URL.format(LeadVertexService.API_KEY, first_order_id)
        response = requests.get(url)

        if response.status_code == 200:
            order_data = json.loads(response.text)
            return order_data
        else:
            return None

    @staticmethod
    def get_orders_and_details(phone_number):
        """Получает заказы и детали заказа по номеру телефона."""
        order_ids = LeadVertexService.get_orders(phone_number)
        order_data = LeadVertexService.get_details(order_ids)

        if not order_data:
            person_status, _ = PersonStatusLV.objects.get_or_create(
                status_id=111,
                defaults={'name': 'Не использовано'}
            )
            last_update = datetime(2000, 1, 1)
            return (person_status, last_update)

        most_recent_order = max(order_data.items(), key=lambda x: x[1]['lastUpdate'])
        status_id = most_recent_order[1]['status']
        last_update = most_recent_order[1]['lastUpdate']

        try:
            person_status = PersonStatusLV.objects.get(status_id=status_id)
        except PersonStatusLV.DoesNotExist:
            return None

        return (person_status, last_update)

    @staticmethod
    def update_person_and_usage():
        """Обновляет статус и дату использования для одной записи."""
        while True:
            with transaction.atomic():
                person = Person.objects.filter(status_id=None).select_for_update(skip_locked=True).first()

                if not person:
                    break

                order_data = LeadVertexService.get_orders_and_details(person.phone)

                person_status, last_update = order_data
                if person_status is None:
                    person_status = PersonStatusLV(status_id=111, name='Не использовано')

                person.status = person_status
                person.save()

                if last_update is not None:
                    if isinstance(last_update, str):
                        last_update_datetime = datetime.strptime(last_update, "%Y-%m-%d %H:%M:%S")
                        last_update_aware = timezone.make_aware(last_update_datetime)
                    else:
                        last_update_aware = timezone.make_aware(last_update)

                    PersonUsage.objects.create(person=person, date_of_use=last_update_aware)
                    print(f"{person}, {last_update_aware} updated")


class PersonService:

    def filtered_queryset(request):
        """ Фильтрует и сортирует объекты Person на основе параметров запроса. """
        qs = Person.objects.all()
        regions = request.GET.getlist('region')
        utcs = request.GET.getlist('utc')
        max_rows = request.GET.get('max_rows')
        gender = request.GET.getlist('gender')
        tag = request.GET.getlist('tag')
        status = request.GET.getlist('status')

        if gender:
            qs = qs.filter(gender__in=gender)

        if tag:
            qs = qs.filter(tags__pk__in=tag)

        if regions:
            qs = qs.filter(region__in=regions)

        if utcs:
            qs = qs.filter(region__utc__in=utcs)

        if status:
            qs = qs.filter(status__in=status)

        min_date = datetime.min + timedelta(days=1)  # Значение по умолчанию для пустых значений даты использования
        qs = qs.annotate(
            last_usage_date=Coalesce(Max('personusage__date_of_use'), min_date)
        ).order_by('last_usage_date', 'random_uuid')

        qs = qs.prefetch_related(
            Prefetch('personusage_set', queryset=PersonUsage.objects.order_by('-date_of_use')))

        if max_rows:
            qs = qs[:int(max_rows)]

        return qs

    @staticmethod
    def export_to_excel(queryset, selected_columns, merge_fio=False):
        """ Экспортирует объекты Person в файл Excel. """

        if merge_fio:
            selected_columns.remove('last_name')
            selected_columns.remove('first_name')
            selected_columns.remove('middle_name')
            selected_columns.append('fio')

        column_list = ['id'] + selected_columns

        if merge_fio:
            queryset = queryset.annotate(fio=Concat('last_name', Value(' '), 'first_name', Value(' '), 'middle_name'))

        df = pd.DataFrame(queryset.values(*column_list))

        fio_mapping = ('fio', 'ФИО')
        columns = ['id'] + [ColumnConfig.get_header_name(column) if column != 'fio' else fio_mapping[1] for column in
                            selected_columns]
        df.columns = columns

        if merge_fio:
            # Поместить колонку ФИО на первое место
            fio_column = df.pop('ФИО')
            df.insert(1, 'ФИО', fio_column)

        for index, row in df.iterrows():
            person_id = row['id']
            person = Person.objects.get(pk=person_id)
            PersonUsage.objects.create(person=person, date_of_use=now())

        response = HttpResponse(content_type='application/ms-excel')
        row_count = len(df)
        current_date = now().strftime('%Y-%m-%d_%H-%M')
        filename = f"person_list_{row_count}_rows_{current_date}.xlsx"

        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        df.drop(columns=['id'], inplace=True)
        df.to_excel(response, index=False)
        return response

    @staticmethod
    def has_data_for_columns(qs):
        """ Определяет, есть ли данные для каждого столбца среди объектов Person в QuerySet. """
        columns = [ColumnConfig.get_column_name(key) for key in ColumnConfig.MAPPING.keys()]
        qs_values = qs.values(*columns)
        return {key: any(item[key] for item in qs_values) for key in columns}


COUNTER = 0


class TableService:
    @staticmethod
    def upload_table(filename):
        excel_data = TableService.read_table(filename)
        columns = excel_data.columns.tolist()
        num_rows = len(excel_data) + 1
        loaded_table = PersonTable.objects.create(file=filename, columns=columns, num_rows=num_rows)
        return loaded_table

    @staticmethod
    def read_table(filename):
        start_time = time.time()
        data = pd.read_excel(filename, header=None, dtype=str)
        data = validate_data(data)
        print(f"load {time.time() - start_time}")
        return data

    @staticmethod
    def save_table(loaded_table):
        if loaded_table.status != PersonTableStatus.STATUS_MATCHING:
            return False

        loaded_table.status = PersonTableStatus.STATUS_PROCESSED
        loaded_table.save()
        global COUNTER
        excel_data = TableService.read_table(loaded_table.file)
        keys = [pair.split(":")[0] for pair in loaded_table.columns]
        column_pairs = loaded_table.columns
        person_data = {}
        for pair in column_pairs:
            attribute_name, value = pair.split(":", maxsplit=1)
            person_data = parse_person_data(person_data, attribute_name, value)

        person, created = Person.objects.get_or_create(phone=person_data['phone'])
        if created:
            for key, value in person_data.items():
                setattr(person, key, value)
            print(f"Создан объект: {person}")
        else:
            print(f"Обновлен объект: {person}")
            update_person(person, person_data)

        person.save()
        person.tags.set(loaded_table.tags.all())
        COUNTER += 1
        print(f"Счетчик: {COUNTER}")

        for _, row in excel_data.iterrows():
            person_data = {}
            for i, value in enumerate(row):
                attribute_name = keys[i]
                person_data = parse_person_data(person_data, attribute_name, value)

            if person_data['phone']:
                person, created = Person.objects.get_or_create(phone=person_data['phone'])
                if created:
                    for key, value in person_data.items():
                        setattr(person, key, value)
                    print(f"Создан объект: {person}")
                else:
                    print(f"Обновлен объект: {person}")
                    update_person(person, person_data)

                person.save()
                person.tags.set(loaded_table.tags.all())
                COUNTER += 1
                print(f"Счетчик: {COUNTER}")
            else:
                print(f"Не удалось сохранить строку {person}, номер телефона некорректный")
