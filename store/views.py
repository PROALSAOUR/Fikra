from django.shortcuts import render
from store.models import *

def index(request):
    # جلب الإعلانات التي يتم عرضها
    ads = AdsSlider.objects.filter(show=True)
    
    # جلب العلامات التجارية المميزة
    brands = Brand.objects.filter(featured=True).only('title', 'img')
    
    # جلب الفئات المميزة والظاهرة فقط، وتحميل المنتجات التابعة لهذه الفئات
    categories = Category.objects.filter(
        featured=True,
        status='visible'
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
