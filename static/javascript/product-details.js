document.addEventListener('DOMContentLoaded', function() {
    // تفعيل Swiper.js للسلايدر الرئيسي
    const mainproductSwiper = new Swiper('.main-slider', {
        loop: true, // يجعل السلايدر دائريًا
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        autoplay: {
            delay: 5000, // تبديل الصورة تلقائيًا كل 5 ثواني
            disableOnInteraction: false,
        },
        on: {
            init: function () {
                updateImageCount(this); // عند تحميل الصفحة لأول مرة
            },
            slideChange: function () {
                updateImageCount(this); // عند تغيير الشريحة
            }
        }
    });

    // تفعيل Swiper.js للصور الثانوية
    const thumbnailSwiper = new Swiper('.thumbnail-slider', {
        slidesPerView: 4, // عدد الصور الظاهرة في العرض الواحد
        spaceBetween: 10, // المسافة بين الصور
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        loop: false,
    });

    // جافا سكريبت لتبديل الصور عند النقر على الصور الثانوية
    const thumbnails = document.querySelectorAll('.thumbnail');
    if (thumbnails.length > 0) {
        thumbnails.forEach((thumbnail, index) => {
            thumbnail.addEventListener('click', () => {
                if (mainproductSwiper) {
                    mainproductSwiper.slideToLoop(index, 500, false); // التبديل إلى الصورة المحددة
                }
            });
        });
    }

    // تحديث الصورة المصغرة عند التمرير في السلايدر الرئيسي
    if (mainproductSwiper) {
        mainproductSwiper.on('slideChange', () => {
            const activeIndex = mainproductSwiper.realIndex;

            // تزامن السلايدر الثانوي
            if (thumbnailSwiper) {
                thumbnailSwiper.slideTo(activeIndex, 500);
            }

            // تمييز الصورة المصغرة النشطة
            thumbnails.forEach((thumb, index) => {
                if (thumb.parentElement) {
                    thumb.parentElement.classList.toggle('swiper-slide-active', index === activeIndex);
                }
            });
        });
    }

    // دالة لتحديث العداد
    function updateImageCount(swiper) {
        const currentIndex = swiper.realIndex + 1; // لأن realIndex يبدأ من 0
        const totalSlides = swiper.slides.length - swiper.loopedSlides * 2; // حذف الصور المكررة بسبب loop
        const imageCountElement = document.querySelector('.image-count');

        if (imageCountElement) {
            imageCountElement.textContent = `${currentIndex} / ${totalSlides}`;
        }
    }
});

// =============================================================================================
// الدالة المسؤلة عن تغيير لون المنتج و  كمية المخزون بشكل ديناميكي واضافة المنتج الى السلة من الصفحة
document.addEventListener('DOMContentLoaded', function() {
    var sizeOptions = document.querySelectorAll('.size-option');
    var itemGroups = document.querySelectorAll('.item-group');
    var colorOptions = document.querySelectorAll('.item-option');
    var stockQuantityElement = document.getElementById('stock-quantity');
    var userQuantityInput = document.getElementById('user-quantity');
    var plusButton = document.querySelector('.plus');
    var minusButton = document.querySelector('.minus');
    var availableStock = 0; // الكمية المتاحة للمقاس واللون المختارين
    // تحقق من وجود العناصر
    if (!sizeOptions.length || !itemGroups.length || !colorOptions.length || !stockQuantityElement || !userQuantityInput || !plusButton || !minusButton) {
        return; // إذا كان هناك عنصر مفقود، نخرج من الدالة
    }
  
    function selectFirstColor(group) {
        var firstColor = group.querySelector('.item-option');
        if (firstColor && !firstColor.checked) {
            firstColor.checked = true; // تحديد أول لون بشكل افتراضي إذا لم يكن محددًا
        }
    }
  
    function updateItemGroups() {
        var selectedSizeId = document.querySelector('.size-option:checked')?.value;
  
        resetQuantity(); // إعادة تعيين الكمية إلى القيمة الافتراضية (1)
  
        itemGroups.forEach(function(group) {
            if (selectedSizeId && group.getAttribute('data-size-id') === selectedSizeId) {
                group.style.display = 'block';
                selectFirstColor(group); // تحديد أول لون عند تغيير المقاس
            } else {
                group.style.display = 'none';
            }
        });
  
        getSelectedSizeAndColor(); // تحديث المخزون عند تغيير المقاس
    }
  
    sizeOptions.forEach(function(sizeOption) {
        sizeOption.addEventListener('change', updateItemGroups);
    });
  
    colorOptions.forEach(function(colorOption) {
        colorOption.addEventListener('change', function() {
            resetQuantity(); // إعادة تعيين الكمية إلى القيمة الافتراضية (1)
            getSelectedSizeAndColor();
        });
    });
  
    function updateStock(sizeId, sku) {
        fetch(`/get-stock?size_id=${sizeId}&color=${encodeURIComponent(sku)}`)
            .then(response => response.json())
            .then(data => {
                if (data.stock !== undefined) {
                    availableStock = data.stock ; // تخزين الكمية المتاحة
                    stockQuantityElement.textContent = availableStock -1 ; // تحديث الكمية المعروضة
                    userQuantityInput.max = availableStock; // ضبط الحد الأقصى للكمية
                    updateQuantityDisplay(); // تحديث الكمية الظاهرة بناءً على المخزون الجديد
                }
            })
            .catch(error => console.error('Error fetching stock:', error));
    }
  
    function getSelectedSizeAndColor() {
        var selectedSize = document.querySelector('.size-option:checked');
        var selectedSku = document.querySelector('.item-option:checked');
  
        if (selectedSize && selectedSku) {
            var sizeId = selectedSize.value;
            var sku = selectedSku.value; // استخدام الـ SKU الآن
            console.log(`Selected size: ${sizeId}, SKU: ${sku}`); // تأكيد القيم المختارة
            updateStock(sizeId, sku); // تمرير الـ SKU إلى دالة التحديث
        } else {
            console.log('Size or SKU not selected');
        }
    }
  
    function resetQuantity() {
        userQuantityInput.value = 1; // إعادة تعيين الكمية إلى القيمة الافتراضية
        adjustStock(); // إعادة ضبط المخزون بناءً على الكمية الجديدة
    }
  
    function updateQuantityDisplay() {
        var userQuantity = parseInt(userQuantityInput.value);
        if (isNaN(userQuantity) || userQuantity < 1) {
            userQuantityInput.value = 1;
        } else if (userQuantity > availableStock) {
            userQuantityInput.value = availableStock;
        }
    }
  
    function adjustStock() {
        var userQuantity = parseInt(userQuantityInput.value);
        var initialQuantity = 1; // القيمة الافتراضية لمربع الإدخال
        var adjustedStock = availableStock - Math.max(userQuantity, initialQuantity);
        stockQuantityElement.textContent = adjustedStock;
    }
  
    plusButton.addEventListener('click', function(event) {
        event.preventDefault(); // منع تصرفات الزر الافتراضية
        var currentQuantity = parseInt(userQuantityInput.value);
        if (currentQuantity < availableStock) {
            userQuantityInput.value = currentQuantity + 1;
        }
        updateQuantityDisplay();
        adjustStock();
    });
  
    minusButton.addEventListener('click', function(event) {
        event.preventDefault(); // منع تصرفات الزر الافتراضية
        var currentQuantity = parseInt(userQuantityInput.value);
        if (currentQuantity > 1) {
            userQuantityInput.value = currentQuantity - 1;
        }
        updateQuantityDisplay();
        adjustStock();
    });
  
    userQuantityInput.addEventListener('input', function() {
        updateQuantityDisplay();
        adjustStock();
    });
  
    let hideTimeout;
  
    function showAddToCartMenu() {
        const menu = document.querySelector('.add-cart-pop-page');
        if (!menu) return; // تأكد من وجود القائمة
  
        menu.style.display = 'block';
        setTimeout(() => {
            menu.style.visibility = 'visible';
            menu.style.opacity = '1';
            menu.style.transform = 'translate(-50%, -40%) scale(1)';
        }, 10);
  
        clearTimeout(hideTimeout);
        hideTimeout = setTimeout(hideMenu, 3000);
    }
  
    function hideMenu() {
        const menu = document.querySelector('.add-cart-pop-page');
        if (!menu) return; // تأكد من وجود القائمة
  
        menu.style.opacity = '0';
        menu.style.transform = 'translate(-50%, -40%) scale(0.5)';
        setTimeout(() => {
            menu.style.visibility = 'hidden';
            menu.style.display = 'none';
        }, 300);
    }
  
    document.querySelector('.form').addEventListener('submit', function(e) {
        e.preventDefault(); // منع النموذج من الإرسال التلقائي
  
        var formData = new FormData(this); // استخدام FormData لجمع البيانات
        var url = this.action; // URL للدالة
  
        fetch(url, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken') 
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                showAddToCartMenu();
                // يمكنك تحديث واجهة المستخدم أو سلة التسوق هنا
            } else {
                alert(data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    });
  
    updateItemGroups(); // تحديث المجموعات والعناصر عند تحميل الصفحة لأول مرة
});
// =============================================================================================
// دالة نسخ الرابط بصفحة تفاصيل المنتج
function copyLink() {
    const dummy = document.createElement('input'),
        text = window.location.href;  // الحصول على رابط الصفحة الحالية
  
    document.body.appendChild(dummy);
    dummy.value = text;
    dummy.select();
    document.execCommand('copy');
    document.body.removeChild(dummy);
  
    alert("تم نسخ رابط المنتج بنجاح!");
}
// =============================================================================================
// دالة اضافة المنتج لقائمة الاهتمامات
document.addEventListener("DOMContentLoaded", function() {
    let btn = document.getElementById("notify-btn");
    if (btn) {
        btn.addEventListener("click", function() {
            let url = btn.getAttribute("data-url");  // استخراج رابط API من data-url
            let csrfToken = getCookie("csrftoken");  // جلب الـ CSRF token من الكوكيز
            
            fetch(url, {
                method: "POST",
                headers: { 
                    "X-CSRFToken": csrfToken,  // استخدام الـ CSRF token من الكوكيز
                    "Content-Type": "application/json"
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    btn.classList.add("interested");
                    btn.textContent = "سوف نقوم بإعلامك فور توفر المنتج✅";
                } else {
                    alert(data.message);
                }
            })
            .catch(error => console.error("Error:", error));
        });
    }
});
// =============================================================================================

