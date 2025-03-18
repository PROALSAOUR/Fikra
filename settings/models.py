from django.db import models

class Settings(models.Model):
    replace_possibility = models.BooleanField(default=True, verbose_name="إمكانية الاستبدال")
    return_possibility = models.BooleanField(default=True, verbose_name="إمكانية الإرجاع")
    max_return_days = models.IntegerField(verbose_name='اقصى مدة استرجاع', default=3)
    max_replace_days = models.IntegerField(verbose_name='اقصى مدة استبدال', default=3)
    partners_percentage = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='نسبة الشركاء' , default=0.0)
    free_delivery =  models.BooleanField(default=False, verbose_name='توصيل مجاني؟' )
    expected_days = models.IntegerField(verbose_name=" الأيام المتوقعة لوصول الطلب", default=7)
    
    @classmethod
    def get_settings(cls):
        """إرجاع الإعدادات الحالية أو إنشاء سجل جديد إذا لم يكن موجودًا"""
        # يتم استعمالها في جلب التوصيل في صفحة العرض تحديدا دالة السلة
        settings = cls.objects.first()
        if not settings:
            settings = cls.objects.create()
        return settings
    
    def __str__(self):
        return "الإعدادات"
    
    class Meta:
        verbose_name = "الإعدادات"
        verbose_name_plural = "الإعدادات"
            
class Social(models.Model):
    facebook = models.URLField(verbose_name='فيسبوك', blank=True)
    tiktok = models.URLField(verbose_name='تيكتوك', blank=True)
    whatsapp = models.CharField(verbose_name='رقم الواتساب', blank=True, max_length=20)
    phone_number1 = models.CharField(verbose_name='رقم الهاتف الاساسي', null=True, max_length=20)
    phone_number2 = models.CharField(verbose_name='رقم الهاتف الثانوي', null=True, max_length=20)
    email = models.EmailField(verbose_name='ايميل', blank=True)
    
    class Meta:
        verbose_name = "حسابات الموقع"
        verbose_name_plural = "حسابات الموقع"
    
