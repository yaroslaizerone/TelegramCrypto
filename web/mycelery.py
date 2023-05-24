from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration

sentry_sdk.init(
    dsn='https://80d6ba7899ef4a2ba125fab0c67ddc9a@o4505035629395968.ingest.sentry.io/4505035714920448',
    integrations=[
        CeleryIntegration(),
    ],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,
)

# Установка переменной окружения для настройки Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('core')

# Использование конфигурации Django settings.py для настройки Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Настройки Celery
app.conf.update(
    broker_url='redis://localhost:6379/0',
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
