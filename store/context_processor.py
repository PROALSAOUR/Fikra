from django.db.models import Count
from store.models import *

def globals(request):
    men_categores = Category.objects.filter(parent_category__name='رجالي').annotate(product_count=Count('products')).order_by('-product_count')[:5]
    women_categores = Category.objects.filter(parent_category__name='نسائي').annotate(product_count=Count('products')).order_by('-product_count')[:5]
    
    return {
        'men_categores': men_categores,
        'women_categores': women_categores,
    }


    