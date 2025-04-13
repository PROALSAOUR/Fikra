from cards.models import *
from store.models import *
from accounts.models import UserProfile, Banned_users
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
from accounts.send_messages import buy_copon_done_message, receive_copon_done_message
import logging
logger = logging.getLogger(__name__)  # تسجيل الأخطاء في اللوج

# ===================================================
# مستودع البطاقات
@login_required
def cards_repo(request):
    user = request.user
    today = now().date()
    user_copons = CoponItem.objects.filter(user=user, has_used=False).prefetch_related('copon_code')
    active_copons =  user_copons.filter(expire__gte=now().date()).order_by('-purchase_date')
    for copon in active_copons:
        if copon.expire and copon.expire >= today:
            copon.days_remaining = (copon.expire - today).days
        else:
            copon.days_remaining = 0  # الكوبون منتهي الصلاحية
    expired_copons  = user_copons.filter(expire__lt=now().date()).order_by('-purchase_date')[:5]
    copons_count = active_copons.count() + expired_copons.count()
    context  = {
        'active_copons': active_copons,
        'expired_copons': expired_copons,
        'copons_count': copons_count,
    }
    
    return render(request, 'cards/cards-repo.html',context)
# صفحة متجر البطاقات
def cards_store(request):    
    copons = Copon.objects.filter(is_active=True).only('name','value','img','price', 'expiration_days').order_by('value')
    context  = {
        'copons': copons,
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
    if request.user.is_authenticated:
        user = request.user
    try:
        copon = get_object_or_404(Copon, id=cid)
        profile = get_object_or_404(UserProfile, user=user)
        inbox = profile.inbox
        points = profile.points
        
        # التحقق مما إذا كان المستخدم محظورًا عبر حسابه أو رقم هاتفه
        is_banned = Banned_users.objects.filter(user=user).exists() or \
                    Banned_users.objects.filter(phone_number=user.phone_number).exists()
        if is_banned:
            return JsonResponse({'error': 'لا يمكنك شراء الكوبون، حسابك أو رقم هاتفك محظور'}, status=403)
        
    except UserProfile.DoesNotExist:
        logger.error(f"ملف المستخدم غير موجود للمستخدم: {user}.", exc_info=True)
        return JsonResponse({'error': 'حدث خطأ أثناء الحصول على ملف المستخدم'}, status=500)
    except Copon.DoesNotExist:
        logger.error(f"الكوبون غير موجود: {cid}.", exc_info=True)
        return JsonResponse({'error': 'الكوبون غير موجود'}, status=404)
    except Exception as e:
        logger.error(f"خطأ غير متوقع: {e}", exc_info=True)
        return JsonResponse({'error': 'حدث خطأ غير متوقع، الرجاء المحاولة لاحقًا'}, status=500)
    
    # التحقق من أن المستخدم لديه نقاط كافية
    if copon.price > points:
        logger.warning(f"المستخدم {user} حاول شراء كوبون {cid} بدون نقاط كافية.")
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
    # لو نقاط المستخدم صارت سالب معناها قدر يتجاوز التحقق السابق بشكل ما واشترى الكوبون بدون ما يدفع
    if profile.points < 0 :
        logger.warning(f"نقاط المشتري {user} اصبحت سالبة بعد شرائه للكوبون {copon}")
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
        
        data = json.loads(request.body)
        verfie_code = data.get('verfie-code')
    
        try:
            verfie_copon = ReceiveCopon.objects.get(code=verfie_code)

            if verfie_copon.is_used:
                logger.info(f"User {user} tried to use an already used code: {verfie_code}")
                return JsonResponse({"success": False, "message": "الكود الذي ادخلته مستخدم بالفعل"})

            # إنشاء CoponItem جديد
            copon_item = CoponItem.objects.create(
                user=user,
                copon_code=verfie_copon.copon,   
                receive_from_code=True, 
            )

            verfie_copon.copon.sales_count += 1 
            copon_item.buy_copon()
            copon_item.sell_price = 0 # عند الحصول على الكوبون من كود فإن سعر شراءه صفر 
            verfie_copon.copon.save()
            copon_item.save()
            
            # تحديث حالة الكود إلى "مستخدم"
            verfie_copon.is_used = True
            verfie_copon.used_by = user
            verfie_copon.save()
            
            # ارسال رسالة عند اتمام استلام الكوبون
            message = receive_copon_done_message(user_name=request.user.first_name, copon_name=verfie_copon.copon)
            request.user.inbox.add_message(message)
            logger.info(f"User {user.username} successfully received the coupon: {verfie_copon.copon.name}")
            return JsonResponse({"success": True, "message": 'تهانينا! تم استلام الكوبون بنجاح.'})

        except ReceiveCopon.DoesNotExist:
            logger.warning(f"المستخدم {user}يحاول ادخال كود استلام كوبون غير موجود وهو:{verfie_code}")
            return JsonResponse({"success": False, "message": "الكود غير صحيح."})
        except Exception as e:
            logger.error(f"خطأ بدالة استرداد كوبون من الرمز الخاص به: {e}", exc_info=True)
            return JsonResponse({'success': False, 'error': 'حدث خطأ غير متوقع، الرجاء المحاولة لاحقًا'})

    logger.warning(f"المستخدم {user} وصل الى دالة verfie_code بطريقة خاطئة.")
    return JsonResponse({"success": False, "message": "طريقة وصول خاطئة"})

# ===================================================