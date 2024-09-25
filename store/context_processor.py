from django.db.models import Count
from store.models import *
from blog.models import BlogPage
from accounts.models import  UserProfile, Inbox
from django.shortcuts import get_object_or_404

def globals(request):
    
    user = request.user
    
    about_us = get_object_or_404(BlogPage.objects.only('slug'), slug='about-us')
   
    men_category =  Category.objects.get(slug='men')
    women_category =  Category.objects.get(slug='women')
     
    men_categories = Category.objects.filter(parent_category=men_category, status='visible').annotate(product_count=Count('products')).order_by('-product_count').only('slug', 'name')[:5]
    women_categories = Category.objects.filter(parent_category=women_category, status='visible').annotate(product_count=Count('products')).order_by('-product_count')[:5]
    
    if user.is_authenticated:
        
        favourite, created = Favourite.objects.get_or_create(user=user) # احصل أو أنشئ المفضلة للمستخدم
        favourite_products =  favourite.products.values_list('id', flat=True) # احصل على جميع المنتجات المفضلة للمستخدم  
        
        # تحقق مما إذا كان المستخدم لديه بروفايل وصندوق بريد بالفعل
        profile, created = UserProfile.objects.get_or_create(user=user)
        if created:
            # إذا تم إنشاء بروفايل جديد، قم بإنشاء صندوق بريد خاص به
            inbox = Inbox.objects.create(user=user)
            profile.inbox = inbox
            profile.save()
        
        user_points = profile.points
        
        inbox = Inbox.objects.get(user=user)
        unread_messages = inbox.messages.filter(is_read=False).only('id')
        unread_messages_count = unread_messages.count()
        
            
    else:
        favourite_products = []
        user_points = 0
        unread_messages_count = 0
        
    return {
        'men_category': men_category,
        'women_category': women_category,
        'men_categories': men_categories,
        'women_categories': women_categories,
        'about-us':about_us,
        'favourite_products': favourite_products,
        'user_points': user_points,
        'unread_messages_count': unread_messages_count,
    }    