from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
import json
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from orders.models import *
from cards.models import GiftItem, CoponUsage
from settings.models import Settings
from store.models import Cart
from accounts.models import UserProfile
from django.utils import timezone
from accounts.send_messages import create_order_message, cancel_order_message, edit_order_message, return_order_item_message


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
                
        except Exception:
            available_items = None    
    
    context = {
        'order':order,
        'items':items,
        'available_items':available_items,
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
                return JsonResponse({'success': False, 'error': 'هذا الطلب ليس لك.'})
            else:
                if order.status == 'canceled' :
                    return JsonResponse({'success': False, 'error': 'هذا الطلب تم إلغائه مسبقا بالفعل'})
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
                    inbox.messages.add(message)
                    inbox.save()
                    
                    return JsonResponse({'success': True, 'message': 'تمت عملية إلغاء الطلب بنجاح!'})
            
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'لم يتم ايجاد الطلب.'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'المعذرة يبدو انه هنالك بيانات ناقصة يرجى المحاولة لاحقا.'})
    
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
            
            # تحقق من حالة الطلب
            order = Order.objects.get(id=order_id, user=user)
            if order.status == 'canceled':
                return JsonResponse({'success': False, 'error': "نعتذر. لا يمكن تعديل الطلبات التي تم إلغاؤها"})
            if order.status == 'delivered' and order.deliverey_date:
                # احسب الفرق بين التاريخ الحالي وتاريخ التسليم
                days_since_delivery = (timezone.now() - order.deliverey_date).days
                # تحقق مما إذا كانت المدة أكبر من عدد أيام الاستبدال القصوى
                
                max_replace_days = Settings.objects.values_list('max_return_days', flat=True).first()

                if max_replace_days is None:
                    max_replace_days = 3  # ثلاث أيام كقيمة افتراضية
                
                if days_since_delivery > max_replace_days:
                    return JsonResponse({'success': False, 'error': F"نعتذر , يبدو انك قد تجاوزت اقصى مدة مسموحة للإرجاع و هي {max_replace_days}"})
                
            
            order_item = order.order_items.get(id=remove_id)
            order_item.delete()
            
            product_variant = order_item.order_item 
            product_variant.update_stock(order_item.qty)  # زيادة المخزون بناءً على الكمية
            product_variant.sold -= order_item.qty  # انقاص الكمية المباعة بناءً على الكمية
            product_variant.save()
                
            # التحقق من عدد العناصر المتبقية في الطلب
            if not order.order_items.exists():  # إذا لم يكن هناك أي عناصر متبقية
                order.status = 'canceled'
            else:     
                # تجديد بيانات الطلب بعد حذف المنتج  
                order.old_total -= order_item.price * order_item.qty
                order.total_price = order.old_total + order.dlivery_price - order.discount_amount
                order.total_points -= order_item.points * order_item.qty
            order.save()  
            
            # انشاء معاملة فقط ان لم تكن حالة الطلب  جاري المعالجة
            if order.status != 'pending' :      
                # انشاء معاملة لإخبار الموظفين انه هنالك عملية إلغاء منتجات حصلت
                dealing, created = OrderDealing.objects.get_or_create(order=order)
                DealingItem.objects.create(
                    order_dealing= dealing,
                    old_item = product_variant,
                    status = 'return',
                    price_difference = 0,
                )
                dealing.save()               
                #  ارسال رسالة الى المستخدم عند ارجاع منتج من الطلب
                message = return_order_item_message(user_name=user.first_name, order=order.serial_number)
                inbox = user.profile.inbox
                inbox.messages.add(message)
                inbox.save() 
                
            return JsonResponse({'success': True, 'message':'تمت ازالة المنتج من الطلب بنجاح' })
                  
        except OrderItem.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'العنصر المطلوب غير موجود'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
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
            try:
                # تحقق من حالة الطلب
                order = Order.objects.get(id=order_id, user=user)
                if order.status == 'canceled':
                    return JsonResponse({'success': False, 'error': "نعتذر. لا يمكن تعديل الطلبات التي تم إلغاؤها"})
                if order.status == 'delivered' and order.deliverey_date:
                    # احسب الفرق بين التاريخ الحالي وتاريخ التسليم
                    days_since_delivery = (timezone.now() - order.deliverey_date).days
                    # تحقق مما إذا كانت المدة أكبر من عدد أيام الاستبدال القصوى
                    
                    max_replace_days = Settings.objects.values_list('max_replace_days', flat=True).first()
                    if max_replace_days is None:
                        max_replace_days = 3  # ثلاث أيام كقيمة افتراضية
                    
                    if days_since_delivery > max_replace_days:
                        return JsonResponse({'success': False, 'error': f"نعتذر , يبدو انك قد تجاوزت اقصى مدة مسموحة للإستبدال و هي {max_replace_days}"})
               
                try:
                    # الحصول على عنصر الطلب المراد استبداله
                    item = order.order_items.get(id=replace_item_id)
                    cart = Cart.objects.get(user=user)
                    # الحصول على عنصر السلة الجديد
                    new_item = cart.items.prefetch_related('cart_item__product_item__variations__size')\
                        .select_related('cart_item__product_item').get(id=selected_new_item)
                    
                    old_variation = item.order_item  # متغير المنتج القديم
                    new_variation = new_item.cart_item  # متغير المنتج الجديد
                    # تخزين الكميتين كي يتم استعمالهم مع المخزون و المباع
                    old_qty = item.qty # الكمية القديمة
                    new_qty = new_item.qty # الكمية الجديدة
                    
                    
                    
                    if new_item.cart_item.stock <= 0:  # تحقق من توفر المنتج الجديد
                        return JsonResponse({'success': False, 'error': 'المنتج المستبدل غير متاح حاليا'})
                    
                    # التحقق مما إذا كان المنتج القديم والجديد مرتبطين بنفس متغير المنتج
                    if old_variation == new_variation:
                        # تحديث الكمية والسعر فقط دون حذف العنصر القديم
                        item.qty = new_item.qty
                        item.price = new_item.cart_item.product_item.product.get_price()  # تحديث السعر بناءً على المتغير الجديد
                        item.points = new_item.cart_item.product_item.product.bonus
                        item.status = 'replaced'
                        item.save()

                    else:
                        # التحقق مما إذا كان العنصر الجديد موجودًا بالفعل في الطلب
                        existing_order_item = order.order_items.filter(order_item=new_item.cart_item).first()
                        
                        if existing_order_item:
                            # دمج الكميات وتحديث السعر إذا كانت العناصر موجودة بالفعل في الطلب
                            existing_order_item.qty += new_item.qty
                            existing_order_item.price = new_item.cart_item.product_item.product.get_price()  # تحديث السعر بناءً على الكمية الجديدة
                            existing_order_item.points = new_item.cart_item.product_item.product.bonus
                            existing_order_item.status = 'replaced'
                            existing_order_item.save()

                            # إزالة العنصر القديم
                            item.delete()

                        else:
                            # استبدال العنصر القديم بالجديد
                            item.order_item = new_item.cart_item
                            item.qty = new_item.qty
                            item.price = new_item.cart_item.product_item.product.get_price()
                            item.points = new_item.cart_item.product_item.product.bonus
                            item.status = 'replaced'
                            item.save()

                    # تخزين السعر القديم للطلب قبل التعديل  لإستعماله في جلب الفارق بين المنتجين المعدلين
                    old_total =  order.total_price  
                        
                    # تحديث إجمالي الطلب
                    order.old_total = sum([i.price * i.qty for i in order.order_items.all()])
                    order.total_price = order.old_total + order.dlivery_price - order.discount_amount
                    order.total_points = sum([i.points * i.qty for i in order.order_items.all()])
                    
                    # التحقق من أن السعر الإجمالي لا يمكن أن يكون أقل من الصفر
                    if order.total_price < 0:
                        order.total_price = 0
                        
                    # تخزين السعر الجديد للطلب بعد التعديل  لإستعماله في جلب الفارق بين المنتجين المعدلين
                    new_total =  order.total_price
                    order.save()

                    # تعديل النقاط إذا كان الطلب قد تم تسليمه بالفعل
                    if order.status == 'delivered':
                        profile = UserProfile.objects.get(user=user)
                        profile.points = order.total_points  # تعديل النقاط بناءً على الطلب المعدل
                        profile.save()
                        
                    # تحديث المخزون والمبيعات للمنتجات القديمة والجديدة
                    old_variation.update_stock(old_qty)  # إعادة الكمية القديمة إلى المخزون
                    old_variation.sold -= old_qty # تحديث الكمية المباعة
                    old_variation.save()
                    new_variation.sell(new_qty)  # تحديث المبيعات
                        
                    # انشاء معاملة فقط ان لم تكن حالة الطلب  جاري المعالجة
                    if order.status != 'pending' :                     
                        # انشاء معاملة لإخبار الموظفين انه هنالك عملية استبدال منتجات حصلت
                        dealing, created = OrderDealing.objects.get_or_create(order=order)
                        DealingItem.objects.create(
                            order_dealing= dealing,
                            old_item = old_variation,
                            new_item = new_variation,
                            new_qty = item.qty,
                            status = 'replace',
                            price_difference = new_total - old_total,
                        )
                        dealing.save()  
                        #  ارسال رسالة الى المستخدم عند تعديل الطلب
                        message = edit_order_message(user_name=user.first_name, order=order.serial_number)
                        inbox = user.profile.inbox
                        inbox.messages.add(message)
                        inbox.save() 

                    return JsonResponse({'success': True, 'message': 'تم تعديل المنتج بنجاح'})

                except OrderItem.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'المنتج المستبدل غير موجود'})
            except Order.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'الطلب الذي تحاول تعديله غير صالح'})
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
        card_type = request.POST.get('card-type')
        card_id = request.POST.get('card-id')
        use_this = request.POST.get('use-this')
        
        discount_amount = 0
        total_price = 0
        total_bonus = 0
        available_items = []
        with_message = False
        message = 'لايوجد رسالة مرفقة'

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
                    total_price += product_variation.product_item.product.get_price() * item.qty
                    total_bonus += product_variation.product_item.product.bonus * item.qty

            if not available_items:
                return JsonResponse({'success': False, 'error': 'نفذت الكمية الخاصة بجميع المنتجات التي طلبتها'})

        except Cart.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'السلة غير موجودة!'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

        dlivery_price = 0  # قيمة التوصيل الافتراضية
        try:
            dlivery = DliveryPrice.objects.first()
            dlivery_price = dlivery.price if dlivery else 0
        except Exception:
            dlivery_price = 0

        # Check if user wants to use discount
        if use_this and card_type:
            if card_type == 'gift':
                try:
                    gift = GiftItem.objects.get(id=card_id, recipient=user, has_used=False)
                    gift.has_used = True
                    discount_amount = min(gift.sell_value, total_price)

                    if gift.has_recipient():  # تحقق مما إذا كان هناك مستلم
                        with_message = True
                        # تحقق من وجود المستلم ثم احصل على الرسالة
                        gift_recipient = gift.gift_recipients if hasattr(gift, 'gift_recipients') else None  # استخدم hasattr للتحقق من وجود gift_recipients
                        message = gift_recipient.message if gift_recipient else 'لا يوجد رسالة مرفقة'


                except GiftItem.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'كود الهدية الذي ادخلته غير موجود في مخزونك!'})

            elif card_type == 'copon':
                try:
                    copon = CoponUsage.objects.get(id=card_id, user=user, has_used=False)
                    if copon.is_expire():
                        return JsonResponse({'success': False, 'error': 'الكوبون الذي ادخلته منتهي الصلاحية'})
                    if copon.copon_code.min_bill_price > total_price:
                        return JsonResponse({'success': False, 'error': 'لايمكن استعمال الكوبون الذي ادخلته مع هذه الفاتورة'})
                    else:
                        copon.has_used = True
                        discount_percentage = Decimal(copon.copon_code.value) / Decimal(100)
                        discount_amount = total_price * discount_percentage

                except CoponUsage.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'كود الكوبون الذي ادخلته غير موجود في مخزونك!'})

        # إنشاء الطلب
        order = Order.objects.create(
            user=user,
            old_total=total_price,
            total_price=total_price - discount_amount + dlivery_price, 
            total_points=total_bonus,
            dlivery_price=dlivery_price,
            discount_amount=discount_amount,
            with_message=with_message,
            message=message,
        )
        
        # إنشاء عناصر الطلب
        for item in available_items:
            OrderItem.objects.create(
                order=order,
                order_item=item['product_variation'],
                qty=item['qty'],
                points = item['points'],
                price=item['product_variation'].product_item.product.get_price(),
            )
            item['product_variation'].sell(item['qty'])

        # ارسال رسالة عند اتمام الطلب 
        message = create_order_message(user_name=user.first_name, order=order.serial_number)
        inbox = user.profile.inbox
        inbox.messages.add(message)
        inbox.save()
        
        # إفراغ السلة عند نجاح الطلب
        cart.delete()

        # حفظ التغييرات على الهدايا والكوبونات
        if use_this and card_type == 'gift':
            gift.save()
        elif use_this and card_type == 'copon':
            copon.save()

        # منطق نجاح الطلب
        return JsonResponse({'success': True, 'message': 'تمت عملية الطلب بنجاح!'})

    return JsonResponse({'success': False, 'error': 'طلب غير صالح'})

