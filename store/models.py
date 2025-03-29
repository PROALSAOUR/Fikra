from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.html import mark_safe
from shortuuid.django_fields import ShortUUIDField
from accounts.models import User
import string

# ======================== Product ======================================

class AdsSlider(models.Model):
    
    ads_options = [
        ('category', 'تصنيف'),
        ('one_product', 'منتج معين'),
        ('special_products', ' منتجات خاصة'),
        ('just_show', 'منظر فقط'),
    ]
    
    title = models.CharField(max_length=255 , verbose_name='العنوان')
    slug = models.SlugField(max_length=100, unique=True , verbose_name='slug')
    img = models.ImageField( upload_to='store/Ads' , verbose_name='الصورة')
    show = models.BooleanField( default=False , verbose_name='عرض')
    info = models.TextField(null=True, blank=True , verbose_name='الوصف')
    ads_for = models.CharField(choices=ads_options, max_length=20, default='special_products' , verbose_name='إعلان من اجل ')
    category = models.ForeignKey('Category', null=True, blank=True, related_name='ads', on_delete=models.CASCADE , verbose_name='اعلان للتصنيف ..')
    one_product = models.ForeignKey('Product', null=True, blank=True, related_name='ads', on_delete=models.CASCADE , verbose_name='اعلان للمنتج..')
    created_at = models.DateTimeField(auto_now_add=True , verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True , verbose_name='تاريخ التحديث')
    
    def get_ad_url(self):
        if self.ads_for == 'category':
            return reverse('store:category', kwargs={'slug': self.category.slug})
        elif self.ads_for == 'one_product':
            return reverse('store:product_details', kwargs={'pid': self.one_product.id})
        elif self.ads_for == 'special_products':
            return reverse('store:ad_details', kwargs={'slug': self.slug})
        else:
            return reverse('store:home')
    
    def clean(self):
        super().clean() 

        if self.ads_for == 'category' and not self.category:
            raise ValidationError('Category Ads must be linked to a Category.')
        elif self.ads_for == 'one_product' and not self.one_product:
            raise ValidationError('One Product Ads must be linked to a Product.')

    def ad_image(self):
        return mark_safe("<img src='%s' width='80' height='50'/>" % (self.img.url) )
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'اعلان'
        verbose_name_plural = 'الاعلانات'
    
class AdsProducts(models.Model):
    product =  models.ManyToManyField('Product', related_name='products' , verbose_name='المنتج') 
    Ads_name = models.ForeignKey(AdsSlider, null=True, blank=True, related_name='adsproducts', on_delete=models.CASCADE , verbose_name='الإعلان')
   
class Brand(models.Model):
    title = models.CharField(max_length=255 , verbose_name='الاسم')
    img = models.ImageField( upload_to='store/Brands' , verbose_name='الصورة')
    featured = models.BooleanField(default=False , verbose_name='مميز')
        
    def __str__(self) -> str:
        return self.title
    
    def brand_image(self):
        return mark_safe("<img src='%s' width='50' height='50'/>" % (self.img.url) )
    
    def products_count(self):
        return self.products.count()
    
    class Meta:
        verbose_name = 'علامة تجارية'
        verbose_name_plural = 'العلامات تجارية'

class SizeCategory(models.Model):
    name = models.CharField(max_length=80 , verbose_name='اسم الفئة')
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'فئة المقاسات'
        verbose_name_plural = 'فئات المقاسات'

class SizeOption(models.Model):
    value = models.CharField(max_length=20 , verbose_name='القيمة')
    size_category = models.ForeignKey(SizeCategory, on_delete=models.CASCADE, related_name='size_options' , verbose_name='فئة المقاس')
    
    def __str__(self) -> str:
        return self.value
    
    class Meta:
        verbose_name = 'مقاس'
        verbose_name_plural = 'المقاسات'

class Category(models.Model):
    status_choices = [
        ('visible', 'ظاهر'),
        ('hiddin', 'مخفي'),
    ]
    
    name = models.CharField(max_length=100 , verbose_name='الاسم')
    slug = models.SlugField(max_length=100, unique=True , verbose_name='slug')
    img = models.ImageField( upload_to='store/categories' , verbose_name='الصورة') 
    gender_cat = models.BooleanField(default=False , verbose_name='تصنيف جنسي؟') 
    featured = models.BooleanField(default=False , verbose_name='مميز؟')
    status = models.CharField(choices=status_choices, max_length=20, default='visible' , verbose_name='الظهور')
    size_category = models.ForeignKey(SizeCategory, on_delete=models.CASCADE, null=True, blank=True , verbose_name='فئة المقاس')
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE,  null=True, blank=True , verbose_name='التصنيف الأب')
    
    def category_image(self):
        return mark_safe("<img src='%s' width='50' height='50'/>" % (self.img.url) )
    
    def __str__(self) -> str:
        return self.name
    
    def products_count(self):
        return self.products.count()
    
    class Meta:
        verbose_name = 'تصنيف'
        verbose_name_plural = 'التصنيفات'

class Repository(models.Model):
    name = models.CharField(max_length=100 , verbose_name='المستودع')
        
    def __str__(self) -> str:
        return self.name
        
    class Meta:
        verbose_name = 'مستودع'
        verbose_name_plural = 'المستودعات'

class Tag(models.Model):
    name = models.CharField(max_length=20, blank=True , verbose_name='الإسم')
    
    def __str__(self) -> str:
        return self.name
    
    def tag_count(self):
        return self.products.count()
    
    class Meta:
        verbose_name = 'هاشتاج'
        verbose_name_plural = 'هاشتاج'

class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=12, max_length=30, prefix='pr', alphabet= string.ascii_lowercase + string.digits , verbose_name='المعرف')
    name = models.CharField(max_length=255 , verbose_name='الاسم')
    description = models.TextField(verbose_name='الوصف')
    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.CASCADE , verbose_name='البراند')
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE , verbose_name='التصنيف')
    repository =  models.ForeignKey(Repository, related_name='products', on_delete=models.CASCADE , verbose_name='المستودع',)
    tag = models.ManyToManyField(Tag, related_name='products' , verbose_name='الهاشتاج')
    thumbnail_img = models.ImageField(upload_to='store/Products/thumbnails' , verbose_name='صورة العرض')
    featured = models.BooleanField(default=False , verbose_name='مميز؟')
    purchase_price =  models.IntegerField(default=0 , verbose_name='سعر الشراء') 
    price = models.IntegerField(default=0 , verbose_name='سعر البيع') 
    new_price = models.IntegerField( blank=True, null=True , verbose_name='سعر التخفيض')
    bonus =  models.IntegerField(blank=True, null=True, default=20 , verbose_name='المكافأة')
    offer = models.BooleanField(default=False , verbose_name='مخفض؟')
    ready_to_sale = models.BooleanField(default=False , verbose_name='معروض؟')
    available = models.BooleanField(default=False , verbose_name='متوفر؟')
    total_sales = models.IntegerField(blank=True, null=True, default=0 , verbose_name='إجمالي البيع')
    url = models.URLField(blank=True, null=True, verbose_name='رابط المنتج')
    upload_at = models.DateTimeField(auto_now_add=True , verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True , verbose_name='تاريخ التحديث')     
    

    def __str__(self) -> str:
        return self.name
    
    def product_thumbnail(self):
        # دالة مسؤولة عن عرض صورة المنتج المصغرة في لوحة الادارة
        return mark_safe("<img src='%s' width='50' height='50'/>" % (self.thumbnail_img.url) )
    
    def get_offer_percentage(self):
        if self.new_price and self.new_price < self.price:
            discount_percentage = ((self.price - self.new_price) / self.price) * 100
            return round(discount_percentage, 1)
        return 0

    def get_price(self):
        """تعيد سعر المنتج وفقا لحالة التخفيض """
        if self.offer :
            return self.new_price
        else:
            return self.price
            
    def get_total_stock(self):
        """
        تستعمل هذه الدالة للتحقق من ان المنتج متاح بالمخزن 
        """
        total_stock = 0
        for item in self.items.all():
            for variation in item.variations.all():
                total_stock += variation.stock
        return total_stock
    
    def get_sales_count(self):
        '''
        دالة وظيفتها حساب عدد مبيعات المنتج الاجمالية بمحتلف متغيراته
        '''
        total_sales_count = 0
        for item in self.items.all():
            for variation in item.variations.all():
                total_sales_count  += variation.sold
        
        self.total_sales =  total_sales_count
        self.save()
    
    
    class Meta:
        verbose_name = 'منتج'
        verbose_name_plural = 'المنتجات'

class ProductImages(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE , verbose_name='المنتج')
    image = models.ImageField(upload_to='store/Products/images' , verbose_name='الصورة')
    
    def __str__(self):
        return self.product.name
    
    class Meta:
        verbose_name = 'صورة المنتج'
        verbose_name_plural = 'صور المنتج'

class ProductItem(models.Model):
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE , verbose_name='المنتج')
    sku = ShortUUIDField(unique=True, prefix='sku',  length=8, max_length=20, alphabet= string.ascii_lowercase + string.digits , verbose_name='sku')
    color =  models.CharField(max_length=255 , verbose_name='اللون')
    image = models.ImageField(upload_to='store/Products/product_items/', null=True , verbose_name='الصورة')
    
    def item_image(self):
        return mark_safe("<img src='%s' width='50' height='50'/>" % (self.image.url) )

    def __str__(self) -> str:
        return str(self.sku)
    
    class Meta:
        verbose_name = 'متغير المنتج'
        verbose_name_plural = 'متغيرات المنتج'

class ProductVariation(models.Model):
    product_item = models.ForeignKey(ProductItem, related_name='variations', on_delete=models.PROTECT, verbose_name='العنصر')
    size = models.ForeignKey(SizeOption, related_name='variations', on_delete=models.PROTECT , verbose_name='المقاس')
    stock = models.IntegerField(default=0 , verbose_name='الكمية')  # الكمية المتاحة
    sold = models.IntegerField(default=0 , verbose_name='المباع')  # الكمية المباعة
    created_at = models.DateTimeField(auto_now_add=True , verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True , verbose_name='تاريخ التعديل')

    def __str__(self):
        return f"{self.product_item} - {self.product_item.color} - {self.size}"

    def update_stock(self, quantity_change):
        """
        This method updates the stock and ensures the stock never goes negative.
        """
        if self.stock + quantity_change >= 0:
            self.stock += quantity_change
            self.save()
        else:
            raise ValueError("مخزون غير كاف!")

    def sell(self, quantity):
       self.stock -= quantity
       self.sold += quantity
       self.save()
    
    def return_product(self, quantity):
        """دالة ارجاع كميات المنتج المستبدل او المرجع الى المخزون """
        self.update_stock(quantity)  # إعادة الكمية القديمة إلى المخزون
        self.sold -= quantity # تحديث الكمية المباعة
        self.save()
                
    @property
    def item_thumbnail(self):
        return self.product_item.item_image # استرجع صورة المصغرة من المنتج

    class Meta:
        verbose_name = 'المخزون'
        verbose_name_plural = 'المخزون'
    
class Interested(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interested_products' , verbose_name='المستخدم')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='interested_by' , verbose_name='المنتج')
    created_at = models.DateTimeField(auto_now_add=True , verbose_name='تاريخ الإنشاء')
    
    def __str__(self):
        return f"{self.user.phone_number}متابعة المنتج {self.product.name}"    
        
    class Meta:
        verbose_name = 'طلب توفير منتج'
        verbose_name_plural = 'منتجات مطلوب توفيرها'    
# ========================== Favourite ===================================
class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourites' , verbose_name='المستخدم')
    products = models.ManyToManyField(Product , verbose_name='المنتج')
    
    def __str__(self):
        return f"{self.user.phone_number}قائمة المفضلة الخاصة ب"
    
# ============================= Cart ====================================

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts' , verbose_name='المستخدم')
    
    def __str__(self) -> str:
        return f'سلة : {self.user.first_name} {self.user.last_name}'
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items' , verbose_name='السلة')
    cart_item = models.ForeignKey(ProductVariation, on_delete=models.CASCADE, related_name='cart_variations' , verbose_name='عنصر السلة')
    qty = models.PositiveIntegerField(default=1 , verbose_name='الكمية')
    
    def get_stock_quantity(self):
        """
        تعيد الكمية المتاحة في المخزون بناءً على الكمية المطلوبة.
        إذا كانت الكمية المطلوبة أكبر من المخزون المتاح، تعيد 0.
        """
        available_stock = self.cart_item.stock
        return max(0, available_stock - self.qty)
    
    def update_qty(self, new_qty):
        if new_qty < 1:
            raise ValueError("الكمية يجب أن تكون أكبر من 0.")
        if new_qty > self.cart_item.stock:
            raise ValueError("الكمية المطلوبة أكبر من المخزون المتاح.")
        self.qty = new_qty
        self.save()

