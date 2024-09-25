from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from store.models import *


# الصفحة الرئيسية
def index(request):
    # جلب الإعلانات التي يتم عرضها
    ads = AdsSlider.objects.filter(show=True)
    
    # جلب العلامات التجارية المميزة
    brands = Brand.objects.filter(featured=True)
    
    #جلب اسم المستخدم الاول اذا كان مسجل دخول 
    user_name = request.user.first_name if request.user.is_authenticated else None
    
    # جلب الفئات المميزة والظاهرة فقط، وتحميل المنتجات التابعة لهذه الفئات
    categories = Category.objects.filter(
        featured=True,
        status='visible',
        gender_cat=False,
    ).prefetch_related(
        'products'
    ).filter(
        products__featured=True,
        products__ready_to_sale=True,
    ).distinct()[:8] # عدد اقسام المنتجات المطلوب عرضها بالصفحة الرئيسية
    
    offered_products = Product.objects.filter(offer=True)[:8]
    
    context = {
        'ads': ads,
        'brands': brands,
        'user_name': user_name,
        'categories': categories,
        'offered_products':offered_products,
    }
    
    return render(request, 'store/index.html', context)
# ===================================================
# صفحة الاعلان
def ads_page(request, slug):
    ad = get_object_or_404(AdsSlider, slug=slug)
    ad_content = AdsProducts.objects.filter(Ads_name=ad).prefetch_related('product')
    
    context = {
        'ad_content': ad_content,
        'ad': ad,
    }
    return render(request, 'store/ads-details.html', context)
# ===================================================
# صفحة العلامة التجارية
def brand_page(request, slug):
    brand = get_object_or_404(Brand, title=slug)
    last_products = Product.objects.filter(brand=brand).order_by('-updated_at')[:12]
    offerd_products = Product.objects.filter(brand=brand, offer=True)[:12]
    
    # تطبيق Paginator على جميع منتجات العلامة التجارية
    all_brand_products_list = Product.objects.filter(brand=brand)
    paginator_all = Paginator(all_brand_products_list, 12)  # 12 منتجًا لكل صفحة

    page_all = request.GET.get('page_all', 1)
    try:
        all_brand_products = paginator_all.page(page_all)
    except PageNotAnInteger:
        all_brand_products = paginator_all.page(1)
    except EmptyPage:
        all_brand_products = paginator_all.page(paginator_all.num_pages)
    
    # ===========================================================
    # إضافة فلترة أخرى بناءً على معايير المستخدم (البحث، السعر، العلامة التجارية)
    query = request.GET.get('q', '')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    category_id = request.GET.get('category')
   
    filters = Q(ready_to_sale=True) & Q(brand=brand)
    
    if query:
        filters &= (Q(name__icontains=query) | Q(tag__name__icontains=query))

    if price_min and price_min.isdigit():
        price_min = int(price_min)
        filters &= Q(
            Q(new_price__gte=price_min) | 
            (Q(offer=False) & Q(price__gte=price_min))
        )
        
    if price_max and price_max.isdigit():
        price_max = int(price_max)
        filters &= Q(
            Q(new_price__lte=price_max) | 
            (Q(offer=False) & Q(price__lte=price_max))
        )
    
    if category_id:
        # جلب التصنيف الأب
        parent_category = get_object_or_404(Category, id=category_id)
        # جلب التصنيفات الفرعية
        subcategories = Category.objects.filter(parent_category=parent_category)
        # دمج التصنيف الأب والتصنيفات الفرعية
        category_ids = [parent_category.id] + list(subcategories.values_list('id', flat=True))
        filters &= Q(category_id__in=category_ids)

    # جلب المنتجات بناءً على الفلاتر
    results = Product.objects.filter(filters).distinct()
    
    # إعداد التصفح المرقم
    paginator = Paginator(results, 20)  # عرض 20 منتجًا في كل صفحة
    page = request.GET.get('page', 1)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    # البيانات الإضافية للعرض
    categories = Category.objects.filter(status='visible')
    products_count = results.count()
    
    context = {
        'brand': brand,
        'all_brand_products': all_brand_products, # جميع منتجات البراند
        'products': products, # المنتجات المفلترة
        'last_products': last_products,
        'offerd_products':offerd_products,
        'categories': categories, # قائمة التصنيفا التي داخل مربع الفلترة
        'products_count': products_count,
    }
    
    return render(request, 'store/brand.html', context)
# ===================================================
# صفحة  بيع المنتجات بالنقاط
# def point_products_page(request):
    # products = Product.objects.filter(ready_to_sale=True,).order_by('-new_price')
    # products_count = products.count()
    
    # paginator = Paginator(products, 20)  # عرض 20 منتجًا في كل صفحة
    # page = request.GET.get('page', 1)

    # try:
    #     points_products = paginator.page(page)
    # except PageNotAnInteger:
    #     points_products = paginator.page(1)
    # except EmptyPage:
    #     points_products = paginator.page(paginator.num_pages)

    # if request.headers.get('x-requested-with') == 'XMLHttpRequest':
    #     results_data = list(points_products.object_list.values())
    #     return JsonResponse({'results': results_data})
    
    
    # context  ={
    #     'points_products': points_products,
    #     'products_count': products_count,
    # }
    # return render(request, 'store/points-products.html', context)
# ===================================================
# صفحة التصنيف
def category_page(request, slug):
    
    category = get_object_or_404(Category, slug=slug)
    
    # استرجاع التصنيفات الفرعية التي تنتمي للتصنيف الأب
    subcategories = Category.objects.filter(parent_category=category)
    
    # استرجاع المنتجات التي تنتمي للتصنيفات الفرعية
    subcategory_products = Product.objects.filter(category__in=subcategories)
    
    # استرجاع المنتجات التي تنتمي للتصنيف الأب مباشرة
    parent_category_products = Product.objects.filter(category=category)
    
    # دمج المنتجات من التصنيف الأب والتصنيفات الفرعية
    combined_products = parent_category_products | subcategory_products
    
    # حساب العدد الكلي للمنتجات
    total_products_count = combined_products.count()
    
    # الحصول على المنتجات التي سيتم عرضها (احصرها إلى 12)
    view_products = combined_products.distinct()[:12]
    # ===========================================================
    # إضافة فلترة أخرى بناءً على معايير المستخدم (البحث، السعر، العلامة التجارية)
    query = request.GET.get('q', '')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    brand_id = request.GET.get('brand')

    # فلترة المنتجات حسب التصنيف الأب والتصنيفات الفرعية
    filters = Q(ready_to_sale=True) & Q(category__in=[category] + list(subcategories))
    
    if query:
        filters &= (Q(name__icontains=query) | Q(tag__name__icontains=query))

    if price_min and price_min.isdigit():
        price_min = int(price_min)
        filters &= Q(
            Q(new_price__gte=price_min) | 
            (Q(offer=False) & Q(price__gte=price_min))
        )
        
    if price_max and price_max.isdigit():
        price_max = int(price_max)
        filters &= Q(
            Q(new_price__lte=price_max) | 
            (Q(offer=False) & Q(price__lte=price_max))
        )
    
    if brand_id:
        filters &= Q(brand_id=brand_id)

    # جلب المنتجات بناءً على الفلاتر
    results = Product.objects.filter(filters).distinct()
    
    # إعداد التصفح المرقم
    paginator = Paginator(results, 20)  # عرض 20 منتجًا في كل صفحة
    page = request.GET.get('page', 1)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    # البيانات الإضافية للعرض
    brands = Brand.objects.all()
    products_count = results.count()
    
    context = {
        'view_products': view_products,
        'category': category,
        'subcategories': subcategories,
        'total_products_count': total_products_count,  # إضافة العدد الكلي للمنتجات قبل الفلترة  
        'brands': brands,
        'products_count': products_count, # إضافة العدد الكلي للمنتجات بعد الفلترة  
        'products': products,  # عرض المنتجات التي تم فلترتها
    }
    return render(request, 'store/category.html', context)
# ===================================================
# صفحة العروض
def offer_page(request):
    products = Product.objects.filter(offer=True, ready_to_sale=True).order_by('-new_price')
    products_count = products.count()
    
    paginator = Paginator(products, 20)  # عرض 20 منتجًا في كل صفحة
    page = request.GET.get('page', 1)

    try:
        offerd_products = paginator.page(page)
    except PageNotAnInteger:
        offerd_products = paginator.page(1)
    except EmptyPage:
        offerd_products = paginator.page(paginator.num_pages)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        results_data = list(offerd_products.object_list.values())
        return JsonResponse({'results': results_data})
    
    
    context  ={
        'offerd_products': offerd_products,
        'products_count': products_count,
    }
    return render(request, 'store/offer-products.html', context)
# ===================================================
# صفحة البحث
def search_page(request):
    query = request.GET.get('q', '')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    category_id = request.GET.get('category')
    brand_id = request.GET.get('brand')

    filters = Q(ready_to_sale=True)

    if query:
        filters &= (Q(name__icontains=query) | Q(tag__name__icontains=query))

    if price_min and price_min.isdigit():
        price_min = int(price_min)
        filters &= Q(
            Q(new_price__gte=price_min) | 
            (Q(offer=False) & Q(price__gte=price_min))
        )
        
    if price_max and price_max.isdigit():
        price_max = int(price_max)
        filters &= Q(
            Q(new_price__lte=price_max) | 
            (Q(offer=False) & Q(price__lte=price_max))
        )
        
    if category_id:
        # جلب التصنيف الأب
        parent_category = get_object_or_404(Category, id=category_id)
        # جلب التصنيفات الفرعية
        subcategories = Category.objects.filter(parent_category=parent_category)
        # دمج التصنيف الأب والتصنيفات الفرعية
        category_ids = [parent_category.id] + list(subcategories.values_list('id', flat=True))
        filters &= Q(category_id__in=category_ids)
    if brand_id:
        filters &= Q(brand_id=brand_id)

    results = Product.objects.filter(filters).distinct()
    
 # إعداد التصفح المرقم
    paginator = Paginator(results, 20)  # عرض 20 منتجًا في كل صفحة
    page = request.GET.get('page', 1)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        results_data = list(products.object_list.values())
        return JsonResponse({'results': results_data})

    categories = Category.objects.filter(status='visible')
    brands = Brand.objects.all()
    products_count = results.count()

    return render(request, 'store/search.html', {
        'products': products,
        'categories': categories,
        'brands': brands,
        'products_count': products_count, 
    })
# ===================================================
# صفحة تفاصيل المنتج 
def product_details(request, pid):
    product = get_object_or_404(Product, id=pid)
    category = product.category
    brand = product.brand

    related_category_products = Product.objects.filter(category=category).exclude(pk=pid)[:8]
    related_brand_products = Product.objects.filter(brand=brand).exclude(pk=pid)[:8]

    product_images = product.images.all()

    variants = ProductVariation.objects.filter(product_item__product_id=pid, stock__gt=0).select_related('size', 'product_item')
    
    # الحصول على جميع الأحجام الفريدة المرتبطة بالمنتج
    sizes = SizeOption.objects.filter(variations__product_item__product_id=pid, variations__stock__gt=0).distinct()

    # تنظيم البيانات بحيث يتم تصنيف العناصر حسب المقاس
    size_item_map = {}
    for variant in variants:
        size = variant.size
        item = variant.product_item
        if size not in size_item_map:
            size_item_map[size] = []
        if item not in size_item_map[size]:
            size_item_map[size].append(item)

    context = {
        'product': product,
        'product_images': product_images,
        'related_category_products': related_category_products,
        'related_brand_products': related_brand_products,
        'size_item_map': size_item_map,
        'sizes': sizes,
    }

    return render(request, 'store/product-details.html', context)
# الدالة الخاصة بالحصول على كمية المنتج في صفحة  تفاصيل المنتج
def get_stock(request):
    size_id = request.GET.get('size_id')
    sku = request.GET.get('color')  # نستخدم color للإشارة إلى الـ SKU هنا

    try:
        # التحقق من وجود المتغير باستخدام sku و size_id
        variation = ProductVariation.objects.get(product_item__sku=sku, size_id=size_id)
        stock = variation.stock  # الكمية المتاحة في المخزون
        return JsonResponse({'stock': stock})
    except ProductVariation.DoesNotExist:
        return JsonResponse({'stock': 0})  # إذا لم يتم العثور على المتغير، رجع 0
# ===================================================
# صفحة المفضلة
@login_required
def favourite_page(request):
    """
        get_or_create يرجع tuple يحتوي على:
        الكائن (favourite في هذه الحالة).   
        قيمة True أو False (إذا تم إنشاء الكائن للتو)
        لذا نستعمل created
    """
    favourite, created = Favourite.objects.get_or_create(user=request.user) # احصل أو أنشئ المفضلة للمستخدم
    products = favourite.products.all() # احصل على جميع المنتجات المفضلة للمستخدم
    products_count = products.count() # احسب عدد المنتجات في المفضلة
    
    # search query
    query = request.GET.get('q', '')
    filters = Q(ready_to_sale=True) # & Q(كيف اضيف شرط ان المنتج داخل السلة)
    if query:
        filters &= (Q(name__icontains=query) | Q(tag__name__icontains=query))
        search_results = products.filter(filters).distinct()
    else:
        search_results = []
    # ============
    
    context = {
        'products': products,
        'products_count': products_count,
        'search_results': search_results,
    }
    return render(request, 'store/favourite.html', context)
# دالة الاضافة الى المفضلة
@login_required
def add_to_favourites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    favourite, created = Favourite.objects.get_or_create(user=request.user)
    if product in favourite.products.all():
        favourite.products.remove(product)
        added = False
    else:
        favourite.products.add(product)
        added = True

    response_data = {
        'added': added,
        'product_id': product_id,
    }

    return JsonResponse(response_data)
# دالة افراغ المفضلة
@login_required
def clear_favourites(request):
    """
    Clears all products from the user's favourites list.
    """
    favourite, created = Favourite.objects.get_or_create(user=request.user)
    favourite.products.clear()  # Remove all products from the favourites
    return redirect('store:favourite_page')  # Redirect back to the favourites page
# ===================================================
# صفحة السلة 
@login_required
def cart_page(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.prefetch_related('cart_item__product_item__variations__size').select_related('cart_item__product_item__product').all()  # احصل على جميع المنتجات في سلة المستخدم

    available_items = []
    unavailable_items = []
    
    total_qty = 0  # عدد المنتجات الاجمالي
    total_price = 0  # حساب السعر الاجمالي 
    total_bonus = 0  # حساب مجموع الـ bonus

    for item in cart_items:
        # تحقق من وجود المخزون للمتغير المرتبط بالمنتج
        product_variation = item.cart_item
        stock = product_variation.stock if product_variation else 0  # الكمية المتاحة
        
        if stock > 0:
            available_items.append({
                # اريد تمرير الكمية stock هنا المرتبطة بالمتغير المرتبط ب cartitem
                'product': item.cart_item.product_item.product,
                'product_item': item.cart_item.product_item,
                'size': product_variation.size.value if product_variation else 0,
                'color': item.cart_item.product_item.color,
                'qty': item.qty,
                'cart_item': item,
                'stock': int(stock)  # إضافة الكمية المتاحة
            })
            # تحديث العدد والسعر بناءً على العناصر المتاحة
            total_qty += item.qty
            total_price += item.cart_item.product_item.product.get_price() * item.qty
            total_bonus += item.cart_item.product_item.product.bonus * item.qty
        else:
            unavailable_items.append({
                'product': item.cart_item.product_item.product,
                'product_item': item.cart_item.product_item,
                'size': item.cart_item.product_item.variations.first().size.value if item.cart_item.product_item.variations.exists() else None,
                'color': item.cart_item.product_item.color,
                'qty': item.qty,
                'cart_item': item,
                'stock': 0,
            })

    av_count =  len(available_items)
    unav_count =  len(unavailable_items)
    
    context = {
        'cart_items': cart_items,
        'available_items': available_items,
        'unavailable_items': unavailable_items,
        'av_count': av_count,
        'unav_count': unav_count,
        'total_qty': total_qty,
        'total_price': total_price,
        'total_bonus': total_bonus,
    }

    return render(request, 'store/cart.html', context)
# دالة الاضافة الى السلة من صفحة تفاصيل المنتج 
@login_required
def add_to_cart(request):
    if request.method == 'POST':
        size_id = request.POST.get('size')
        sku = request.POST.get('item')
        quantity = int(request.POST.get('qty', 1))

        # التحقق من وجود المستخدم وسلة التسوق
        cart, created = Cart.objects.get_or_create(user=request.user)

        try:
            variation = ProductVariation.objects.get(product_item__sku=sku, size_id=size_id)

            if variation.stock >= quantity:
                # إضافة العنصر إلى السلة
                cart_item, created = CartItem.objects.get_or_create(
                    cart=cart,
                    cart_item=variation,
                    defaults={'qty': quantity}
                )

                if not created:  # إذا كان العنصر موجودًا بالفعل في السلة، نقوم بتحديث الكمية
                    cart_item.qty += quantity
                    cart_item.save()


                return JsonResponse({'status': 'success', 'message': 'تم إضافة العنصر إلى السلة'})
            else:
                return JsonResponse({'status': 'error', 'message': 'مخزون غير كاف'})

        except ProductVariation.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'المتغير غير موجود'})

    return JsonResponse({'status': 'error', 'message': 'طلب غير صالح'})
# دالة الاضافة الى السلة من بطاقة المنتج 
@login_required
def add_to_cart2(request, pid):
    if request.method == 'POST':
        product = get_object_or_404(Product, pid=pid)

        # الحصول على جميع عناصر المنتج
        product_items = product.items.all()
        available_variation = None
        
        # البحث عن متغير متوفر له مخزون في جميع عناصر المنتج
        for product_item in product_items:
            variations = product_item.variations.all()
            for variation in variations:
                if variation.stock > 0:
                    available_variation = variation
                    break  # إنهاء الحلقة إذا وجدنا متغيرًا متاحًا

            if available_variation:  # إذا وجدنا متغير متاح، نخرج من الحلقة
                break

        if available_variation is None:
            return JsonResponse({'success': False, 'error': 'لا يوجد مخزون متاح لأي من المتغيرات التابعة للمنتج.'})

        # إضافة المتغير المتاح إلى السلة
        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, cart_item=available_variation)

        if not created:
            cart_item.qty += 1
        else:
            cart_item.qty = 1

        cart_item.save()

        return JsonResponse({'success': True, 'message': 'تم إضافة المنتج إلى السلة.'})

    return JsonResponse({'success': False, 'error': 'الطلب غير صحيح.'})

# دالة الازالة من السلة
@login_required
def remove_from_cart(request, cart_item_id):
    if request.method == 'POST':
        try:
            cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
            cart_item.delete()  # احذف العنصر

            # إعداد البيانات للعودة إلى العميل
            return JsonResponse({
                'success': True,
                'message': 'Item removed from cart'
            })
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'CartItem does not exist'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
# دالة زر تغيير الكمية داخل السلة
@login_required
def update_cart_item_qty(request):
    if request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id')
        new_qty = request.POST.get('qty')
        # تحقق من أن cart_item_id و new_qty غير فارغين
        if not cart_item_id or not new_qty:
            return JsonResponse({'error': 'يرجى تقديم بيانات صحيحة.'}, status=400)

        try:
            # جلب العنصر من السلة
            cart_item = CartItem.objects.get(id=cart_item_id)
            product_variation = cart_item.cart_item  # تأكد من أن هذا هو الكائن الصحيح
            # تحقق من الكمية الجديدة
            new_qty = int(new_qty)  # تحويل الكمية إلى عدد صحيح
            if new_qty < 1:
                new_qty = 1
            elif new_qty > product_variation.stock:
                new_qty = product_variation.stock 
                
            # تحديث الكمية وحفظ التغييرات
            cart_item.qty = new_qty
            cart_item.save()
                        
            # إرجاع الكمية الجديدة والمخزون المتبقي
            return JsonResponse({
                'new_qty': new_qty,
                'stock_quantity': cart_item.get_stock_quantity(),
            })
        except CartItem.DoesNotExist:
            return JsonResponse({'error': 'العنصر غير موجود في السلة.'}, status=404)
        except ValueError:
            return JsonResponse({'error': 'الكمية يجب أن تكون عددًا صحيحًا.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500) # المشكلة تأتي من هنا

    return JsonResponse({'error': 'طريقة غير صحيحة، يجب أن تكون POST.'}, status=400)

# ===================================================





