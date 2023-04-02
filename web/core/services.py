import time
import pandas as pd
from core.utils import validate_data, parse_person_data
from core.models import Person, PersonTable, PersonUsage
from core.constants import PersonTableStatus
from django.http import HttpResponse
from core.column_config import ColumnConfig
from datetime import datetime
from django.db.models import Prefetch, Max


class PersonService:

    @staticmethod
    def filtered_queryset(request):
        """ Фильтрует и сортирует объекты Person на основе параметров запроса. """
        qs = Person.objects.all()
        regions = request.GET.getlist('region')
        utcs = request.GET.getlist('utc')
        max_rows = request.GET.get('max_rows')
        if regions:
            qs = qs.filter(region__in=regions)
        if utcs:
            qs = qs.filter(region__utc__in=utcs)

        qs = qs.annotate(last_usage_date=Max('personusage__date_of_use')) \
            .order_by('last_usage_date', '-pk')

        qs = qs.prefetch_related(
            Prefetch('personusage_set', queryset=PersonUsage.objects.order_by('-date_of_use')))

        if max_rows:
            qs = qs[:int(max_rows)]

        return qs

    @staticmethod
    def export_to_excel(queryset, selected_columns):
        """ Экспортирует объекты Person в файл Excel. """
        column_list = ['id'] + selected_columns
        df = pd.DataFrame(queryset.values(*column_list))
        columns = ['id'] + [ColumnConfig.get_header_name(column) for column in selected_columns]
        df.columns = columns

        for index, row in df.iterrows():
            person_id = row['id']
            person = Person.objects.get(pk=person_id)
            PersonUsage.objects.create(person=person)

        response = HttpResponse(content_type='application/ms-excel')
        row_count = len(df)
        current_date = datetime.now().strftime('%Y-%m-%d_%H-%M')
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
        data = validate_data(pd.read_excel(filename, header=None))
        print(f"load {time.time() - start_time}")
        return data

    @staticmethod
    def save_table(loaded_table):
        if loaded_table.status != PersonTableStatus.STATUS_MATCHING:
            return False

        loaded_table.status = PersonTableStatus.STATUS_PROCESSED
        loaded_table.save()

        excel_data = TableService.read_table(loaded_table.file)
        keys = [pair.split(":")[0] for pair in loaded_table.columns]
        column_pairs = loaded_table.columns
        person_data = {}
        for pair in column_pairs:
            attribute_name, value = pair.split(":", maxsplit=1)
            person_data = parse_person_data(person_data, attribute_name, value)
        person = Person(**person_data)
        person.save()  # записываю заголовок
        global COUNTER
        COUNTER += 1
        print(f"Счетчик: {COUNTER} {person}")

        for _, row in excel_data.iterrows():
            person_data = {}
            for i, value in enumerate(row):
                attribute_name = keys[i]
                person_data = parse_person_data(person_data, attribute_name, value)
            person = Person(**person_data)
            if person.phone:
                person.save()
                COUNTER += 1
                print(f"Счетчик: {COUNTER} {person}")
            else:
                print(f"Не удалось сохранить строку {row}, номер телефона некорректный")
        loaded_table.status = PersonTableStatus.STATUS_COMPLETED
        loaded_table.save()

        return True
