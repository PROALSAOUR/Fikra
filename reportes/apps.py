from django.apps import AppConfig


class ReportesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reportes'
    
    def ready(self):
        import reportes.signals  # تأكد من تحميل الإشارات عند بدء التشغيل

