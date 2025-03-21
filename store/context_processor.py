from django.db.models import Count
from django.core.cache import cache
from store.models import *
from accounts.models import  UserProfile, Inbox
from settings.models import Social

def social_data(request):
    
    # جلب حسابات الموقع من الكاش أو قاعدة البيانات
    social = cache.get('social')
    if not social:
        social = Social.objects.first()
        if social:
            cache.set('social', social, 60 * 60)
        else:
            return {
                'facebook_link': "#",
                'tiktok_link': "#",
                'whatsapp_link':"#",
                'phone_number1': "#",
                'phone_number2': "#",
                'email': "#",
            }
        
    return {
        'facebook_link': social.facebook,
        'tiktok_link': social.tiktok,
        'whatsapp_link': social.whatsapp,
        'phone_number1': social.phone_number1,
        'phone_number2': social.phone_number2,
        'email': social.email,
    }
    
    
def globals(request):
    
    user = request.user
       
    # تحقق من وجود men_category في الكاش
    men_category = cache.get('men_category')
    if not men_category:
        try:
            men_category = Category.objects.get(slug='men')
            cache.set('men_category', men_category, timeout=60*60)  # تخزينه في الكاش لمدة ساعة
            # تحقق من وجود men_categories في الكاش
            men_categories = cache.get('men_categories')
            if not men_categories:
                men_categories = Category.objects.filter(parent_category=men_category, status='visible') \
                    .annotate(product_count=Count('products')) \
                    .order_by('-product_count') \
                    .only('slug', 'name')[:5]
                cache.set('men_categories', men_categories, timeout=60*60)  # تخزينه في الكاش لمدة ساعة    
        except Category.DoesNotExist:
            men_category = None
            men_categories = None
    else:
        men_categories = cache.get('men_categories')
        
    # تحقق من وجود women_category في الكاش
    women_category = cache.get('women_category')
    if not women_category:
        try:
            women_category = Category.objects.get(slug='women')
            cache.set('women_category', women_category, timeout=60*60)  # تخزينه في الكاش لمدة ساعة
            # تحقق من وجود women_categories في الكاش
            women_categories = cache.get('women_categories')
            if not women_categories:
                women_categories = Category.objects.filter(parent_category=women_category, status='visible') \
                    .annotate(product_count=Count('products')) \
                    .order_by('-product_count')[:5]
                cache.set('women_categories', women_categories, timeout=60*60)  # تخزينه في الكاش لمدة ساعة
        except Category.DoesNotExist:
            women_category = None
            women_categories = None
    else:
        women_categories = cache.get('women_categories')
    
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
        'favourite_products': favourite_products,
        'user_points': user_points,
        'unread_messages_count': unread_messages_count,
    }    