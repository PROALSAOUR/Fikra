// ========================================================================================================= 
// تفعيل Swiper.js للسلايدر الرئيسي
const mainSwiper = new Swiper('.main-slider', {
  loop: true, // يجعل السلايدر دائريًا
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },
  autoplay: {
    delay: 5000, // تبديل الصورة تلقائيًا كل 5 ثانية
    disableOnInteraction: false,
  },
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
      if (mainSwiper) {
        mainSwiper.slideToLoop(index, 500, false); // التبديل إلى الصورة المحددة
      }
    });
  });
}

// تحديث الصورة الرئيسية عند التمرير في السلايدر الرئيسي
if (mainSwiper) {
  mainSwiper.on('slideChange', () => {
    const activeIndex = mainSwiper.realIndex;
    if (thumbnailSwiper) {
      thumbnailSwiper.slideTo(activeIndex, 500);
    }
    thumbnails.forEach((thumb, index) => {
      if (thumb.parentElement) {
        thumb.parentElement.classList.toggle('swiper-slide-active', index === activeIndex);
      }
    });
  });
}
// =================================================================================================== 
document.addEventListener('DOMContentLoaded', function() {
  const toggle = document.getElementById('them');
  const body = document.body;
  const sideMenu = document.querySelector('.mega-menu');
  const sideMenuCheckbox = document.getElementById('side-menu');

  // إعداد سلايدر المنتجات
  if (document.querySelector('.products-slider')) {
    var ProductSlider = new Swiper('.products-slider', {
      grabCursor: true,
      slidesPerView: 'auto',
      loopAdditionalSlides: 30, // لجعل الحركة أكثر سلاسة
    });
  }
    
  // تحقق من وجود الكلاس في localStorage واضف الكلاس إلى body إذا كان موجودًا
  if (localStorage.getItem('them') === 'light') {
    body.classList.add('light-them');
    if (toggle) {
      toggle.checked = true;
    }
  }

  // حدث عند تغيير حالة التشيك بوكس
  if (toggle) {
    toggle.addEventListener('change', function() {
      if (toggle.checked) {
        body.classList.add('light-them');
        localStorage.setItem('them', 'light');
      } else {
        body.classList.remove('light-them');
        localStorage.removeItem('them'); // تأكد من حذف المفتاح الصحيح
      }
    });
  }

  // إغلاق القائمة الجانبية عند النقر على زر الإغلاق
  const exitButton = document.querySelector('.exit');
  if (exitButton && sideMenuCheckbox && sideMenu) {
    exitButton.addEventListener('click', function() {
      sideMenuCheckbox.checked = false;
      body.classList.remove('no-scroll'); // إزالة منع التمرير
    });
  }

  // إغلاق القائمة الجانبية عند النقر على أي مكان خارجها
  document.addEventListener('click', function(event) {
    if (
      sideMenuCheckbox &&
      sideMenu &&
      !sideMenu.contains(event.target) &&
      !document.querySelector('.menu').contains(event.target) &&
      !event.target.matches('#side-menu')
    ) {
      sideMenuCheckbox.checked = false;
      body.classList.remove('no-scroll'); // إزالة منع التمرير
    }
  });

  // تفعيل خاصية التمرير عند فتح القائمة الجانبية
  if (sideMenuCheckbox) {
    sideMenuCheckbox.addEventListener('change', function() {
      if (sideMenuCheckbox.checked) {
        body.classList.add('no-scroll'); // منع التمرير
      } else {
        body.classList.remove('no-scroll'); // إزالة منع التمرير
      }
    });
  }

  // إعداد سلايدر الترويج
  if (document.querySelector('.tranding-slider')) {
    var TrandingSlider = new Swiper('.tranding-slider', {
      effect: 'coverflow',
      grabCursor: true,
      centeredSlides: true,
      loop: true,
      slidesPerView: 'auto',
      coverflowEffect: {
        rotate: 0,
        stretch: 0,
        depth: 100,
        modifier: 2.5,
      },
      autoplay: {
        delay: 2000, // مدة التأخير بالميلي ثانية (2000 ميلي ثانية = 2 ثانية)
        disableOnInteraction: false, // استمرار التشغيل التلقائي حتى عند التفاعل مع السلايدر
      },
      speed: 1000,
      loopAdditionalSlides: 30, // لجعل الحركة أكثر سلاسة
      freeMode: true, // تفعيل الوضع الحر لضمان الحركة المستمرة
    });
  }

  // إعداد سلايدر العلامات التجارية
  if (document.querySelector('.branding-slider')) {
    var BrandingSlider = new Swiper('.branding-slider', {
      grabCursor: true,
      centeredSlides: true,
      loop: true,
      slidesPerView: 'auto',
      autoplay: {
        delay: 0,
        disableOnInteraction: true, // استمرار التشغيل التلقائي حتى عند التفاعل مع السلايدر
      },
      speed: 10000,
      loopAdditionalSlides: 30, // لجعل الحركة أكثر سلاسة
      freeMode: true, // تفعيل الوضع الحر لضمان الحركة المستمرة
    });
  }
});
// ========================================================================================================
//  التعامل مع قائمة الفلاتر بصفحة البحث 
document.addEventListener('DOMContentLoaded', function () {
  const filterToggle = document.querySelector('.filter-toggle');
  const filterOptions = document.querySelector('.filter-options');
  const closeFilter = document.querySelector('.close-filter');
  const filterTabs = document.querySelectorAll('.filter-tab');
  const filterContent = document.querySelector('.filter-content');
  const applyFiltersButton = document.querySelector('.apply-filters');

  if (filterToggle && filterOptions) {
    // إظهار قائمة الفلترة عند الضغط على الأيقونة
    filterToggle.addEventListener('click', function (event) {
      event.stopPropagation(); // منع النقر من الانتشار إلى الوثيقة
      filterOptions.style.display = 'block';
    });
  }

  if (closeFilter && filterOptions) {
    // إخفاء قائمة الفلترة عند النقر على زر الإغلاق
    closeFilter.addEventListener('click', function (event) {
      event.stopPropagation(); // منع النقر من الانتشار إلى الوثيقة
      filterOptions.style.display = 'none';
    });
  }

  if (filterOptions && applyFiltersButton) {
    // إغلاق قائمة الفلاتر عند النقر على زر apply-filters فقط
    applyFiltersButton.addEventListener('click', function (event) {
      event.stopPropagation(); // منع النقر من الانتشار إلى الوثيقة
      filterOptions.style.display = 'none';
    });
  }

  if (filterOptions && filterToggle && filterContent) {
    // إغلاق قائمة الفلاتر عند النقر خارج القائمة
    document.addEventListener('click', function (event) {
      if (!filterOptions.contains(event.target) &&
          !filterToggle.contains(event.target) &&
          !filterContent.contains(event.target)) {
        filterOptions.style.display = 'none';
      }
    });
  }

  if (filterTabs.length > 0 && filterContent) {
    // التبديل بين الفلاتر عند النقر على أزرار الخيارات
    filterTabs.forEach(function (tab) {
      tab.addEventListener('click', function (event) {
        event.stopPropagation(); // منع النقر من الانتشار إلى الوثيقة
        const targetId = tab.dataset.target;
        const existingFilter = document.getElementById(`active-${targetId}`);

        // إذا كان الفلتر موجودًا بالفعل
        if (existingFilter) {
          // إزالة الفلتر من المحتوى
          existingFilter.remove();
          // إزالة اللون المختار من الزر
          tab.classList.remove('selected');
        } else {
          // إضافة فلتر جديد
          const newFilterGroup = document.createElement('div');
          newFilterGroup.classList.add('filter-group', 'active');
          newFilterGroup.id = `active-${targetId}`;

          const originalFilterGroup = document.getElementById(targetId);
          if (originalFilterGroup) {
            newFilterGroup.innerHTML = originalFilterGroup.innerHTML;
            filterContent.appendChild(newFilterGroup);
            // إضافة اللون المختار إلى الزر
            tab.classList.add('selected');
          }
        }
      });
    });

  
  }
});
// =========================================================================================================
//  انشاء تأثير قلب البطاقة لصفحة تسجيل الدخول 
document.addEventListener('DOMContentLoaded', function() {
  const flipButtons = document.querySelectorAll('.flip');
  const signCard = document.querySelector('.sign-card');
  
  // استرجاع حالة البطاقة من localStorage
  const isFlipped = localStorage.getItem('isFlipped') === 'true';
  
  // تطبيق حالة البطاقة عند تحميل الصفحة
  if (isFlipped) {
    signCard.classList.add('rotate');
  }
  
  if (flipButtons.length > 0 && signCard) {
    flipButtons.forEach(button => {
      button.addEventListener('click', function() {
        signCard.classList.toggle('rotate');
        
        // حفظ الحالة الجديدة في localStorage
        const isCurrentlyFlipped = signCard.classList.contains('rotate');
        localStorage.setItem('isFlipped', isCurrentlyFlipped);
      });
    });
  }
});
// =========================================================================================================
// كود اظهار المحتوى في صفحة الاسئلة الشائعة و رسائل المستخدم
function toggleContent(element) {
  const content = element.nextElementSibling;
  const icon = element.querySelector('i');

  if (content.style.display === "block") {
      content.style.display = "none";
      icon.classList.remove('fa-chevron-up');
      icon.classList.add('fa-chevron-down');
  } else {
      content.style.display = "block";
      icon.classList.remove('fa-chevron-down');
      icon.classList.add('fa-chevron-up');
  }
}
// =========================================================================================================
//  كود  تغيير حالة الرسالة الى مقروئة عند النقر عليها
function markMessageAsRead(markUrl, element) {
  const notificationMessage = element.parentElement;

  // تحقق مما إذا كانت الرسالة قد قرئت مسبقًا
  if (!notificationMessage.classList.contains('read')) {
      // أضف كلاس 'read' لتغيير حالة الرسالة
      notificationMessage.classList.add('read');

      // إرسال طلب AJAX إلى الخادم لتحديث حالة الرسالة
      fetch(markUrl, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': getCookie('csrftoken') // تضمين CSRF token
          },
      })
      .then(response => {
          if (!response.ok) {
              console.error('Failed to mark as read.');
          }
      })
      .catch(error => {
          console.error('Error:', error);
      });
  }
}
// =========================================================================================================
// دالة لجلب الـ CSRF token من الكوكيز
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
// =========================================================================================================
// الدالة المسؤلة عن اعادة المستخدم الى الصفحة التي جاء منها في تفاصيل المنتج
function goBack() {
  window.history.back();
}
// =========================================================================================================
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
// =========================================================================================================
// دالة اضافة المنتج و ازالته من المفضلة
$(document).ready(function() {
  $('.add-to-fav-link').on('click', function(event) {
      event.preventDefault(); // Prevent the default link behavior

      var $this = $(this);
      var url = $this.attr('href');
      var productId = $this.data('product-id');

      $.ajax({
          url: url,
          method: 'GET',
          success: function(response) {
              if (response.added) {
                  $this.find('i').removeClass('fa-regular fa-heart').addClass('fa-solid fa-heart');
              } else {
                  $this.find('i').removeClass('fa-solid fa-heart').addClass('fa-regular fa-heart');
              }

              // Reload the page if the user is on the favourites page
              if (window.location.pathname === '/favourite/') {
                  location.reload();
              }
          },
          error: function(xhr, status, error) {
              console.error('Error adding to favourites:', error);
          }
      });
  });
});
// =========================================================================================================
// الدالة الخاصة بإفراغ المفضلة
document.addEventListener('DOMContentLoaded', function() {
  var clearBtn = document.getElementById('clear-favourites-btn');
  if (clearBtn) {
      clearBtn.addEventListener('click', function() {
          fetch(clearFavouritesUrl, {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
                  'X-CSRFToken': csrfToken
              },
              body: JSON.stringify({})
          }).then(response => {
              if (response.ok) {
                  location.reload(); // إعادة تحميل الصفحة لتحديث المفضلة
              } else {
                  alert('حدث خطأ أثناء محاولة إفراغ المفضلة.');
              }
          }).catch(error => {
              console.error('حدث خطأ:', error);
              alert('حدث خطأ أثناء محاولة إفراغ المفضلة.');
          });
      });
  }
});
// =========================================================================================================
// دالة اضافة المنتج الى السلة من البطاقة الخاصة به
$(document).ready(function() {
  $('.add-to-cart-link').click(function(e) {
      e.preventDefault(); // منع الانتقال إلى الرابط

      var url = $(this).attr('href'); // الحصول على الرابط من عنصر الارتباط

      $.ajax({
          type: 'POST',
          url: url,
          data: {
              csrfmiddlewaretoken: getCookie('csrftoken'), // استخدام الدالة لجلب رمز CSRF
          },
          success: function(response) {
              if (response.success) {
                  showAddToCartMenu(); // عرض النافذة المنبثقة عند النجاح
              } else {
                  alert(response.error); // عرض رسالة الخطأ
              }
          },
          error: function() {
              alert('حدث خطأ أثناء إرسال الطلب.');
          }
      });
  });
});
// =========================================================================================================
//  دالة ازالة المنتج من السلة
document.querySelectorAll('.add-to-trash a').forEach(function(button) {
  button.addEventListener('click', function(event) {
      event.preventDefault();  // منع إعادة تحميل الصفحة

      const cartItemId = this.dataset.cartItemId;  // الحصول على معرف عنصر السلة
      const url = this.getAttribute('href');  // الرابط الخاص بحذف العنصر من السلة

      // استخدام دالة getCookie لجلب توكن CSRF من الكوكيز
      const csrftoken = getCookie('csrftoken');

      // إرسال طلب Ajax لحذف العنصر
      fetch(url, {
          method: 'POST',
          headers: {
              'X-CSRFToken': csrftoken,  // إضافة توكن CSRF
              'Content-Type': 'application/json',
              'X-Requested-With': 'XMLHttpRequest'  // تأكد من أن الطلب يعتبر طلب Ajax
          },
          body: JSON.stringify({
              'cart_item_id': cartItemId,  // إرسال معرف عنصر السلة
          })
      })
      .then(response => {
          if (!response.ok) {
              throw new Error('Network response was not ok');
          }
          return response.json();
      })
      .then(data => {
          if (data.success) {
              // إعادة تحميل الصفحة بعد الحذف
              location.reload();  // أو يمكنك استخدام window.location.reload();
          } else {
              console.error('Error removing item:', data.error);
          }
      })
      .catch(error => console.error('Error:', error));
  });
});
// =========================================================================================================
// كود زر تغيير الكمية داخل السلة 
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.cart-q').forEach(quantityElem => {
      const minusButton = quantityElem.querySelector('.minus');
      const plusButton = quantityElem.querySelector('.plus-cart');
      const quantityInput = quantityElem.querySelector('.quantity-value');
      const stockQuantityElem = quantityElem.querySelector('.stock-quantity-h');
      const itemId = quantityElem.dataset.cartItemId; // افترض وجود data-cart-item-id في الـ HTML

      // عند النقر على زر الناقص
      minusButton.addEventListener('click', () => {
          let currentQty = parseInt(quantityInput.value);
          if (currentQty > 1) {
              quantityInput.value = currentQty - 1;
              updateStockDisplay();
              updateCartItem(itemId, quantityInput.value);
          }
      });

      // عند النقر على زر الزائد
      plusButton.addEventListener('click', () => {
          let currentQty = parseInt(quantityInput.value);
          const stockQuantity = parseInt(stockQuantityElem.value);
          if (currentQty < stockQuantity) {
              quantityInput.value = currentQty + 1;
              updateStockDisplay();
              updateCartItem(itemId, quantityInput.value);
          }
      });

      // تحديث العرض الخاص بالمخزون
      function updateStockDisplay() {
        // الحصول على العنصر الجذري (الذي يحمل class "cart-q") للسياق الحالي
        const cartItemElement = quantityInput.closest('.cart-q');
        const stockQuantityElem = cartItemElement.querySelector('.stock-quantity-h'); // استخدم العنصر الخاص بالمخزون في السياق الحالي
        const stockQuantityDisplay = cartItemElement.querySelector('.stock-quantity'); // استخدم العنصر الذي يعرض الكمية المتبقية

        const currentQty = parseInt(quantityInput.value);
        const stockQuantity = parseInt(stockQuantityElem.value);
        
        // تحديث المخزون المتبقي بناءً على الكمية الحالية
        const newStockQuantity = stockQuantity - currentQty;

        // تحديث العنصر الذي يعرض الكمية المتبقية في المخزون
        if (stockQuantityDisplay) {
            stockQuantityDisplay.textContent = newStockQuantity;
        } else {
            console.error('Element with class "stock-quantity" not found.');
        }
    }

      // عند فقدان التركيز على مربع الكمية
      quantityInput.addEventListener('blur', () => {
          const currentQty = parseInt(quantityInput.value);
          const stockQuantity = parseInt(stockQuantityElem.value);

          if (currentQty < 1) {
              quantityInput.value = 1;
              updateCartItem(itemId, 1);
              updateStockDisplay();
          } else if (currentQty > stockQuantity) {
              quantityInput.value = stockQuantity;
              updateCartItem(itemId, stockQuantity);
              updateStockDisplay();
          }
      });

      // عند تغيير القيمة في مربع الكمية
      quantityInput.addEventListener('change', () => {
          clearTimeout(timeout);
          timeout = setTimeout(() => {
              updateCartItem(itemId, parseInt(quantityInput.value));
          }, 2000);
      });

      let timeout;

      // دالة رفع التغييرات إلى السيرفر
      function updateCartItem(cartItemId, newQty) {
          $.ajax({
              url: updateCartUrl, // استخدام المتغير الممرر من الـ HTML
              method: 'POST',
              data: {
                  cart_item_id: cartItemId,
                  qty: newQty,
                  csrfmiddlewaretoken: getCookie('csrftoken') // استخدام دالة جلب الـ CSRF token
              },
              success: function(response) {
                  stockQuantityElem.value = response.new_stock; // تحديث الكمية المتاحة
              },
              error: function(xhr) {
                  console.error(xhr.responseText);
              }
          });
      }
  });
});
// =========================================================================================================


