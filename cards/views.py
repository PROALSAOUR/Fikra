from cards.models import *
from store.models import *
from accounts.models import UserProfile, Message
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from itertools import chain
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import phonenumbers
from django.utils import timezone


# ===================================================
# مستودع البطاقات
def cards_repo(request):
    user = request.user
    
    user_copons = CoponUsage.objects.filter(user=user, has_used=False).prefetch_related('copon_code')
    
    active_copons =  user_copons.filter(expire__gte=now().date()).order_by('-purchase_date')
    expired_copons  = user_copons.filter(expire__lt=now().date()).order_by('-purchase_date')[:5]
    
    copons_count = active_copons.count() + expired_copons.count()
    
    # =================================================================
    
    from_self =  GiftItem.objects.filter(has_used=False , buyer=user, recipient=user).prefetch_related('gift').order_by('-purchase_date')
    from_frind =  GiftItem.objects.filter(has_used=False, recipient=user).exclude(buyer=user).prefetch_related('gift', 'gift_recipients').order_by('-purchase_date')
    for_frind = GiftItem.objects.filter(buyer=user).exclude(recipient=user).prefetch_related('gift', 'gift_recipients').order_by('-purchase_date')[:12]
    
    gifts_count = from_self.count() + from_frind.count() 
    
    # =================================================================

    context  = {
        'active_copons': active_copons,
        'expired_copons': expired_copons,
        'copons_count': copons_count,
        # ==========================
        'from_self': from_self,
        'from_frind': from_frind,
        'for_frind': for_frind,
        'gifts_count': gifts_count,
        # ==========================
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
       
    # التحقق من إذا كان المستخدم يملك الكوبون بالفعل
    user_copon, created = CoponUsage.objects.get_or_create(user=user, copon_code=copon)
    
    if not created:
        
        # لو مو مستعمل وله صلاحية وصلاحيته غير منتهية اكسر البيعة
        if not user_copon.has_used and user_copon.expire and user_copon.expire > now().date():
            return JsonResponse({'error': 'لديك هذا الكوبون في مخزونك بالفعل'}, status=400)
       
    
    # ارسال رسالة عند شراء كوبون
    message = Message(
        subject= f'تمت عملية شراء كوبون بنجاح',
        content= 
        f"""
        مرحبا {user_copon.user.first_name}
        لقد تمت عملية شراء الكوبون ({ user_copon.copon_code }) بنجاح يمكنك العثور عليه الأن داخل مخزونك واستعماله مع احد طلباتك القادمة ,
        في حال كان لديك اي استفسار يرجى التواصل مع خدمة العملاء وسوف يتم الرد عليك بأسرع وقت ممكن.
        """,
        timestamp=timezone.now()
    )
            
    message.save()
    inbox.messages.add(message)
    
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
# دالة شراء هدية من صفحة التفاصيل
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
            buy_for = data.get('buy_for') # قيمة الراديو العائد من الفورم 
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
                    # إذا لم يكن المستخدم موجودًا على فكرة 
                    
                    # انشاء كود استلام للهدية كي يتمكن المستخدم من استلام هديته بعد انشاء حساب على فكرة
                    receive = ReceiveGift.objects.create(
                        value = gift.value,
                        gift = gift,
                    )
                    
                    GiftDealing.objects.create(
                        sender=user, 
                        receiver_name=recipient_name,
                        receiver_phone=recipient_phone,
                        sell_price=gift.price,
                        sell_value=gift.value,
                        receive = receive,
                        message = message_content,
                    )
                    
                     # رسالة الى المشتري تخبره ان المستلم ليس لديه حساب على فكرة وانه سيتم التواصل معه
                    message = Message(
                        subject= f'تمت عملية شراء الهدية بنجاح',
                        content= 
                        f"""
                        مرحبا {user.first_name}
                        لقد تمت عملية شراء الهدية ({ gift }) بنجاح, يبدو ان  ({recipient_name}[{recipient_phone}]) غير مسجل في قاعدة البيانات الخاصة بمتجرنا لكن لاتقلق سوف يتواصل معه احد موظفينا لإيصال هديتك اليه,
                        في حال كان لديك اي استفسار يرجى التواصل مع خدمة العملاء وسوف يتم الرد عليك بأسرع وقت ممكن.
                        """,
                        timestamp=timezone.now()
                    )
                    
                    message.save()
                    profile.inbox.messages.add(message)
                    
                    profile.points -= gift.price
                    profile.save()
                    gift.sales_count += 1
                    gift.save()
                    
                    return JsonResponse({'success': 'تم إرسال إشعار خدمة العملاء , ستم التواصل مع المستلم قريبا لتسليمه هديته'}, status=200)

            # إنشاء كائن GiftItem
            gift_item = GiftItem.objects.create(
                gift=gift,
                buyer=user,
                sell_price=gift.price,
                sell_value=gift.value,
                recipient=recipient
            )

            # إنشاء كائن GiftRecipient
            GiftRecipient.objects.create(
                gift_item=gift_item,
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
                recipient = user  
                
                try: # هل المستلم لديه حساب على فكرة؟
                    recipient = User.objects.get(phone_number=recipient_phone)
                except User.DoesNotExist:
                    
                    # انشاء كود استلام للهدية كي يتمكن المستخدم من استلام هديته بعد انشاء حساب على فكرة
                    receive = ReceiveGift.objects.create(
                        value = gift.value,
                        gift = gift,
                    )
                    
                    # إذا لم يكن المستخدم موجودًا، قم بإنشاء سجل في GiftDealing
                    GiftDealing.objects.create(
                        sender=user, 
                        receiver_name=recipient_name,
                        receiver_phone=recipient_phone,
                        sell_price=gift.price,
                        sell_value=gift.value,
                        receive = receive,
                        message = message_content,
                    )
                    
                    # رسالة الى المشتري تخبره ان المستلم ليس لديه حساب على فكرة وانه سيتم التواصل معه
                    message = Message(
                        subject= f'تمت عملية شراء الهدية بنجاح',
                        content= 
                        f"""
                        مرحبا {user.first_name}
                        لقد تمت عملية شراء الهدية ({ gift }) بنجاح, يبدو ان  ({recipient_name}[{recipient_phone}]) غير مسجل في قاعدة البيانات الخاصة بمتجرنا لكن لاتقلق سوف يتواصل معه احد موظفينا لإيصال هديتك اليه,
                        في حال كان لديك اي استفسار يرجى التواصل مع خدمة العملاء وسوف يتم الرد عليك بأسرع وقت ممكن.
                        """,
                        timestamp=timezone.now()
                    )
            
                    message.save()
                    profile.inbox.messages.add(message)
                    
                    
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
                sell_value=gift.value,
                recipient=recipient
            )

            # إنشاء كائن GiftRecipient
            GiftRecipient.objects.create(
                gift_item=gift_item,
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
# دالة استلام هدية من الكود 
@login_required
def verfie_code(request):
    user = request.user

    if request.method == 'POST':        
        try:
            data = json.loads(request.body)
            verfie_code = data.get('verfie-code')
        
            try:
                verfie_gift = ReceiveGift.objects.get(code=verfie_code)
                dealing = verfie_gift.dealing.first()

                if verfie_gift.is_used:
                    return JsonResponse({"success": False, "message": "الكود الذي ادخلته مستخدم بالفعل"})

                # إنشاء GiftItem جديد
                gift_item = GiftItem.objects.create(
                    buyer=dealing.sender, # not user but how create the dealing
                    gift=verfie_gift.gift,
                    sell_price=0,
                    sell_value=verfie_gift.value,
                    recipient=user,
                )
                
                # إنشاء كائن GiftRecipient
                GiftRecipient.objects.create(
                    gift_item=gift_item,
                    recipient_name= user.first_name,
                    recipient_phone=user.phone_number,
                    message=dealing.message,
                )
                

                # تحديث حالة الكود إلى "مستخدم"
                verfie_gift.is_used = True
                verfie_gift.save()

                return JsonResponse({"success": True, "message": 'تهانينا! تم استلام كود الهدية بنجاح.'})

            except ReceiveGift.DoesNotExist:
                return JsonResponse({"success": False, "message": "كود الهدية غير صحيح أو غير موجود."})
            
        except ReceiveGift.DoesNotExist:
            return JsonResponse({"success": False, "message": 'نعتذر حصلت مشكلة اثناء معالجة البيانات!'})

    return JsonResponse({"success": False, "message": "حدث خطأ ما."})
# دالة تغيير حالة الهدية عند فتحها
@login_required
def change_seen_status(request, gid):
    
    try: 
        user = request.user
        gift_item = GiftItem.objects.get(id=gid)
        if gift_item.buyer != user and gift_item.recipient == user :
            gift_item.is_seen = True
            gift_item.save()  # احفظ التغييرات

        return JsonResponse({'status': 'success'})  # أرجع استجابة JSON
    except:
        return JsonResponse({'status': 'error'})  # أرجع استجابة JSON

# ===================================================