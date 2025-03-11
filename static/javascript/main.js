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
  if (isFlipped && signCard) {
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
document.addEventListener('DOMContentLoaded', function() {
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

  // تأكد من تحميل jQuery أولاً
  if (window.jQuery) {
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
  }
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
      const leftInStock = quantityElem.querySelector('.stock-quantity'); // تأكد من أن leftInStock مرتبط بكل عنصر

      const itemId = quantityElem.dataset.cartItemId; // افترض وجود data-cart-item-id في الـ HTML

      // تحقق من قيمة qty عند تحميل الصفحة
      const initialQty = parseInt(quantityInput.value);
      const stockQuantity = parseInt(stockQuantityElem.value);

      if (initialQty < 1) {
        quantityInput.value = 1;
        updateCartItem(itemId, 1);
        updateStockDisplay(quantityElem);
        schedulePageRefresh();
      } else if (initialQty > stockQuantity) {
        quantityInput.value = stockQuantity;
        updateCartItem(itemId, stockQuantity);
        updateStockDisplay(quantityElem);
        schedulePageRefresh();
      }

      // عند النقر على زر الناقص
      minusButton.addEventListener('click', () => {
          let currentQty = parseInt(quantityInput.value);
          if (currentQty > 1) {
              quantityInput.value = currentQty - 1;
              updateStockDisplay(quantityElem);
              updateCartItem(itemId, quantityInput.value);
              schedulePageRefresh();
          }
      });

      // عند النقر على زر الزائد
      plusButton.addEventListener('click', () => {
        const currentQty = parseInt(quantityInput.value);
        const stockQuantity = parseInt(stockQuantityElem.value); 
        // تحقق مما إذا كانت الكمية الحالية أقل من المخزون المتاح لهذا العنصر
        if (currentQty < stockQuantity) {
            quantityInput.value = currentQty + 1;  // زيادة الكمية
            updateStockDisplay(quantityElem);  // تحديث عرض الكمية المتبقية
            updateCartItem(itemId, quantityInput.value);  // تحديث الكمية في الخادم
            schedulePageRefresh();
        } 
      });
    
      // تحديث العرض الخاص بالمخزون
      function updateStockDisplay(elem) {
        const currentQty = parseInt(elem.querySelector('.quantity-value').value);
        const stockQuantity = parseInt(elem.querySelector('.stock-quantity-h').value);
        
        // تحديث المخزون المتبقي بناءً على الكمية الحالية
        const newStockQuantity = stockQuantity - currentQty;

        // تحديث العنصر الذي يعرض الكمية المتبقية في المخزون
        const stockQuantityDisplay = elem.querySelector('.stock-quantity');
        if (stockQuantityDisplay) {
            stockQuantityDisplay.textContent = newStockQuantity;
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
              schedulePageRefresh();
          } else if (currentQty > stockQuantity) {
              quantityInput.value = stockQuantity;
              updateCartItem(itemId, stockQuantity);
              updateStockDisplay(quantityElem);
              schedulePageRefresh();
          }
      });

      // عند تغيير القيمة في مربع الكمية
      quantityInput.addEventListener('change', () => {
          clearTimeout(timeout);
          timeout = setTimeout(() => {
              updateCartItem(itemId, parseInt(quantityInput.value));
              schedulePageRefresh();
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
                  // تحديث الكمية المتبقية في المخزون في العنصر الصحيح
                  leftInStock.innerText = response.stock_quantity;
              },
              error: function(xhr) {
                  console.error(xhr.responseText);
              }
          });
      }

      // دالة لتحديث الصفحة بعد ثانية واحدة
      function schedulePageRefresh() {
        setTimeout(() => {
            location.reload(); // تحديث الصفحة
        }, 200); // التأخير بالميللي ثانية
    }
  });
});
// =========================================================================================================
// دوال اختيار كوبون  داخل السلة
// دالة للتحقق من حالة مربع الاختيار
function checkCheckbox() {
  // الحصول على مربع الاختيار
  const checkbox = document.querySelector('input[name="use-this"]');
  // الحصول على div الذي يحتوي على كلاس receipt
  const receiptDiv = document.querySelector('.receipt');

  if (checkbox && receiptDiv) {
      // التحقق مما إذا كان مربع الاختيار مختارًا
      if (checkbox.checked) {
          // إضافة كلاس offer إذا كان مختارًا
          receiptDiv.classList.add('offer');
      } else {
          // إزالة كلاس offer إذا لم يكن مختارًا
          receiptDiv.classList.remove('offer');
      }
  }
}
// استدعاء الدالة عند تغيير حالة مربع الاختيار
document.addEventListener('DOMContentLoaded', function() {
  const checkbox = document.querySelector('input[name="use-this"]');
  if (checkbox) {
      checkbox.addEventListener('change', checkCheckbox); // إضافة حدث التغيير
  }

  // استدعاء الدالة عند تحميل الصفحة للتحقق من الحالة الافتراضية
  checkCheckbox();
});
// دالة وظيفتها اختيار كوبون خصم داخل السلة
function applyCoponCard(event) {
  // منع تحديث الصفحة عند النقر على الزر
  event.preventDefault();

  // الحصول على الراديو المختار
  const selectedRadio = document.querySelector('input[type="radio"][name="choosen-copon-card"]:checked');

  if (selectedRadio) {
      // الحصول على قيم sell_value و gift_id و gift_name من الراديو المختار
      const coponValue = parseFloat(selectedRadio.getAttribute('data-value'));
      const coponId = selectedRadio.getAttribute('data-copon-id');
      const coponName = selectedRadio.getAttribute('data-copon-name'); // الحصول على الاسم

      // تعديل span الذي يحتوي على class old و class new لوضع القيم
      const totalPriceElement = document.querySelector('.total-price .old');
      const newPriceElement = document.querySelector('.total-price .new');

      if (totalPriceElement && newPriceElement) {
          const totalPrice = parseFloat(totalPriceElement.textContent) || 0;
          const discountAmount = coponValue ;

          let newPrice = totalPrice - discountAmount;

          if (newPrice < 0) {
              newPrice = 0; // إذا كانت القيمة سالبة، ضع 0
          }

          newPriceElement.textContent = ' | ' + newPrice.toFixed(1); // وضع القيمة الجديدة
      }

      // إخفاء عنصر p.add-copon-link
      const addCoponLink = document.querySelector('.add-copon-link');
      if (addCoponLink) {
          addCoponLink.classList.add('hidden');
      }

      // إظهار div.check-code
      const checkCodeDiv = document.querySelector('.check-code');
      if (checkCodeDiv) {
          checkCodeDiv.classList.remove('hidden');

          // تحديث قيم input المخفي داخل check-code
          const cardIdInput = checkCodeDiv.querySelector('input[name="card-id"]');
          const cardInfoParagraph = checkCodeDiv.querySelector('p'); 

          if ( cardIdInput) {
              cardIdInput.value = coponId; 

              // تحديث نص <p> بالمعلومات الجديدة
              cardInfoParagraph.textContent = ` استعمال: ${coponName} بقيمة: ${coponValue} دينار`;
          }
      }

      // جعل مربع الاختيار مختارًا عند تطبيق بطاقة الهدية
      const checkbox = document.querySelector('input[name="use-this"]');
      if (checkbox) {
          checkbox.checked = true; // اجعله مختارًا
          checkCheckbox(); // استدعاء الدالة للتحقق من حالة checkbox
      }
  }

  // إعادة جميع التغييرات عند تحديث الصفحة
  window.onbeforeunload = function () {
      const addCoponLink = document.querySelector('.add-copon-link');
      const checkCodeDiv = document.querySelector('.check-code');

      if (addCoponLink) {
          addCoponLink.classList.remove('hidden');
      }

      if (checkCodeDiv) {
          checkCodeDiv.classList.add('hidden');
          const cardIdInput = checkCodeDiv.querySelector('input[name="card-id"]');

          if (cardIdInput) {
            cardIdInput.value = '';
          }

          const cardInfoParagraph = checkCodeDiv.querySelector('p');
          if (cardInfoParagraph) {
              cardInfoParagraph.textContent = ''; // إعادة النص إلى الحالة الافتراضية
          }
      }

      // إلغاء اختيار الـ checkbox عند تحديث الصفحة
      const checkbox = document.querySelector('input[name="use-this"]'); // تحديد الـ checkbox
      if (checkbox) {
          checkbox.checked = false; // إلغاء الاختيار
      }
  };
}
//  =========================================================================================================
// الكود الخاص بعرض النافذة الخاصة باستعمال كود الهدية
document.addEventListener('DOMContentLoaded', function() {
  const shareCodeMenu = document.querySelector('.use-code-pop-page');
  const shareCodeLink = document.querySelector('.use-code-link');
  const verfieButton = document.querySelector("input[name='verfie-code']")

  if (verfieButton && shareCodeMenu && shareCodeLink) {
    // ارسال بيانات الفورم الى دالة بايثون
    $(document).ready(function() {
      $("form").on("submit", function(event) {
          event.preventDefault(); // منع إعادة تحميل الصفحة
    
          var verfieCode = $(verfieButton).val(); // الحصول على القيمة من حقل الإدخال
    
          $.ajax({
              url: "/cards/verfie-code/",
              type: "POST",
              data: JSON.stringify({
                  'verfie-code': verfieCode
              }),
              contentType: "application/json",
              headers: {
                  'X-CSRFToken': getCookie('csrftoken')
              },
              success: function(response) {
                  // تحديث عرض الرسائل هنا
                  if (response.success) {
                      $(".errors").html("<div class='success error-message'><p>" + response.message + "</p></div>");
                      setTimeout(function() {
                        hideShareCodeMenu();
                        location.reload();
                      }, 2000); // تأخير لمدة 2 ثانية (2000 ميلي ثانية)
                  } else {
                      $(".errors").html("<div class='error-message'><p>" + response.message + "</p></div>");
                  }
              },
              error: function(xhr, status, error) {
                  console.error(error);
                  $(".errors").html("<div class='error-message'><p>حدث خطأ، يرجى المحاولة لاحقاً.</p></div>");
              }
          });
      });
    });  

    // دالة لإظهار القائمة
    function showShareCodeMenu() {
      shareCodeMenu.style.display = 'block'; // عرض القائمة
      setTimeout(() => {
          shareCodeMenu.style.visibility = 'visible';
          shareCodeMenu.style.opacity = '1';
          shareCodeMenu.style.transform = 'translate(-50%, -40%) scale(1)';
      }, 10);
      // حفظ حالة القائمة على أنها ظاهرة
      localStorage.setItem('shareCodeMenuVisibility', 'visible');
    }

    // دالة لإخفاء القائمة
    function hideShareCodeMenu() {
        shareCodeMenu.style.opacity = '0';
        shareCodeMenu.style.transform = 'translate(-50%, -40%) scale(0.5)';
        setTimeout(() => {
            shareCodeMenu.style.visibility = 'hidden';
            shareCodeMenu.style.display = 'none';
        }, 300);
        // حفظ حالة القائمة على أنها مخفية
        localStorage.setItem('shareCodeMenuVisibility', 'hidden');
    }

    // استرجاع الحالة المحفوظة من localStorage عند تحميل الصفحة
    const savedVisibility = localStorage.getItem('shareCodeMenuVisibility');
    if (savedVisibility === 'visible') {
        showShareCodeMenu(); // إظهار القائمة إذا كانت ظاهرة قبل التحديث
    } else {
        hideShareCodeMenu(); // إخفاء القائمة إذا كانت مخفية
    }

    // التحقق من وجود العناصر قبل إضافة الأحداث
    shareCodeLink.addEventListener('click', function (e) {
        e.preventDefault();
        if (shareCodeMenu.style.visibility === 'hidden' || shareCodeMenu.style.visibility === '') {
            showShareCodeMenu();
        }
    });

    // إخفاء القائمة عند النقر خارجها
    document.addEventListener('click', function (e) {
        if (shareCodeMenu && shareCodeMenu.style.visibility === 'visible' && !shareCodeMenu.contains(e.target) && !shareCodeLink.contains(e.target)) {
            hideShareCodeMenu();
        }
    });

  }
});
// =============================================================================================
// الكود الخاص بعملية انشاء طلب في السلة 
// الكود الخاص بعرض النافذة الخاصة بإتمام عملية الطلب بنجاح
document.addEventListener('DOMContentLoaded', function() {
  const confirmButton = document.querySelector('form.discount .confirm');
  const menu = document.querySelector('.ordered-done-pop-page');
  const link = document.querySelector('.ordered-done-link');
  
  // تحقق من وجود الزر قبل إضافة حدث 'click'
  if (confirmButton) {
      confirmButton.addEventListener('click', function (e) {
          e.preventDefault(); // منع إعادة تحميل الصفحة

          // جلب الفورم الذي يحتوي على الزر الذي تم النقر عليه
          const form = confirmButton.closest('form'); 
          const formData = new FormData(form); // جمع بيانات النموذج

          // التحقق من القيم وإعداد القيم الافتراضية إذا كانت فارغة
          const cardId = formData.get('card-id') || ''; // تعيين قيمة فارغة إذا كانت غير موجودة
          const usethis = formData.get('use-this') || ''; // تعيين قيمة فارغة إذا كانت غير موجودة

          // تحديث FormData بالقيم
          formData.set('card-id', cardId);
          formData.set('use-this', usethis);

          // إرسال البيانات باستخدام fetch
          fetch('/orders/create-order/', {  
              method: 'POST',
              body: formData,
              headers: {
                  'X-CSRFToken': getCookie('csrftoken') // تمرير CSRF token
              }
          })
          .then(response => response.json()) // تحويل الرد إلى JSON
          .then(data => {
              if (data.success) {
                  showMenu();
                  setTimeout(function() {
                    location.reload(); // تحديث الصفحة بعد 3 ثوانٍ
                  }, 3000); 
              } else {
                  alert(data.error || 'حدث خطأ ما');
              }
          })
          .catch(error => {
              console.error('Error:', error); // عرض أي أخطاء أخرى
              alert('حدث خطأ أثناء إرسال البيانات');
          });
      });
  }
  if (menu && link) { // تحقق من وجود العنصرين قبل إضافة الأحداث
    
    let hideTimeout; // متغير لتخزين مؤقت الإخفاء
    function showMenu() {
          menu.style.display = 'block'; // عرض القائمة
          setTimeout(() => {
              menu.style.visibility = 'visible';
              menu.style.opacity = '1';
              menu.style.transform = 'translate(-50%, -40%) scale(1)';
          }, 10);
  
          // إعداد مؤقت للإخفاء بعد 3 ثوانٍ من ظهور القائمة
          clearTimeout(hideTimeout);
          hideTimeout = setTimeout(hideMenu, 3000);
    }
    function hideMenu() {
          menu.style.opacity = '0';
          menu.style.transform = 'translate(-50%, -40%) scale(0.5)';
          setTimeout(() => {
              menu.style.visibility = 'hidden';
              menu.style.display = 'none';
          }, 300);
    }
    document.addEventListener('click', function (e) {
        if (menu.style.visibility === 'visible' && !menu.contains(e.target) && !link.contains(e.target)) {
            hideMenu();
        }
    });
  }
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
//  دالة الغاء الطلب 
document.addEventListener('DOMContentLoaded', function () {
  const cancelForm = document.getElementById('cancel-order-form');
  const cancelInput = document.getElementById('cancel-order-id');
  const cancelButton = document.querySelector('.cancel-order');

  if (cancelForm && cancelButton) {
      cancelButton.addEventListener('click', function (e) {
          e.preventDefault(); // منع إعادة تحميل الصفحة

          const cancelOrderId = cancelInput.value;

          if (cancelOrderId) {
              fetch('/orders/cancel-order/', {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json',
                      'X-CSRFToken': getCookie('csrftoken') // الحصول على CSRF Token
                  },
                  body: JSON.stringify({
                    order_id: cancelOrderId 
                    })
              })
              .then(response => response.json())
              .then(data => {
                  if (data.success) {
                      // التعامل مع النجاح، مثل إخفاء النافذة وتحديث الصفحة
                      alert('تم إلغاء الطلب بنجاح');
                      location.reload(); // إعادة تحميل الصفحة لتحديث البيانات
                  } else {
                      alert( data.error || 'فشل إلغاء الطلب، يرجى المحاولة لاحقًا.');
                      location.reload();
                  }
              })
              .catch(error => {
                  console.error('حدث خطأ:', error);
              });
          }
      });
  }
});
// =============================================================================================
// دالة حذف عنصر من عناصر الطلب
document.addEventListener('DOMContentLoaded', function () {
  const removeIcons = document.querySelectorAll('.remove-clicable');

  if (removeIcons.length > 0) {
    removeIcons.forEach(icon => {
      icon.addEventListener('click', function () {
          // الحصول على العنصر الأب الذي يحتوي على البيانات
          const parentElement = this.closest('.remove');
          const removeId = parentElement.getAttribute('data-remove-id');
          const orderId = parentElement.getAttribute('data-order-id');

          // تأكيد أن هناك بيانات مطلوبة
          if (removeId && orderId) {
              // إرسال البيانات إلى دالة بايثون باستخدام fetch
              fetch('/orders/remove-order-item/', {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json',
                      'X-CSRFToken': getCookie('csrftoken') // تضمين CSRFToken إذا كان مطلوبًا
                  },
                  body: JSON.stringify({
                      remove_id: removeId,
                      order_id: orderId
                  })
              })
              .then(response => response.json())
              .then(data => {
                  if (data.success) {
                      alert(data.message);
                      location.reload();                      
                  } else {
                      alert(data.error);
                  }
              })
              .catch(error => {
                  console.error('حدث خطأ:', error);
              });
          }
      });
    });
  }
});
// =============================================================================================
// دالة تأخذ معرف العنصر المراد استبداله وترسله الى الفورم لكي يتم ارساله الى دالة المعالجة
document.addEventListener('DOMContentLoaded', function() {
  // حدد جميع العناصر التي تحتوي على الكلاس replace-clicable
  const clickableElements = document.querySelectorAll('.replace-clicable');

  // أضف مستمع للنقر على كل عنصر
  clickableElements.forEach(function(element) {
      element.addEventListener('click', function() {
          // الحصول على الـ data-item-id من العنصر الأب الذي يحتوي على الكلاس replace
          const itemId = element.closest('.replace').getAttribute('data-item-id');

          // إيجاد الحقل المخفي الذي داخل الفورم class='choose-to-replace'
          const hiddenInput = document.querySelector('.choose-to-replace input[name="replace-product-id"]');
          
          if (hiddenInput) {
              // نسخ الـ itemId إلى الحقل المخفي
              hiddenInput.value = itemId;
          }
      });
  });
});
// =============================================================================================
// دوال تعديل الطلب من قائمة الطلبات السابقة
document.addEventListener('DOMContentLoaded', function () {
  const deleteMenu = document.querySelector('.replace-menu');
  const deleteLinks = document.querySelectorAll('.replace-clicable'); // الحصول على جميع العناصر التي تحتوي على الكلاس
  const submitButton = document.querySelector('.hide-replace-link'); // تحديد زر "استعمال"

  // دالة لعرض النافذة المنبثقة
  function showDeleteMenu() {
    deleteMenu.style.display = 'block';
    setTimeout(() => {
      deleteMenu.style.visibility = 'visible';
      deleteMenu.style.opacity = '1';
      deleteMenu.style.transform = 'translate(-50%, -50%) scale(1)';
    }, 10);
  }
  // دالة لإخفاء النافذة المنبثقة
  function hideDeleteMenu() {
    deleteMenu.style.opacity = '0';
    deleteMenu.style.transform = 'translate(-50%, -50%) scale(0.5)';
    setTimeout(() => {
      deleteMenu.style.visibility = 'hidden';
      deleteMenu.style.display = 'none';
    }, 300);
  }

  // إضافة حدث النقر لكل عنصر من عناصر .replace-clicable
  deleteLinks.forEach(function (deleteLink) {
    deleteLink.addEventListener('click', function (e) {
      e.preventDefault();
      showDeleteMenu();

      // هنا نحدد العناصر الخاصة بالفورم بعد عرض النافذة
      const form = document.querySelector('.choose-to-replace'); // تحديد الفورم بعد النقر
      const hiddenInput = form.querySelector('input[name="replace-product-id"]');
      const orderId = form.querySelector('input[name="order-id"]');
      const radioInputs = form.querySelectorAll('input[name="replace-product"]');

      // تحقق من وجود العناصر
      if (form && hiddenInput && radioInputs.length > 0 && orderId) {

        // دالة لعمل طلب Fetch وإرسال البيانات
        function submitReplaceForm() {
          // الحصول على الـ ID المختار من الراديو
          const selectedRadio = form.querySelector('input[name="replace-product"]:checked');

          if (selectedRadio) {
            const orderIdValue = orderId.value;
            const replaceProductId = hiddenInput.value;
            const selectedProductId = selectedRadio.value;

            // إعداد البيانات التي سيتم إرسالها
            const formData = new FormData();
            formData.append('order_id', orderIdValue);
            formData.append('replace_product_id', replaceProductId);
            formData.append('selected_product_id', selectedProductId);

            // إرسال البيانات باستخدام fetch
            fetch('/orders/edit-order/', {
              method: 'POST',
              body: formData,
              headers: {
                'X-CSRFToken': getCookie('csrftoken') // تأكد من تضمين CSRF token إذا كنت بحاجة إليه
              },
            })
              .then(response => response.json()) // تحويل الاستجابة إلى JSON
              .then(data => {
                if (data.success) {
                  alert(data.success.message || 'تمت عملية الاستبدال بنجاح');
                  hideDeleteMenu();
                  setTimeout(function() {
                    location.reload(); // تحديث الصفحة بعد 3 ثوانٍ
                  }, 1000); 
                } else {
                  alert(data.error || 'حدث خطأ ما');
                }
              })
              .catch(error => {
                console.error('Error:', error); // عرض أي أخطاء أخرى
                alert('حدث خطأ أثناء إرسال البيانات');
              });
          } else {
            alert('يرجى اختيار احد المنتجات لإجراء عملية الاستبدال');
          }
        }

        // إضافة حدث النقر على زر "استعمال" فقط
        submitButton.addEventListener('click', function (e) {
          e.preventDefault(); // منع الإرسال الافتراضي للفورم
          submitReplaceForm(); // تنفيذ دالة الإرسال باستخدام fetch
        });
      }
    });
  });

  // إخفاء النافذة عند النقر خارجها
  document.addEventListener('click', function (e) {
    if (deleteMenu){
      if (deleteMenu.style.visibility === 'visible' && !deleteMenu.contains(e.target)) {
        hideDeleteMenu();
      }
    }
  });
});
// =============================================================================================
// إخفاء رسائل الخطأ أو النجاح بعد تحميل الصفحة في صفحات الحساب
document.addEventListener('DOMContentLoaded', function() {
  setTimeout(function() {
      const errorMessages = document.querySelectorAll('.error-messages');
      // إخفاء الرسائل الإضافية إذا كانت أكثر من 2
      if (errorMessages.length > 2) {
          errorMessages.forEach(function(message, index) {
              if (index >= 2) {
                  message.style.display = 'none';
              }
          });
      }
      // إخفاء الرسائل بعد 4 ثوانٍ
      setTimeout(function() {
          errorMessages.forEach(function(message) {
              message.style.display = 'none';
          });
      }, 4000);
  });
});
// =============================================================================================
// =============================================================================================

