from django.shortcuts import render, get_object_or_404
from store.models import *

def index(request):
    # جلب الإعلانات التي يتم عرضها
    ads = AdsSlider.objects.filter(show=True)
    
    # جلب العلامات التجارية المميزة
    brands = Brand.objects.filter(featured=True).only('title', 'img')
    
    # جلب الفئات المميزة والظاهرة فقط، وتحميل المنتجات التابعة لهذه الفئات
    categories = Category.objects.filter(
        featured=True,
        status='visible',
        gender_cat=False,
    ).prefetch_related(
        'products'
    ).filter(
        products__featured=True,
        products__ready_to_sale=True
    ).distinct()[:8] # عدد اقسام المنتجات المطلوب عرضها بالصفحة الرئيسية
    
    offered_products = Product.objects.filter(offer = True)[:10]
    
    context = {
        'ads': ads,
        'brands': brands,
        'categories': categories,
        'offered_products':offered_products,
    }
    
    return render(request, 'store/index.html', context)

def brand_page(request, slug):
    brand = get_object_or_404(Brand, title=slug)
    products = Product.objects.filter(brand=brand)[:12]
    last_products = Product.objects.filter(brand=brand).order_by('-updated_at')[:12]
    offerd_products = Product.objects.filter(brand=brand, offer=True)[:12]
    
    context = {
        'products': products,
        'last_products': last_products,
        'offerd_products':offerd_products,
        'brand': brand,
    }
    
    return render(request, 'store/brand.html', context)

def category_page(request, id):
    
    category = get_object_or_404(Category, id=id)
    
    # استرجاع التصنيفات الفرعية التي تنتمي للتصنيف الأب
    subcategories = Category.objects.filter(parent_category=category)
    
    # استرجاع المنتجات التي تنتمي للتصنيفات الفرعية
    subcategory_products = Product.objects.filter(category__in=subcategories)
    
    # استرجاع المنتجات التي تنتمي للتصنيف الأب مباشرة
    parent_category_products = Product.objects.filter(category=category)
    
    # دمج المنتجات من التصنيف الأب والتصنيفات الفرعية
    combined_products = parent_category_products | subcategory_products
    
    # حساب العدد الكلي للمنتجات
    total_products_count = combined_products.count()
    
    # الحصول على المنتجات التي سيتم عرضها (احصرها إلى 12)
    products = combined_products.distinct()[:12]
    
    context = {
        'products': products,
        'category': category,
        'subcategories': subcategories,
        'total_products_count': total_products_count,  # إضافة العدد الكلي إلى السياق
    }
    return render(request, 'store/category.html', context)







