from cards.models import *
from store.models import *
from accounts.models import UserProfile
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from itertools import chain
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from accounts.send_messages import buy_copon_done_message, receive_copon_done_message

# ===================================================
# مستودع البطاقات
def cards_repo(request):
    user = request.user
    
    user_copons = CoponItem.objects.filter(user=user, has_used=False).prefetch_related('copon_code')
    
    active_copons =  user_copons.filter(expire__gte=now().date()).order_by('-purchase_date')
    expired_copons  = user_copons.filter(expire__lt=now().date()).order_by('-purchase_date')[:5]
    
    copons_count = active_copons.count() + expired_copons.count()
    
    # =================================================================

    context  = {
        'active_copons': active_copons,
        'expired_copons': expired_copons,
        'copons_count': copons_count,
    }
    
    return render(request, 'cards/cards-repo.html',context)
# صفحة متجر البطاقات
def cards_store(request):
    #  خاص بالكوبونات
    
    copons_list = Copon.objects.filter(is_active=True).only('name','value','img','price', 'expiration_days').order_by('-sales_count')
        
    paginator_all = Paginator(copons_list, 20)  

    page_all = request.GET.get('page_all', 1)
    
    try:
        copons = paginator_all.page(page_all)
    except PageNotAnInteger:
        copons = paginator_all.page(1)
    except EmptyPage:
        copons = paginator_all.page(paginator_all.num_pages)
    
    # =====================================================
    
    # إضافة فلترة أخرى بناءً على معايير المستخدم (البحث، السعر، العلامة التجارية)
    query = request.GET.get('q', '')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
   
    filters = Q(is_active=True)
    
    if query:
        filters &= (Q(name__icontains=query) | Q(tags__name__icontains=query)) 

    if price_min and price_min.isdigit():
        price_min = int(price_min)
        filters &= Q(price__gte=price_min) 
        
    if price_max and price_max.isdigit():
        price_max = int(price_max)
        filters &= Q(price__lte=price_max)
    
    # جلب المنتجات بناءً على الفلاتر
    results_list = list(chain(
    Copon.objects.filter(filters).distinct()
    ))
    
    # إعداد التصفح المرقم
    paginator = Paginator(results_list, 20)  # عرض 20 منتجًا في كل صفحة
    page = request.GET.get('page', 1)

    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    results_count = len(results_list)
    
    # =====================================================
    
    context  = {
        'copons': copons,
        'results':results,
        'results_count':results_count,
    }
    return render(request, 'cards/cards-store.html',context)
# صفحة تفاصيل الكوبون
def copon_details(request, cid):
     
    copon = get_object_or_404(Copon, id=cid)
        
    context  = {
        'copon': copon,
    }
    return render(request, 'cards/copon-details.html', context)
# دالة شراء كوبون من اي مكان
@login_required
def buy_copon(request, cid):
    """
    دالة للتحقق من الكوبون المراد شرائه
    """
    # الحصول على الكوبون والمستخدم
    copon = get_object_or_404(Copon, id=cid)
    user = request.user
    profile = get_object_or_404(UserProfile, user=user)
    inbox = profile.inbox
    
    points = profile.points
    
    # التحقق من أن المستخدم لديه نقاط كافية
    if copon.price > points:
        return JsonResponse({'error': 'لاتوجد نقاط كافية لإتمام عملية الشراء'}, status=400)
       
    user_copon = CoponItem.objects.create(
        user=user,
        copon_code=copon,    
    )
        
    # ارسال رسالة عند شراء كوبون
    message = buy_copon_done_message(user_name=user_copon.user.first_name, copon_name=user_copon.copon_code)
    inbox.add_message(message)
    
    # خصم النقاط وحفظ التحديثات
    points -= copon.price
    profile.points = points
    profile.save()
    
    # حفظ سجل استخدام الكوبون
    copon.sales_count += 1 
    user_copon.buy_copon()
    copon.save()
    user_copon.save()

    return JsonResponse({'success': 'تم شراء الكوبون بنجاح'}, status=200)
# دالة استلام هدية من الكود 
@login_required
def verfie_code(request):
    user = request.user

    if request.method == 'POST':        
        try:
            data = json.loads(request.body)
            verfie_code = data.get('verfie-code')
        
            try:
                verfie_copon = ReceiveCopon.objects.get(code=verfie_code)

                if verfie_copon.is_used:
                    return JsonResponse({"success": False, "message": "الكود الذي ادخلته مستخدم بالفعل"})

                # إنشاء CoponItem جديد
                copon_item = CoponItem.objects.create(
                    user=user,
                    copon_code=verfie_copon.copon,   
                    receive_from_code=True, 
                )

                verfie_copon.copon.sales_count += 1 
                copon_item.buy_copon()
                verfie_copon.copon.save()
                copon_item.save()
                
                # تحديث حالة الكود إلى "مستخدم"
                verfie_copon.is_used = True
                verfie_copon.used_by = user
                verfie_copon.save()
                
                # ارسال رسالة عند اتمام استلام الكوبون
                message = receive_copon_done_message(user_name=request.user.first_name, copon_name=verfie_copon.copon)
                request.user.inbox.add_message(message)
                
                return JsonResponse({"success": True, "message": 'تهانينا! تم استلام الكوبون بنجاح.'})

            except ReceiveCopon.DoesNotExist:
                return JsonResponse({"success": False, "message": "الكود غير صحيح."})
            
        except ReceiveCopon.DoesNotExist:
            return JsonResponse({"success": False, "message": 'نعتذر حصلت مشكلة اثناء معالجة البيانات!'})

    return JsonResponse({"success": False, "message": "حدث خطأ ما."})

# ===================================================