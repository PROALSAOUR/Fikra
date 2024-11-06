from django.db import models
from django.core.exceptions import ValidationError
import phonenumbers


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
# كلاس الشركاء 
class Partners(models.Model):
    name = models.CharField(max_length=250 , verbose_name='الاسم')
    phone_number = models.CharField( max_length=15, verbose_name='رقم الهاتف',  unique=True)
    share_percentage = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='النسبة')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنضمام')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التعديل')
    def clean_phone_number(self):
        phone_number = self.phone_number
        if not phone_number:  # التحقق من أن الرقم غير فارغ
            raise ValidationError("رجاء قم بإدخال رقم الهاتف")
        
        try:
            # التحقق من صحة رقم الهاتف باستخدام phonenumbers
            parsed_phone = phonenumbers.parse(phone_number, 'LY')  # يمكنك تغيير 'LY' إلى بلد مناسب
            if not phonenumbers.is_valid_number(parsed_phone):
                raise ValidationError("رقم الهاتف غير صالح.")
        except phonenumbers.NumberParseException:
            raise ValidationError("يرجى إدخال رقم هاتف صحيح.")
        return phone_number
    
    def clean(self):
        self.clean_phone_number() # التحقق ان ارقام الهاتق صالحة
        # التحقق أن نسب الشركاء مجتمعة ليست فوق 100%
        total_percentage = Partners.objects.exclude(id=self.id).aggregate(total=models.Sum('share_percentage'))['total'] or 0
        if total_percentage + self.share_percentage > 100:
            raise ValidationError('المجموع الإجمالي لنسب الشركاء سوف يتجاوز ال %100')

    def __str__(self) -> str:
        return f'{self.name}'
    
    class Meta:
        verbose_name = 'شريك'
        verbose_name_plural = 'الشركاء'
# كلاس ارباح الشركاء شهريا
class PartnersProfit(models.Model):
    month = models.ForeignKey('MonthlyTotal', on_delete=models.CASCADE, verbose_name='الشهر', related_name='partners_monthly_profits')
    partner = models.ForeignKey(Partners, on_delete=models.CASCADE, verbose_name='الشريك', related_name='partner_profits')
    profit = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='الربح', null=True)
    received = models.BooleanField(default=False, verbose_name='تم التسليم؟')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التعديل')
    
    
    def __str__(self) -> str:
        return f'{self.month} => {self.partner.name}'
    
    class Meta:
        verbose_name = 'الربح'
        verbose_name_plural = "الأرباح"        
# كلاس المستثمرين
class Investigator(models.Model):
    name = models.CharField(max_length=50, verbose_name='الاسم')
    phone_number = models.CharField(max_length=15, verbose_name='رقم الهاتف')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنضمام')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التعديل')
    def clean_phone_number(self):
        phone_number = self.phone_number
        if not phone_number:  # التحقق من أن الرقم غير فارغ
            raise ValidationError("رجاء قم بإدخال رقم الهاتف")
        
        try:
            # التحقق من صحة رقم الهاتف باستخدام phonenumbers
            parsed_phone = phonenumbers.parse(phone_number, 'LY')  # يمكنك تغيير 'LY' إلى بلد مناسب
            if not phonenumbers.is_valid_number(parsed_phone):
                raise ValidationError("رقم الهاتف غير صالح.")
        except phonenumbers.NumberParseException:
            raise ValidationError("يرجى إدخال رقم هاتف صحيح.")
        return phone_number
    
    def clean(self):
        self.clean_phone_number() # التحقق ان ارقام الهاتق صالحة
    
    def __str__(self) -> str:
        return f'{self.name}'
    
    class Meta:
        verbose_name = 'مستثمر'
        verbose_name_plural = 'المستثمرين'    
# كلاس ربح المستثمر
class InvestigatorProfit(models.Model):
    month = models.ForeignKey('MonthlyTotal', on_delete=models.CASCADE, verbose_name='الشهر', related_name='investigator_monthly_profits')
    from_group =  models.ForeignKey('InvestmentGroup', on_delete=models.CASCADE, verbose_name='من المجموعة', related_name='investigator_group_profits' ,null=True)
    investigator = models.ForeignKey(Investigator, on_delete=models.CASCADE, verbose_name='المستثمر', related_name='investigator_profits')
    profit = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='الربح')
    received = models.BooleanField(default=False, verbose_name='تم التسليم؟')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التعديل')
    
    def __str__(self) -> str:
        return f'{self.month} => {self.investigator.name}'
    
    class Meta:
        verbose_name = 'ربح المستثمر'
        verbose_name_plural = 'ارباح المستثمرين'
# كلاس مجموعة استثمارية
class InvestmentGroup(models.Model):
    name = models.CharField(max_length=50, verbose_name='الاسم')
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='الحصة', null=True)
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='المبلغ المتبقي', null=True)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="العوائد", null=True)
    ready = models.BooleanField(default=False , verbose_name="جاهزة؟") # هل المجموعة مكتملة الاعضاء وجاهزة لتوزيع الارباح
    completed = models.BooleanField(default=False , verbose_name="مكتملة؟") # هل المجموعة تم توزيع ارباحها بالكامل؟
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التعديل')
        
    def check_if_completed(self):
        "التحقق من وجود مبلغ متبقي للمجموعة والا تغير الحالة الى  مكتملة"
        if self.remaining_amount:
            if self.remaining_amount <= 0 :
                self.completed = True
                
    def save(self, *args, **kwargs):
        self.check_if_completed()
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return f'{self.name}'
    
    class Meta:
        verbose_name = 'مجموعة استثمارية'
        verbose_name_plural = 'المجموعات الاستثمارية '
# كلاس ربط بين المستثمرين ومجموعاتهم الاستثمارية
class InvestmentGroupMember(models.Model):
    investigator = models.ForeignKey(Investigator, on_delete=models.CASCADE, verbose_name='المستثمر', related_name='members')  
    group = models.ForeignKey(InvestmentGroup, on_delete=models.CASCADE, verbose_name='المجموعة', related_name='members')  
    investment_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=" المبلغ المستثمر")
    investment_percentage = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0, verbose_name='النسبة')
    profit_value = models.DecimalField(max_digits=10, decimal_places=2,  null=True, default=0, verbose_name='العائد')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنضمام')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التعديل')
    
    def __str__(self) -> str:
        return f"{self.investigator.name} => {self.group.name}"
    
    class Meta:
        verbose_name = 'عضو'
        verbose_name_plural = "الأعضاء"
# نموذج الربط بين الإحصائيات الشهرية والمجموعات الاستثمارية
class MonthlyInvestmentGroup(models.Model):
    monthly_total = models.ForeignKey("MonthlyTotal", on_delete=models.CASCADE, verbose_name='إحصائية شهرية', related_name='investment_groups')
    investment_group = models.ForeignKey(InvestmentGroup, on_delete=models.CASCADE, verbose_name='المجموعة', related_name='monthly_totals')
    monthly_percentage = models.DecimalField(max_digits=3, decimal_places=2, verbose_name="النسبة الشهرية", null=True)
    goods_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="من البضاعة", null=True)
    profit_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="من الربح", null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=" الإجمالي", null=True)
    def __str__(self):
        return f"{self.monthly_total} - {self.investment_group}"

    class Meta:
        verbose_name = 'مجموعة استثمارية شهرية'
        verbose_name_plural = 'المجموعات الاستثمارية الشهرية'

# ======================== Total Profits & Costs ================================
# كلاس احصائية لكل شهر
class MonthlyTotal(models.Model):
    month = models.IntegerField(verbose_name='الشهر') # رقم الشهر
    year = models.IntegerField(verbose_name='السنة') # رقم السنة
    total_income = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=' الدخل',  null=True, default=0)
    additional_income =  models.DecimalField(max_digits=10, decimal_places=2, verbose_name=' الإضافات',  null=True, default=0)
    total_costs = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=' المصاريف' , null=True, default=0)
    total_packaging = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='إجمالي التغليف', null=True, default=0)
    goods_price =  models.DecimalField(max_digits=10, decimal_places=2, verbose_name='سعر البضاعة', null=True, default=0)
    total_profit = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='إجمالي الربح', null=True, default=0)
    sales_number = models.IntegerField(null=True, verbose_name='المنتجات المباعة', default=0) # عدد الامنتجات المباع بالشهر
    
    def __str__(self) -> str:
        return f"{self.month}/{self.year}"
    
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
# كلاس للمصاريف
class Cost(models.Model):
    month = models.ForeignKey(MonthlyTotal, on_delete=models.CASCADE, related_name='costs' , verbose_name='شهر')
    title = models.CharField(verbose_name='الاسم')
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='التكلفة')
    description = models.TextField(verbose_name='الوصف' , null=True, blank=True)
    
    def __str__(self) -> str:
        return f'{self.title} => {self.value}'
    
    class Meta:
        verbose_name = 'مصروف'
        verbose_name_plural = 'المصاريف'
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
        verbose_name_plural = 'الإضافات'

# ===============================================

