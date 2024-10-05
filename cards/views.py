from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from itertools import chain
from datetime import timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from store.models import *
from accounts.models import UserProfile
import json
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import phonenumbers
from cards.models import *


# ===================================================

# مستودع البطاقات
def cards_repo(request):
    
    purchased_copons =  CoponUsage.objects.filter(user=request.user)
    
    context  = {
        # 'copons': copons,
    }
    return render(request, 'cards/cards-repo.html',context)

# صفحة متجر البطاقات
def cards_store(request):
    #  خاص بالهدايا
        
    gifts_list = Gift.objects.filter(is_active=True).only('name','value','img','price').order_by('-sales_count')
    
    paginator_all = Paginator(gifts_list, 20)  

    page_all = request.GET.get('page_all', 1)
    
    try:
        gifts = paginator_all.page(page_all)
    except PageNotAnInteger:
        gifts = paginator_all.page(1)
    except EmptyPage:
        gifts = paginator_all.page(paginator_all.num_pages)
    
    # =====================================================
    
    #  خاص بالكوبونات
    
    copons_list = Copon.objects.filter(is_active=True).only('name','value','img','min_bill_price','price', 'expiration_days').order_by('-sales_count')
        
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
    Copon.objects.filter(filters).distinct(),
    Gift.objects.filter(filters).distinct()
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
        'gifts': gifts,
        'copons': copons,
        'results':results,
        'results_count':results_count,
    }
    return render(request, 'cards/cards-store.html',context)
# صفحة تفاصيل الهدية
def gift_details(request, gid):

    gift = get_object_or_404(Gift, id=gid)
        
    context  = {
        'gift': gift,
    }
    return render(request, 'cards/gift-details.html', context)
# صفحة تفاصيل الكوبون
def copon_details(request, cid):
     
    copon = get_object_or_404(Copon, id=cid)
        
    context  = {
        'copon': copon,
    }
    return render(request, 'cards/copon-details.html', context)
# دالة شراء كوبون 
@login_required
def buy_copon(request, cid):
    """
    دالة للتحقق من الكوبون المراد شرائه
    """
    # الحصول على الكوبون والمستخدم
    copon = get_object_or_404(Copon, id=cid)
    user = request.user
    profile = get_object_or_404(UserProfile, user=user)
    
    points = profile.points
    
    # التحقق من أن المستخدم لديه نقاط كافية
    if copon.price > points:
        return JsonResponse({'error': 'لاتوجد نقاط كافية لإتمام عملية الشراء'}, status=400)
       
    # التحقق من إذا كان المستخدم يملك الكوبون بالفعل
    user_copon, created = CoponUsage.objects.get_or_create(user=user, copon_code=copon)
    
    if not created:
        
        # لو مو مستعمل وله صلاحية وصلاحيته غير منتهية اكسر البيعة
        if not user_copon.has_used and user_copon.expire and user_copon.expire > now().date():
            return JsonResponse({'error': 'لديك هذا الكوبون في مخزونك بالفعل'}, status=400)
       
        
    
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
# دالة شراء هدية
@login_required
def buy_gift(request, gid):
    gift = get_object_or_404(Gift, id=gid)
    user = request.user
    profile = get_object_or_404(UserProfile, user=user)
    
    if gift.price > profile.points:
        return JsonResponse({'error': 'لا توجد نقاط كافية لإتمام عملية الشراء'}, status=400)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            buy_for = data.get('buy_for')
            recipient = user  # افتراضياً المشتري هو المستلم
            
            if buy_for == 'for-me':
                recipient_name = user.username
                recipient_phone = user.phone_number
                message_content = ''
            elif buy_for == 'for-another':
                recipient_name = data.get('recipient_name')
                recipient_phone = data.get('recipient_phone')
                message_content = data.get('message_content')
                
                try:
                    # التحقق من صحة رقم الهاتف حسب البلد 
                    parsed_phone = phonenumbers.parse(recipient_phone, 'LY')
                    if not phonenumbers.is_valid_number(parsed_phone):
                        return JsonResponse({'error': "رقم الهاتف غير صالح."}, status=400)
                    
                except phonenumbers.NumberParseException:
                    return JsonResponse({'error': "يرجى إدخال رقم هاتف صحيح."}, status=400)

                try:
                    recipient = User.objects.get(phone_number=recipient_phone)
                except User.DoesNotExist:
                    # إذا لم يكن المستخدم موجودًا، قم بإنشاء سجل في GiftDealing
                    GiftDealing.objects.create(
                        sender=user, 
                        receiver_name=recipient_name,
                        receiver_phone=recipient_phone,
                    )
                    
                    profile.points -= gift.price
                    profile.save()
                    gift.sales_count += 1
                    gift.save()
                    
                    return JsonResponse({'success': 'تم إرسال إشعار خدمة العملاء.'}, status=200)

            # إنشاء كائن GiftItem
            gift_item = GiftItem.objects.create(
                gift=gift,
                buyer=user,
                sell_price=gift.price,
                recipient=recipient
            )

            # إنشاء كائن GiftRecipient
            GiftRecipient.objects.create(
                gift_item=gift_item,
                gift_for=buy_for,
                recipient_name=recipient_name,
                recipient_phone=recipient_phone,
                message=message_content,
            )

            # تحديث نقاط المستخدم وعدد مبيعات الهدية
            profile.points -= gift.price
            profile.save()
            gift.sales_count += 1
            gift.save()

            return JsonResponse({'success': 'تمت عملية الشراء بنجاح!'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'فشل في قراءة البيانات المرسلة.'}, status=400)
        except IntegrityError:
            return JsonResponse({'error': 'حدثت مشكلة في قاعدة البيانات.'}, status=500)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'المستلم غير موجود.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'طلب غير صحيح.'}, status=400)
# دالة شراء هدية من البطاقة الخارجية
@login_required
def buy_gift2(request, gid):
    gift = get_object_or_404(Gift, id=gid)
    user = request.user
    profile = get_object_or_404(UserProfile, user=user)
    
    if gift.price > profile.points:
        return JsonResponse({'error': 'لا توجد نقاط كافية لإتمام عملية الشراء'}, status=400)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            recipient_name = data.get('recipient_name')
            recipient_phone = data.get('recipient_phone')
            message_content = data.get('message_content')
            buy_for = 'for-me' # افتراضياً الهدية لل مستخدم
            recipient = user  # افتراضياً المشتري هو المستلم
            
            # التحقق من صحة رقم الهاتف حسب البلد 
            try:
                parsed_phone = phonenumbers.parse(recipient_phone, 'LY')
                if not phonenumbers.is_valid_number(parsed_phone):
                    return JsonResponse({'error': "رقم الهاتف غير صالح."}, status=400)
            
            except phonenumbers.NumberParseException:
                return JsonResponse({'error': "يرجى إدخال رقم هاتف صحيح."}, status=400)
            
            # تحقق ان كان المستخدم اشترى الكود لنفسه ام لا
            if user.phone_number != recipient_phone :
                buy_for = 'for-another' 
                recipient = user  
                
                try: # هل المستلم لديه حساب على فكرة؟
                    recipient = User.objects.get(phone_number=recipient_phone)
                except User.DoesNotExist:
                    # إذا لم يكن المستخدم موجودًا، قم بإنشاء سجل في GiftDealing
                    GiftDealing.objects.create(
                        sender=user, 
                        receiver_name=recipient_name,
                        receiver_phone=recipient_phone,
                    )
                    
                    profile.points -= gift.price
                    profile.save()
                    gift.sales_count += 1
                    gift.save()
                    
                    return JsonResponse({'success': 'تم إرسال إشعار خدمة العملاء.'}, status=200)
            
            
            # إنشاء كائن GiftItem
            gift_item = GiftItem.objects.create(
                gift=gift,
                buyer=user,
                sell_price=gift.price,
                recipient=recipient
            )

            # إنشاء كائن GiftRecipient
            GiftRecipient.objects.create(
                gift_item=gift_item,
                gift_for=buy_for,
                recipient_name=recipient_name,
                recipient_phone=recipient_phone,
                message=message_content,
            )

            # تحديث نقاط المستخدم وعدد مبيعات الهدية
            profile.points -= gift.price
            profile.save()
            gift.sales_count += 1
            gift.save()

            return JsonResponse({'success': 'تمت عملية الشراء بنجاح!'}, status=200)

        except json.JSONDecodeError:
                return JsonResponse({'error': 'فشل في قراءة البيانات المرسلة.'}, status=400)
        except IntegrityError:
                return JsonResponse({'error': 'حدثت مشكلة في قاعدة البيانات.'}, status=500)
        except ObjectDoesNotExist:
                return JsonResponse({'error': 'المستلم غير موجود.'}, status=404)
        except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'طلب غير صحيح.'}, status=400)

# ===================================================