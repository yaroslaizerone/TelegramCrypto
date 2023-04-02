from django.core.management.base import BaseCommand
from core.models import PersonStatusLV

class Command(BaseCommand):
    help = 'Получить и сохранить статусы из API LeadVertex'

    def handle(self, *args, **options):
        PersonStatusLV.fetch_statuses(PersonStatusLV)
        self.stdout.write(self.style.SUCCESS('Статусы успешно получены из API'))