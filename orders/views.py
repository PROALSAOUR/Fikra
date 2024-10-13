from django.http import JsonResponse
from django.shortcuts import render
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from orders.models import *
from cards.models import GiftItem, CoponUsage
from store.models import Cart


# دالة عرض الطلبات



# دالة عرض تفاصيل الطلب


# دالة الغاء الطلب


# دالة تعديل الطلب



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

                    if gift.has_recipient():
                        with_message = True
                        message = gift.recipients.message

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



