from django.db import models

class Settings(models.Model):
    max_return_days = models.IntegerField(verbose_name='اقصى مدة استرجاع')
    max_replace_days = models.IntegerField(verbose_name='اقصى مدة استبدال')
    partners_percentage = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='نسبة الشركاء')
    
    def __str__(self):
        return "الإعدادات"
    
    class Meta:
        verbose_name = "الإعدادات"
        verbose_name_plural = "الإعدادات"