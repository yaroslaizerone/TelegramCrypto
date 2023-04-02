import time
import pandas as pd
from core.utils import validate_data, parse_person_data
from core.models import Person, PersonTable
from core.constants import PersonTableStatus
import asyncio


COUNTER =0
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
