from django.db.models import Count
from store.models import *
from blog.models import BlogPage

def globals(request):
    men_category =  Category.objects.get(slug='men')
    about_us =  BlogPage.objects.get(slug='about-us')
    women_category =  Category.objects.get(slug='women')
    men_categories = Category.objects.filter(parent_category=men_category, status='visible').annotate(product_count=Count('products')).order_by('-product_count')[:5]
    women_categories = Category.objects.filter(parent_category=women_category).annotate(product_count=Count('products')).order_by('-product_count')[:5]

    return {
        'men_category': men_category,
        'women_category': women_category,
        'men_categories': men_categories,
        'women_categories': women_categories,
        'about-us':about_us,
    }


    