from django.db import models

class UserReports(models.Model):
    class Meta:
        verbose_name_plural = 'عدد المستخدمين'
        
class OrdersCount(models.Model):
    class Meta:
        verbose_name_plural = 'عدد الطلبات'