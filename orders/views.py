from django.http import JsonResponse
from django.db.utils import IntegrityError
from django.shortcuts import render, get_object_or_404
import json
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from orders.models import *
from cards.models import CoponItem
from settings.models import Settings
from store.models import Cart
from accounts.models import UserProfile
from django.utils import timezone
from accounts.send_messages import create_order_message, cancel_order_message, edit_order_message, return_order_item_message
import logging

logger = logging.getLogger(__name__)  # تسجيل الأخطاء في اللوج


# دالة عرض الطلبات
@login_required
def my_orders(request):
    
    user  = request.user
    orders = Order.objects.filter(user=user).order_by('-order_date', '-updated_at').prefetch_related('order_items')[:25]
    
    context = {
        'orders':orders,
    }
    
    return render(request, 'orders/my-orders.html', context)
# دالة عرض تفاصيل الطلب
@login_required
def order_details(request, oid):
    user  = request.user
    order = get_object_or_404(Order, pk=oid , user=user)
    items = order.order_items.prefetch_related('order_item__product_item__product')
    
    try: # هل يوجد عمليات استبدال او استرجاع تابعة للطلب؟
        order_dealing = OrderDealing.objects.get(order=order)      
    except OrderDealing.DoesNotExist:
        order_dealing = None
    except Exception as e:
        logger.error(f"خطأ بالطلب: {e}", exc_info=True)
        order_dealing = None
    
    replace_possibility = Settings.objects.values_list('replace_possibility', flat=True).first()
    return_possibility = Settings.objects.values_list("return_possibility", flat=True).first()
    
    # إضافة حقل السعر الإجمالي لكل عنصر
    for item in items:
        item.total_price = item.qty * item.price
    
    
    # الحصول على المنتجات في السلة لعرضها بقائمة الاستبدال
    available_items = []
    if order.status != 'canceled':
        try:
            cart = Cart.objects.get(user=user)
            cart_items = cart.items.prefetch_related('cart_item__product_item__variations').select_related('cart_item__product_item__product')

            for item in cart_items:
                product_variation = item.cart_item
                stock = product_variation.stock if product_variation else 0

                if stock > 0:
                    available_items.append({
                        'id': item.id,
                        'product_variation': product_variation,
                        'cart_item': item,
                        'qty': item.qty,
                    })
                
        except Exception as e:
            logger.error(f"خطأ بالطلب: {e}", exc_info=True)
            available_items = None    
    

    context = {
        'order':order,
        'items':items,
        'available_items':available_items,
        'order_dealing':order_dealing,
        'replace_possibility':replace_possibility,
        'return_possibility':return_possibility,
    }
    
    return render(request, 'orders/order-details.html', context)   
# دالة الغاء الطلب
@login_required
def cancel_order(request):  
    user = request.user
    if request.method == 'POST':
        try:
            # فك تشفير البيانات من الطلب
            data = json.loads(request.body)
            order_id = data.get('order_id')  # الحصول على معرف الطلب من JSON
            
            # البحث عن الطلب وإلغاؤه
            order = Order.objects.get(id=order_id)
            if order.user != user:
                logger.error(f"المستخدم {user}يحاول الغاء طلب ليس له ", exc_info=True)
                return JsonResponse({'success': False, 'error': 'هذا الطلب ليس لك.'})
            else:
                if order.status == 'canceled' :
                    return JsonResponse({'success': False, 'error': 'هذا الطلب تم إلغائه مسبقا بالفعل'})
                # سوف يتم اقفال امكانية تعديل الطلب مؤقتا عندما يكون جاري شحنه
                elif order.status == 'shipped':
                    return JsonResponse({'success': False, 'error': "نعتذر لا يمكن إلغاء الطلب من الموقع بعد قيامنا بشحنه إليك، اذا كنت مصراً على إلغاء الطلب رجاءً قم بالتواصل مع خدمة الدعم"})
                elif order.status == 'delivered' :
                    return JsonResponse({'success': False, 'error': 'هذا الطلب تم تسليمه اليك بالفعل ولا يمكن إلغائه الأن'})
                else:
                    
                    # إعادة الكمية إلى المخزون
                    for item in order.order_items.all():
                        product_variant = item.order_item
                        product_variant.update_stock(item.qty)  # زيادة المخزون بناءً على الكمية
                        product_variant.sold -= item.qty  # انقاص الكمية المباعة بناءً على الكمية
                        product_variant.save()
                        
                    order.status = 'canceled'
                    order.save()
                    # ارسال رسالة بعد إلغاء الطلب
                    message = cancel_order_message(user_name=user.first_name, order=order.serial_number)
                    inbox = user.profile.inbox
                    inbox.add_message(message)
                    inbox.save()
                    
                    return JsonResponse({'success': True, 'message': 'تمت عملية إلغاء الطلب بنجاح!'})
            
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'لم يتم ايجاد الطلب.'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'المعذرة يبدو انه هنالك بيانات ناقصة يرجى المحاولة لاحقا.'})
        except Exception as e:
            logger.error(f"خطأ بإلغاء الطلب: {e}", exc_info=True)
            return JsonResponse({'success': False, 'error': 'حدث خطأ غير متوقع، الرجاء المحاولة لاحقًا'})
    
    return JsonResponse({'success': False, 'error': 'طريقة طلب خاطئة.'})
# دالة حذف منتج من الطلب
@login_required
def remove_order_item(request): 
    user = request.user
    if request.method == 'POST':    
        try:
            data = json.loads(request.body)
            order_id = data.get('order_id')
            remove_id = data.get('remove_id')
            
            if not remove_id or not order_id :
                return JsonResponse({'success': False, 'error': 'المعذرة يبدو انه هنالك بيانات ناقصة يرجى المحاولة لاحقا.'})
            
            # نستعمل الكاش هنا لمنع المستخدم من النقر المتتالي على زر التعديل وبالتالي منع امكانية التكرار
            lock_id = f"edit_order_lock_{user.id}_{order_id}"
            if cache.get(lock_id):
                return JsonResponse({'success': False, 'error': 'تم استلام طلب الإرجاع الخاص بك، يرجى الانتظار قبل المحاولة مجددًا'})
            cache.set(lock_id, True, timeout=3)  # وضع القفل
        
            # تحقق من حالة الطلب
            order = Order.objects.get(id=order_id, user=user)
            if order.status == 'canceled':
                return JsonResponse({'success': False, 'error': "نعتذر. لا يمكن تعديل الطلبات التي تم إلغاؤها"})
            # سوف يتم اقفال امكانية تعديل الطلب مؤقتا عندما يكون جاري شحنه
            if order.status == 'shipped':
                return JsonResponse({'success': False, 'error': "نعتذر لا يمكن تعديل الطلب أثناء قيامنا بشحنه إليك، رجاء قم بإعادة محاولة التعديل بعد استلامك للطلب"})
            if order.status == 'delivered' and order.deliverey_date:
                # احسب الفرق بين التاريخ الحالي وتاريخ التسليم
                days_since_delivery = (timezone.now() - order.deliverey_date).days
                # تحقق مما إذا كانت المدة أكبر من عدد أيام الاستبدال القصوى
                
                return_possibility = Settings.objects.values_list("return_possibility", flat=True).first()
                    
                if return_possibility == False: # لو المتجر مقفل عمليات الارجاع
                    return JsonResponse({'success': False, 'error': f"المعذرة، خدمات الإرجاع موقفة حالياً من قبل ادارة المتجر."})
                
                max_return_days = Settings.objects.values_list('max_return_days', flat=True).first()
                if max_return_days is None:
                    max_return_days = 3  # ثلاث أيام كقيمة افتراضية
                
                if days_since_delivery > max_return_days:
                    return JsonResponse({'success': False, 'error': F"نعتذر , يبدو انك قد تجاوزت اقصى مدة مسموحة للإرجاع و هي {max_return_days}"})
                
            
            order_item = order.order_items.get(id=remove_id)
            old_qty = order_item.qty
            old_bounce = order_item.points
            old_discount_price =  order_item.discount_price 
            
            order_item.delete()
            
            product_variant = order_item.order_item 
            
            # =================================================================
            # تعديل النقاط إذا كان الطلب قد تم تسليمه بالفعل
            if order.status == 'delivered':
                profile = UserProfile.objects.get(user=user)
                points_change = old_bounce * old_qty
                profile.points -= points_change  # تعديل النقاط بناءً على الطلب المعدل
                profile.save()
            # =================================================================   
            # اعد حساب جميع القيم
            order.old_total = order.order_items.aggregate(total=models.Sum(models.F('price') * models.F('qty')))['total'] or 0
            order.total_price = order.order_items.aggregate(total=models.Sum(models.F('discount_price')))['total'] or 0
            order.used_discount = order.old_total - order.total_price
            order.save()
            # =================================================================
            price_difference = 0 - old_discount_price
            # انشاء معاملة لإخبار الموظفين انه هنالك عملية استبدال منتجات حصلت
            dealing, created = OrderDealing.objects.get_or_create(order=order)
            DealingItem.objects.create(
                order_dealing= dealing,
                old_item = product_variant,
                old_qty = old_qty,
                old_price = old_discount_price, # السعر المخفض القديم
                status = 'return',
                # يتم وضع قيمة لفارق السعر فقط ان كان الطلب مسلما
                price_difference = price_difference if order.status=='delivered' else 0,
            )
            dealing.save()
            # =================================================================
                                         
            #  ارسال رسالة الى المستخدم عند ارجاع منتج من الطلب
            message = return_order_item_message(user_name=user.first_name, order=order.serial_number)
            inbox = user.profile.inbox
            inbox.add_message(message)
            inbox.save()            
                
            # تعديل حالة الطلب الى ملغي ان لم يتبقى عناصر داخله 
            #  يعمل فقط اذا كانت حالة الطلب جاري المعالجة او التجهيز 
            # ان كانت الحالة مسلم  يتم التعامل منها عبر السيجنال وليس من هنا
            if not order.order_items.exists() and (order.status == 'pending' or order.status == 'checking' ):
                order.status = 'canceled'
                order.save()

            return JsonResponse({'success': True, 'message':'تمت ازالة المنتج من الطلب بنجاح' })
                  
        except OrderItem.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'العنصر المطلوب غير موجود'})
        except Exception as e:
            logger.error(f"خطأ عند ارجاع عنصر من الطلب: {e}", exc_info=True)
            return JsonResponse({'success': False, 'error': 'حدث خطأ غير متوقع، الرجاء المحاولة لاحقًا'})
        finally:
                try:
                    cache.delete(lock_id)
                except Exception as e:
                    logger.warning(f"فشل في حذف القفل من الكاش: {e}", exc_info=True)  # إزالة القفل بعد الانتهاء سواء نجحت العملية أم لا
    # إذا كان الطلب ليس POST
    return JsonResponse({'success': False, 'error': 'طريقة وصول خاطئة'})
# دالة تعديل الطلب
@login_required
def edit_order(request):

    user = request.user
    if request.method == 'POST':
        # الحصول على البيانات المرسلة من الفورم
        order_id = request.POST.get('order_id')
        replace_item_id = request.POST.get('replace_product_id')
        selected_new_item = request.POST.get('selected_product_id')
        
        # تأكد من أن البيانات موجودة
        if replace_item_id and selected_new_item and order_id:
            
            # نستعمل الكاش هنا لمنع المستخدم من النقر المتتالي على زر التعديل وبالتالي منع امكانية التكرار
            lock_id = f"edit_order_lock_{user.id}_{order_id}"
            if cache.get(lock_id):
                return JsonResponse({'success': False, 'error': 'تم استلام طلب التعديل الخاص بك، يرجى الانتظار قبل المحاولة مجددًا'})
            cache.set(lock_id, True, timeout=3)  # وضع القفل

            try:
                # تحقق من حالة الطلب
                order = Order.objects.get(id=order_id, user=user)
                if order.status == 'canceled':
                    return JsonResponse({'success': False, 'error': "نعتذر. لا يمكن تعديل الطلبات التي تم إلغاؤها"})
                # سوف يتم اقفال امكانية تعديل الطلب مؤقتا عندما يكون جاري شحنه
                if order.status == 'shipped':
                    return JsonResponse({'success': False, 'error': "نعتذر لا يمكن تعديل الطلب أثناء شحنه إليك، رجاء قم بإعادة محاولة التعديل بعد استلام الطلب"})
                if order.status == 'delivered' and order.deliverey_date:
                    # احسب الفرق بين التاريخ الحالي وتاريخ التسليم
                    days_since_delivery = (timezone.now() - order.deliverey_date).days
                    # تحقق مما إذا كانت المدة أكبر من عدد أيام الاستبدال القصوى
                    
                    replace_possibility = Settings.objects.values_list("replace_possibility", flat=True).first()
                    
                    if replace_possibility == False: # لو المتجر مقفل عمليات الاستبدال
                        return JsonResponse({'success': False, 'error': f"المعذرة، خدمات الاستبدال موقفة حالياً من قبل ادارة المتجر."})

                    max_replace_days = Settings.objects.values_list('max_replace_days', flat=True).first()
                    if max_replace_days is None:
                        max_replace_days = 3  # ثلاث أيام كقيمة افتراضية
                    
                    if days_since_delivery > max_replace_days:
                        return JsonResponse({'success': False, 'error': f"نعتذر , يبدو انك قد تجاوزت اقصى مدة مسموحة للإستبدال و هي {max_replace_days}"})
                    
                try:
                    # الحصول على عنصر الطلب المراد استبداله
                    item = order.order_items.get(id=replace_item_id)
                    
                    # منع استبدال منتج مستبدل بالفعل
                    if item.status == 'replaced': # إذا كان قد تم استبداله بالفعل
                        logger.error(f"المستخدم  {user} يحاول تعديل عنصر طلب معدل سابقا", exc_info=True)
                        return JsonResponse({'success': False, 'error': "لقد قمت بإستبدال هذا المنتج سابقا"})
                    
                    cart = Cart.objects.get(user=user)
                    # الحصول على عنصر السلة الجديد
                    new_item = cart.items.prefetch_related('cart_item__product_item__variations__size')\
                        .select_related('cart_item__product_item').get(id=selected_new_item)
                    
                    old_variation = item.order_item  # متغير المنتج القديم
                    new_variation = new_item.cart_item  # متغير المنتج الجديد
                    # تخزين الكميتين كي يتم استعمالهم مع المخزون و المباع
                    old_qty = item.qty # الكمية القديمة
                    new_qty = new_item.qty # الكمية الجديدة
                    old_price = item.price 
                    old_discount_price = item.discount_price # سعر المنتج القديم المخفض
                    old_discount_value = round(old_qty * old_price ) - item.discount_price # قيمة الخصم على المنتج المستبدل
                    new_price = new_item.cart_item.product_item.product.get_price()
                    old_order_points = order.total_points # يستعمل لاحقا عند التعديل على نقاط المستخدم
                    
                    if new_item.cart_item.stock <= 0:  # تحقق من توفر المنتج الجديد
                        return JsonResponse({'success': False, 'error': 'المنتج المستبدل غير متاح حاليا'})
                    
                    # =================================================================
                    # استبدال العنصر القديم بالجديد
                    item.order_item = new_item.cart_item
                    item.qty = new_item.qty
                    item.price = new_price
                    # قيمة الخصم الجديدة نفس قيمة الخصم القديمة بشرط ان قيمة الخصم القديمة ليست اكبر من اجمالي المنتج الجديد
                    new_discount_value = old_discount_value if old_discount_value < (item.qty*item.price) else (item.qty*item.price)
                    item.discount_price = (item.qty*item.price) - new_discount_value
                    new_discount_price = item.discount_price # سعر المنتج الجديد المخفض
                    item.points = new_item.cart_item.product_item.product.bonus
                    item.status = 'replaced'
                    item.save()
                    new_item.delete()
                    # =================================================================
                    # تحديث إجمالي نقاط الطلب 
                    order.total_points = order.order_items.aggregate(total=models.Sum(models.F('points') * models.F('qty')))['total'] or 0
                    # تعديل النقاط إذا كان الطلب قد تم تسليمه بالفعل
                    if order.status == 'delivered':
                        profile = UserProfile.objects.get(user=user)
                        points_change = order.total_points - old_order_points # ايجاد فارق النقاط بين الطلب قبل التعديل وبعد التعديل
                        profile.points += points_change  # تعديل النقاط بناءً على الطلب المعدل
                        profile.save()
                    # =================================================================   
                    # اعد حساب جميع القيم
                    order.old_total = order.order_items.aggregate(total=models.Sum(models.F('price') * models.F('qty')))['total'] or 0
                    order.total_price = order.order_items.aggregate(total=models.Sum(models.F('discount_price')))['total'] or 0
                    order.used_discount = order.old_total - order.total_price
                    order.save()
                    # =================================================================
                    price_difference = new_discount_price - old_discount_price
                    # انشاء معاملة لإخبار الموظفين انه هنالك عملية استبدال منتجات حصلت
                    dealing, created = OrderDealing.objects.get_or_create(order=order)
                    try:
                        DealingItem.objects.create(
                            order_dealing= dealing,
                            old_item = old_variation,
                            new_item = new_variation,
                            old_qty = old_qty,
                            new_qty = new_qty,
                            old_price = old_discount_price, # السعر المخفض القديم
                            new_price = new_discount_price, # السعر المخفض الجديد
                            status = 'replace',
                            # يتم وضع قيمة لفارق السعر فقط ان كان الطلب مسلما
                            price_difference = price_difference if order.status=='delivered' else 0,
                        )
                    except IntegrityError:
                        logger.error(f"المستخدم {user} تم انشاء معاملتين تعديل لنفس العنصر ", exc_info=True)
                        return JsonResponse({'success': False, 'error': 'لقد قمت بالفعل بتسجيل هذه المعاملة سابقًا'})
                    except Exception as e:
                        logger.error(f"خطأ أثناء تعديل الطلب: تحديدا عند انشاء عنصر معالجة {e}", exc_info=True)
                        return JsonResponse({'success': False, 'error': 'حدث خطأ غير متوقع، الرجاء المحاولة لاحقًا'})
                    
                    dealing.save()
                    
                    # =================================================================
                    #  ارسال رسالة الى المستخدم عند تعديل الطلب
                    message = edit_order_message(user_name=user.first_name, order=order.serial_number)
                    inbox = user.profile.inbox
                    inbox.add_message(message)
                    inbox.save() 
                            
                    return JsonResponse({'success': True, 'message': 'تم تعديل المنتج بنجاح'})

                except OrderItem.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'المنتج المستبدل غير موجود'})
                except Exception as e:
                    logger.error(f"خطأ أثناء تعديل الطلب: {e}", exc_info=True)
                    return JsonResponse({'success': False, 'error': 'حدث خطأ غير متوقع، الرجاء المحاولة لاحقًا'})
            except Order.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'الطلب الذي تحاول تعديله غير صالح'})
            finally:
                try:
                    cache.delete(lock_id)
                except Exception as e:
                    logger.warning(f"فشل في حذف القفل من الكاش: {e}", exc_info=True)  # إزالة القفل بعد الانتهاء سواء نجحت العملية أم لا
        else:
            # إذا كانت البيانات مفقودة أو غير صالحة
            return JsonResponse({'success': False, 'error': 'نعتذر، يبدو أن هناك بيانات ناقصة'})

    # إذا كان الطلب ليس POST
    return JsonResponse({'success': False, 'error': 'طريقة وصول خاطئة'})
# دالة انشاء طلب من صفحة السلة
@login_required
def create_order(request):
    user = request.user
    if request.method == 'POST':
        card_id = request.POST.get('card-id')
        use_this = request.POST.get('use-this')
        
        copon_value = 0
        old_total = 0
        total_price = 0
        total_bonus = 0
        available_items = []

        try:
            cart = Cart.objects.get(user=user)
            cart_items = cart.items.prefetch_related('cart_item__product_item__variations').select_related('cart_item__product_item__product')

            for item in cart_items:
                product_variation = item.cart_item
                stock = product_variation.stock if product_variation else 0

                if stock > 0:
                    available_items.append({
                        'product_variation': product_variation,
                        'cart_item': item,
                        'qty': item.qty,
                        'points': product_variation.product_item.product.bonus
                    })
                    old_total += product_variation.product_item.product.get_price() * item.qty
                    total_bonus += product_variation.product_item.product.bonus * item.qty

            if not available_items:
                return JsonResponse({'success': False, 'error': 'نفذت الكمية الخاصة بجميع المنتجات التي طلبتها'})

        except Cart.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'يبدو ان سلتك فارغة ، يرجى ملؤها اولاً'})
        except Exception as e:
            logger.error(f"خطأ أثناء انشاء طلب: {e}", exc_info=True)
            return JsonResponse({'success': False, 'error': 'حدث خطأ غير متوقع، الرجاء المحاولة لاحقًا'})


        # Check if user wants to use discount
        if use_this :
            try:
                copon = CoponItem.objects.get(id=card_id, user=user, has_used=False)
                if copon.is_expire():
                    return JsonResponse({'success': False, 'error': 'الكوبون الذي ادخلته منتهي الصلاحية'})
                else:
                    copon.has_used = True
                    copon_value = copon.copon_code.value
                    used_discount = copon_value if not copon_value > total_price else old_total
                    
            except CoponItem.DoesNotExist:
                logger.error(f"المستخدم  {user} يحاول استعمال كوبون خصم غير موجود لديه مع طلبه", exc_info=True)
                return JsonResponse({'success': False, 'error': 'كود الكوبون الذي ادخلته غير موجود في مخزونك!'})
            except Exception as e:
                logger.error(f"خطأ أثناء انشاء طلب تحديدا عند جزئية كوبون الخصم: {e}", exc_info=True)
                return JsonResponse({'success': False, 'error': 'حدث خطأ غير متوقع، الرجاء المحاولة لاحقًا'})
        else:
            used_discount = 0 # عند عدم استعمال خصم فإن قيمة الخصم المستعمل تساوي صفر

        # ========  الاستعلام عما ان كان التوصيل مجاني ==========
        
        settings =  Settings.get_settings()
        delivery = settings.free_delivery
        city = user.profile.city.name if user.profile.city  else 'غير محددة'
        
        # إنشاء الطلب
        order = Order.objects.create(
            user=user,
            old_total=old_total,
            total_price=total_price,
            total_points=total_bonus,
            copon_value=copon_value,
            free_delivery = delivery,
            city=city,
        )
        
        # إنشاء عناصر الطلب
        for item in available_items:
            item_price =  item['product_variation'].product_item.product.get_price()
            item_qty = item['qty']
            if use_this:
                discount_value = round((item_price * item_qty / order.old_total) * used_discount ) # قيمة الخصم على المنتج من قيمة الكوبون الاجمالية
                discount_price = (item_price * item_qty) - discount_value
            else:
                # لايوجد كوبون مستعمل لذا سعر القطعة بعد الخصم نفس السعر الاصلي
                discount_price = item_price * item_qty
                
            order.total_price += discount_price # قيمة الطلب النهائية تساوي مجموع اسعار المنتجات بعد التخفيض ان وجد
                            
            OrderItem.objects.create(
                order=order,
                order_item=item['product_variation'],
                qty=item['qty'],
                points = item['points'],
                price=item['product_variation'].product_item.product.get_price(),
                discount_price = discount_price,
            )
            item['product_variation'].sell(item['qty'])
            
        order.used_discount = used_discount 
        order.save()

        # ارسال رسالة عند اتمام الطلب 
        message = create_order_message(user_name=user.first_name, order=order.serial_number)
        inbox = user.profile.inbox
        inbox.add_message(message)
        inbox.save()
        
        # إفراغ السلة عند نجاح الطلب
        cart.delete()

        # حفظ التغييرات على الهدايا والكوبونات
        if use_this:
            copon.save()
            
        return JsonResponse({'success': True, 'message': 'تمت عملية الطلب بنجاح!'})
    return JsonResponse({'success': False, 'error': 'طلب غير صالح'})
# دالة عرض عناصر طلبات الاستبدال والاسترجاع
@login_required
def order_dealing(request, oid):
    order = get_object_or_404(Order, id=oid)
    context = {
        'serial_number': order.serial_number,
    }
    
    if request.user == order.user:
        try:
            order_dealing = OrderDealing.objects.get(order=order)
            
        except OrderDealing.DoesNotExist:
            order_dealing = None
        except Exception as e:
            logger.error(f"خطأ  داخل دالة عرض طلبات التعديل والارجاع: {e}", exc_info=True)
            order_dealing = None   
        
        if order_dealing:
            dealing_items = order_dealing.deals.prefetch_related(
                'order_dealing__order__user', 
                'old_item__product_item', 
                'new_item__product_item'
            ).order_by('is_dealt', 'created_at')
            
            remaining = order_dealing.remaining
            # تحديد ما إذا كانت القيمة المتبقية لك أو عليك بناءً على علامة القيمة
            if remaining > 0:
                remaining_label = "عليك"
            elif remaining < 0:
                remaining_label = "لك"
            else: # remaining = 0
                remaining_label = "لا يوجد"
                
            remaining = abs(remaining)  # تحويل القيمة إلى موجبة
                
            context.update({
                'order_dealing': order_dealing,
                'dealing_items': dealing_items,
                'remaining': remaining,
                'remaining_label': remaining_label,
            })
    
    return render(request, 'orders/dealing-items.html', context)