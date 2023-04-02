from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Установка переменной окружения для настройки Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('core')

# Использование конфигурации Django settings.py для настройки Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Настройки Celery
app.conf.update(
    broker_url='amqp://guest:guest@localhost:5672//',
    result_backend='redis://localhost:6379/0',
    task_result_expires=3600,
    accept_content=['application/json'],
    task_serializer='json',
    result_serializer='json',
)

# Настройки Flower
app.conf.update(
    celery_flower_user="admin",
    celery_flower_password="password",
    celery_flower_port=5555,
)

# Автоматическое обнаружение и регистрация задач в файлах tasks.py
app.autodiscover_tasks()