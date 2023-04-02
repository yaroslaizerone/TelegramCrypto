from core.models import PersonTable
from celery import shared_task
from core.services import TableService

@shared_task
def save_table_task(loaded_table_id):
    loaded_table = PersonTable.objects.get(id=loaded_table_id)
    TableService.save_table(loaded_table)