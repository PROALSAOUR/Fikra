from django.db import models
from django.core.exceptions import ValidationError


# ======================== Sudo Models =========================================
# نموذج وهمي لعرض اجمالي عدد المستخدمين
class UserReports(models.Model):
    class Meta:
        verbose_name_plural = 'عدد المستخدمين'
# نموذج وهمي لعرض اجمالي عدد الطلبات
class OrdersCount(models.Model):
    class Meta:
        verbose_name_plural = 'عدد الطلبات'
# ======================== Partners & investigators =============================
# نموذج الشركاء بالبرنامج
class Partners(models.Model):
    name = models.CharField(max_length=250 , verbose_name='الاسم')
    share_percentage = models.DecimalField(max_digits=5, decimal_places=2 , verbose_name='النسبة')
    
    def clean(self):
        # التحقق أن نسب الشركاء مجتمعة ليست فوق 100%
        total_percentage = Partners.objects.exclude(id=self.id).aggregate(total=models.Sum('share_percentage'))['total'] or 0
        if total_percentage + self.share_percentage > 100:
            raise ValidationError('المجموع الإجمالي لنسب الشركاء سوف يتجاوز ال %100')

    def save(self, *args, **kwargs):
        # تأكد من نظافة البيانات قبل الحفظ
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.name}'
    
    class Meta:
        verbose_name = 'شريك'
        verbose_name_plural = 'الشركاء'
# ======================== Total Profits & Costs ================================
# كلاس احصائية لكل شهر
class MonthlyTotal(models.Model):
    month = models.IntegerField(verbose_name='الشهر') # رقم الشهر
    year = models.IntegerField(verbose_name='السنة') # رقم السنة
    total_income = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='إجمالي الدخل',  null=True)
    additional_income =  models.DecimalField(max_digits=10, decimal_places=2, verbose_name='إجمالي الإضافات',  null=True)
    total_costs = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='إجمالي التكلفة' , null=True)
    total_packaging = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='إجمالي التغليف', null=True)
    goods_price =  models.DecimalField(max_digits=10, decimal_places=2, verbose_name='سعر البضاعة', null=True)
    total_profit = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='إجمال الربح', null=True)
    sales_number = models.IntegerField(null=True, verbose_name='عدد المبيعات') # عدد الامنتجات المباع بالشهر
    
    def __str__(self) -> str:
        return f"إحصائيات: {self.month}/{self.year}"
    
    class Meta:
        verbose_name = 'المجموع الشهري' 
        verbose_name_plural = 'الإحصائيات الشهرية'         
# كلاس للتغليف
class Packaging(models.Model):
    bag_price = models.DecimalField(max_digits=5, decimal_places=3 ,verbose_name="سعر الكيس")
    packaging_paper_price =  models.DecimalField(max_digits=5, decimal_places=3 , verbose_name="سعر ورق التغليف")
    thanks_card_price = models.DecimalField(max_digits=5, decimal_places=3 , verbose_name="سعر بطاقة الشكر")
    total = models.DecimalField(max_digits=10, decimal_places=3 , default=0, verbose_name="الإجمالي")
    
    def calc_total(self):
        self.total = (self.bag_price or 0) + (self.packaging_paper_price or 0) + (self.thanks_card_price or 0)
        self.save()
    
    def clean(self, *args, **kwargs):
        # تأكد من حساب الإجمالي قبل الحفظ
        self.calc_total()
        super().clean(*args, **kwargs)
    
    def __str__(self) -> str:
        return f'سعر التغليف للطلب '
    
    class Meta:
        verbose_name = 'تغليف'
        verbose_name_plural = 'ميزانية التغليف'
# كلاس لتكلفة تغليف طلب واحد مرتبط بشهر معين
class PackForMonth(models.Model):
    for_month = models.OneToOneField(MonthlyTotal, verbose_name='مرتبط ب' ,on_delete=models.CASCADE)
    one_order_packing_cost = models.DecimalField(max_digits=10, decimal_places=3 ,verbose_name="تكلفة تغليف الطلب الواحد")
    
    class Meta:
        verbose_name_plural = 'تكلفة التغليف'
# كلاس للتكاليف
class Cost(models.Model):
    month = models.ForeignKey(MonthlyTotal, on_delete=models.CASCADE, related_name='costs'  , verbose_name='شهر')
    title = models.CharField(verbose_name='الاسم')
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='التكلفة')
    description = models.TextField(verbose_name='الوصف' , null=True, blank=True)
    
    def __str__(self) -> str:
        return f'{self.title} => {self.value}'
    
    class Meta:
        verbose_name = 'تكلفة'
        verbose_name_plural = 'التكاليف'
# كلاس للدخل الإضافي
class AdditionalIncome(models.Model):
    month = models.ForeignKey(MonthlyTotal, on_delete=models.CASCADE, related_name='incomes'  , verbose_name='شهر')
    title = models.CharField(verbose_name='الاسم')
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='التكلفة')
    description = models.TextField(verbose_name='الوصف' , null=True, blank=True)
    
    def __str__(self) -> str:
        return f'{self.title} => {self.value}'
    
    class Meta:
        verbose_name = 'دخل'
        verbose_name_plural = 'المدخلات'

# ===============================================


