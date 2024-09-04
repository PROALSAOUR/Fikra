from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from store.models import *

# الصفحة الرئيسية
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
# صفحة الاعلان
def ads_page(request, slug):
    ad = get_object_or_404(AdsSlider, slug=slug)
    ad_content = AdsProducts.objects.filter(Ads_name=ad).prefetch_related('product')
    
    context = {
        'ad_content': ad_content,
        'ad': ad,
    }
    return render(request, 'store/ads-details.html', context)
# صفحة العلامة التجارية
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
# صفحة التصنيف
def category_page(request, slug):
    
    category = get_object_or_404(Category, slug=slug)
    
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
# صفحة العروض
def offer_page(request):
    offerd_products = Product.objects.filter(offer=True, ready_to_sale=True).order_by('-new_price')
    products_count = offerd_products.count()
    
    context  ={
        'offerd_products': offerd_products,
        'products_count': products_count,
    }
    return render(request, 'store/offer-products.html', context)
# صفحة البحث
from django.db.models import Q

def search_page(request):
    query = request.GET.get('q', '')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    category_id = request.GET.get('category')
    brand_id = request.GET.get('brand')

    filters = Q(ready_to_sale=True)

    if query:
        filters &= (Q(name__icontains=query) | Q(tag__name__icontains=query))

    if price_min and price_min.isdigit():
        price_min = int(price_min)
        filters &= Q(
            Q(new_price__gte=price_min, payment_type='money') | 
            (Q(offer=False) & Q(price__gte=price_min, payment_type='money'))
        )
        
    if price_max and price_max.isdigit():
        price_max = int(price_max)
        filters &= Q(
            Q(new_price__lte=price_max, payment_type='money') | 
            (Q(offer=False) & Q(price__lte=price_max, payment_type='money'))
        )
        
    if category_id:
        # جلب التصنيف الأب
        parent_category = get_object_or_404(Category, id=category_id)
        # جلب التصنيفات الفرعية
        subcategories = Category.objects.filter(parent_category=parent_category)
        # دمج التصنيف الأب والتصنيفات الفرعية
        category_ids = [parent_category.id] + list(subcategories.values_list('id', flat=True))
        filters &= Q(category_id__in=category_ids)
    if brand_id:
        filters &= Q(brand_id=brand_id)

    results = Product.objects.filter(filters).distinct()
    
 # إعداد التصفح المرقم
    paginator = Paginator(results, 20)  # عرض 20 منتجًا في كل صفحة
    page = request.GET.get('page', 1)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        results_data = list(products.object_list.values())
        return JsonResponse({'results': results_data})

    categories = Category.objects.filter(status='visible')
    brands = Brand.objects.all()
    products_count = results.count()

    return render(request, 'store/search.html', {
        'products': products,
        'categories': categories,
        'brands': brands,
        'products_count': products_count, 
    })
