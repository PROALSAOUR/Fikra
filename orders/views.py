from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
import json
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from orders.models import *
from cards.models import GiftItem, CoponUsage
from store.models import Cart
from django.utils import timezone

# دالة عرض الطلبات
@login_required
def my_orders(request):
    
    user  = request.user
    orders = Order.objects.filter(user=user).order_by('-order_date', '-updated_at').prefetch_related('order_items')
    
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
            
            order = Order.objects.get(id=order_id, user=user)
            
            if order.status == 'canceled':
                return JsonResponse({'success': False, 'error': ' نعتذر, هذا الطلب تم إلغاؤه مسبقا لذالك لايمكن تعديله'}) 
            elif order.status == 'delivered':
                return JsonResponse({'success': False, 'error': "نعتذر, لا يمكن إلغاء منتج من طلب تم تسليمه بالفعل"}) 
            elif order.status == 'shipped':
                return JsonResponse({'success': False, 'error': "المعذرة لكن هذا الطلب تم شحنه اليك بالفعل اذا اردت إلغائه عليك التواصل مع خدمة العملاء"}) 
            else:
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
        if replace_item_id and selected_new_item and order_id :
            
            try:
                #  تحقق من حالة الطلب
                order = Order.objects.get(id=order_id, user=user)
                if order.status == 'canceled':
                    return JsonResponse({'success': False, 'error': "نعتذر. لايمكن تعديل الطلبات التي تم إلغائها"})
                if order.status == 'delivered' and order.deliverey_date: # لو مضى اكثر من 3 ايام على تاريخ التسليم
                    # احسب الفرق بين التاريخ الحالي وتاريخ التسليم
                    days_since_delivery = (timezone.now() - order.deliverey_date).days
                    # تحقق مما إذا كانت المدة أكبر من 3 أيام
                    if days_since_delivery > 3:
                        return JsonResponse({'success': False, 'error': "نعتذر. اقصى مدة لإستبدال المنتجات هي بعد تاريخ التسليم بثلاثة ايام "})
               
                
                try:                        
                    item =  order.order_items.get(id=replace_item_id) # الحصول على عنصر السلة المراد استبداله
                    cart = Cart.objects.get(user=user)
                    new_item = cart.items\
                    .prefetch_related('cart_item__product_item__variations__size')\
                    .select_related('cart_item__product_item').get(id=selected_new_item) # الحصول على عنصر السلة الجديد 
                    
                    parent_product = new_item.cart_item.product_item.product
                    
                    if new_item.cart_item.stock <= 0: #  تحقق من المنتج  الجديد هل متاح
                        return JsonResponse({'success': False, 'error': 'المنتج المستبدل غير متاح حاليا'})
                    else:
                        # ازالة بيانات القديم من الطلب
                        order.old_total -= item.price * item.qty
                        order.total_price = order.old_total + order.dlivery_price - order.discount_amount
                        order.total_points -= item.points * item.qty
                        
                        # استبدال بيانات القديم بالجديد
                        item.order_item = new_item.cart_item
                        item.qty = new_item.qty
                        item.price = parent_product.get_price()
                        item.points = parent_product.bonus
                        
                        item.save()
                        
                        # تحديث بيانات الطلب وفقا  للجديد
                        order.old_total += item.price * item.qty
                        order.total_price = order.old_total + order.dlivery_price - order.discount_amount
                        order.total_points += item.points * item.qty
                        
                        order.save() # تعديل الاجمالي للطلب
                        
                        # إذا كانت العملية ناجحة:
                        return JsonResponse({'success': True, 'message': 'تم استبدال المنتج بنجاح'})
                                        
                except :
                    return JsonResponse({'success': False, 'error': 'المنتج المستبدل غير موجود'  })             
            except :
                return JsonResponse({'success': False, 'error': 'الطلب الذي تحاول تعديله غير صالح' }) 
        else:
            # إذا كانت البيانات مفقودة أو غير صالحة:
            return JsonResponse({'success': False, 'error': 'نعتذر يبدو انه هنالك بيانات ناقصة'})

    # إذا كان الطلب ليس POST:
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



