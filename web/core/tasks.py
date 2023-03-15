from core.models import PersonTable
from celery import shared_task
from core.services import TableService, LeadVertexService


@shared_task
def save_table_task(loaded_table_id):
    loaded_table = PersonTable.objects.get(id=loaded_table_id)
    TableService.save_table(loaded_table)

@shared_task
def update_person_status_and_usage_by_phone_number():
    LeadVertexService.update_person_and_usage()
