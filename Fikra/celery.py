# celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# تعيين إعدادات Django لمشروع Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Fikra.settings')

app = Celery('Fikra')

# قراءة إعدادات Celery من إعدادات Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# اكتشاف المهام (tasks) تلقائيًا من جميع التطبيقات المسجلة
app.autodiscover_tasks()

# إضافة هذا الإعداد ضمن إعدادات Celery
app.conf.broker_connection_retry_on_startup = True