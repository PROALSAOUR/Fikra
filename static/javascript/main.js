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
//  دالة اظهار الفورم واخفاءه داخل صفحة تفاصيل البطاقات
document.addEventListener('DOMContentLoaded', function() {
  const forMeRadio = document.getElementById('for-me');
  const forAnotherRadio = document.getElementById('for-another');
  const buyAsGiftForm = document.querySelector('.buy-as-gift');
  const sendMessageCheckbox = document.getElementById('send-message');
  const messageDetails = document.querySelector('.message-details');

  // التحقق من وجود العناصر
  if (forMeRadio && forAnotherRadio && buyAsGiftForm && sendMessageCheckbox && messageDetails) {

      // وظيفة لتحديث عرض الفورم بناءً على اختيار الراديو
      function updateFormVisibility() {
          if (forMeRadio.checked) {
              buyAsGiftForm.classList.add('dont-show'); // إضافة كلاس dont-show إذا كان for-me مختارًا
          } else if (forAnotherRadio.checked) {
              buyAsGiftForm.classList.remove('dont-show'); // إزالة كلاس dont-show إذا كان for-another مختارًا
          }
      }

      // وظيفة لتحديث عرض تفاصيل الرسالة بناءً على اختيار "إرسال رسالة"
      function updateMessageDetailsVisibility() {
          if (sendMessageCheckbox.checked) {
              messageDetails.classList.remove('dont-show'); // إزالة كلاس dont-show إذا كان send-message مختارًا
          } else {
              messageDetails.classList.add('dont-show'); // إضافة كلاس dont-show إذا لم يكن send-message مختارًا
          }
      }

      // إضافة مستمع للأحداث على مربعات الراديو
      forMeRadio.addEventListener('change', updateFormVisibility);
      forAnotherRadio.addEventListener('change', updateFormVisibility);

      // إضافة مستمع للأحداث على checkbox الخاص بإرسال الرسالة
      sendMessageCheckbox.addEventListener('change', updateMessageDetailsVisibility);

      // استدعاء الوظائف عند تحميل الصفحة للتأكد من حالة العناصر
      updateFormVisibility();
      updateMessageDetailsVisibility();
  }
});
//  =========================================================================================================
// الكود الخاص  بتبديل العرض  بين الكوبونات والهدايا في صفحة اختيار كوبون لاستعماله
document.addEventListener('DOMContentLoaded', function () {
  const giftCardsRadio = document.getElementById('gift-cards');
  const coponCardsRadio = document.getElementById('copon-cards');
  const giftForm = document.getElementById('gift-form');
  const coponsForm = document.getElementById('copons-form');

  // التحقق من وجود جميع العناصر قبل المتابعة
  if (giftCardsRadio && coponCardsRadio && giftForm && coponsForm) {
      // التحقق من حالة الراديو وتعيين الكلاس المناسب
      function checkRadioSelection() {
          if (giftCardsRadio.checked) {
              giftForm.classList.remove('dont-show');
              coponsForm.classList.add('dont-show');
          } else if (coponCardsRadio.checked) {
              coponsForm.classList.remove('dont-show');
              giftForm.classList.add('dont-show');
          }
      }

      // استدعاء الدالة عند تغيير الاختيار
      giftCardsRadio.addEventListener('change', checkRadioSelection);
      coponCardsRadio.addEventListener('change', checkRadioSelection);

      // استدعاء الدالة في البداية للتحقق من الحالة الأولية
      checkRadioSelection();
  } 
});
//  =========================================================================================================
// دالة شراء هدية من صفحة التفاصيل
document.addEventListener('DOMContentLoaded', function () {

  const buyDoneLink = document.querySelector('.buy-done-link');
  const giftIdElement = document.querySelector('#gift-id'); // تحقق من وجود العنصر

  if (!giftIdElement || !giftIdElement.value) {
    return;
  }

  const giftId = giftIdElement.value; // الحصول على قيمة gift-id

  if (buyDoneLink) {
    buyDoneLink.addEventListener('click', function(event) {
      event.preventDefault(); // منع إعادة تحميل الصفحة

      let selectedOption = document.querySelector('input[name="buy-for"]:checked'); // جلب الخيار المحدد عند النقر
      let buy_for = selectedOption ? selectedOption.id : '';

      if (buy_for === 'for-me') {
        fetch(`/cards/buy-gift/${giftId}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // احصل على الـ CSRF token
          },
          body: JSON.stringify({
            buy_for: 'for-me',
          })
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            showBuyDoneMenu();
            // هنا يمكن تنفيذ ما تريد بعد نجاح الشراء
          } else {
            alert(data.error);
          }
        })
        .catch(error => console.error('Error:', error));

      } else if (buy_for === 'for-another') {
        const recipientName = document.querySelector('#recipient-name')?.value || '';
        const recipientPhone = document.querySelector('#recipient-phone')?.value || '';
        const sendMessage = document.querySelector('#send-message')?.checked || false;
        const messageContent = document.querySelector('#content')?.value || '';

        // التحقق من الحقول
        if (recipientName === '') {
          alert('اسم المستلم مطلوب');
          return;
        }

        if (recipientPhone === '') {
          alert('رقم هاتف المستلم مطلوب');
          return;
        }

        if (sendMessage && messageContent === '') {
          alert('محتوى الرسالة مطلوب عند تحديد خيار إرسال رسالة');
          return;
        }

        fetch(`/cards/buy-gift/${giftId}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // احصل على الـ CSRF token
          },
          body: JSON.stringify({
            buy_for: 'for-another',
            recipient_name: recipientName,
            recipient_phone: recipientPhone,
            send_message: sendMessage,
            message_content: messageContent,
          })
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            showBuyDoneMenu();
          } else {
            alert(data.error || 'حدث خطأ ما');
          }
        })
        .catch(error => console.error('Error:', error));
      }
    });
  }

  let hideTimeout;

  function showBuyDoneMenu() {
    const menu = document.querySelector('.buy-done-pop-page');
     

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
      const menu = document.querySelector('.buy-done-pop-page');
     

      menu.style.opacity = '0';
      menu.style.transform = 'translate(-50%, -40%) scale(0.5)';
      setTimeout(() => {
          menu.style.visibility = 'hidden';
          menu.style.display = 'none';
      }, 300);

      location.reload();
  }

});
//  =========================================================================================================
// دالة شراء هدية من البطاقة الخارجية
document.addEventListener('DOMContentLoaded', function() {
  // الكود الخاص بإظهار نافذة ادخال البيانات عند شراء الهدية
  const menu = document.querySelector('.pop-gift-details');
  const links = document.querySelectorAll('.pop-gift-details-link'); // استخدام querySelectorAll لجلب جميع العناصر

  if (menu && links.length > 0) { // تحقق من وجود القائمة والروابط
      function showMenu() {
          menu.style.display = 'block'; // عرض القائمة
          setTimeout(() => {
              menu.style.visibility = 'visible';
              menu.style.opacity = '1';
              menu.style.transform = 'translate(-50%, -40%) scale(1)';
          }, 10);
      }

      function hideMenu() {
          menu.style.opacity = '0';
          menu.style.transform = 'translate(-50%, -40%) scale(0.5)';
          setTimeout(() => {
              menu.style.visibility = 'hidden';
              menu.style.display = 'none';
          }, 300);
      }

      // إضافة حدث النقر لكل رابط
      links.forEach(link => {
          link.addEventListener('click', function (e) {
              e.preventDefault();
              if (menu.style.visibility === 'hidden' || menu.style.visibility === '') {
                  showMenu();
              }
          });
      });

      document.addEventListener('click', function (e) {
          if (menu.style.visibility === 'visible' && !menu.contains(e.target) && !Array.from(links).some(link => link.contains(e.target))) {
              hideMenu();
          }
      });
  }
 
  let giftId = '';  // متغير لتخزين giftId
  // إضافة حدث النقر لكل عنصر هدية
  const giftLinks = document.querySelectorAll('.pop-gift-details-link');

  if (giftLinks) {
    giftLinks.forEach(link => {
      link.addEventListener('click', function(event) {
          // سحب البيانات من العنصر الذي تم النقر عليه
          giftId = this.getAttribute('data-gift-id'); // الحصول على giftId من العنصر
      });
    });
  } else  {
    return;
  }

  const buyLink =document.querySelector('.submit-gift-form')
  if (buyLink) {
    buyLink.addEventListener('click', function(event) {
        event.preventDefault();
        const giftForm = document.getElementById('get-data-from-me');

        if (giftForm) {
            // عند الضغط على رابط شراء الهدية، يجب استدعاء وظيفة تقديم النموذج
            handleFormSubmit();
        }
    });
  }

  function handleFormSubmit() {
      // الحصول على بيانات النموذج
      const recipientName = document.getElementById('recipient-name').value;
      const recipientPhone = document.getElementById('recipient-phone').value;
      const messageContent = document.querySelector('#content')?.value || '';

      // التحقق من وجود جميع البيانات
      if (recipientName && recipientPhone && giftId) {
          // إجراء طلب AJAX
          fetch(`/cards/buy-gift2/${giftId}`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': getCookie('csrftoken')  // احصل على الـ CSRF token
            },
              body: JSON.stringify({
                recipient_name: recipientName,
                recipient_phone: recipientPhone,
                message_content: messageContent,
              })
          })
          .then(response => response.json())
        .then(data => {
          if (data.success) {
            hideMenu();
            showBuyDoneMenu();
            // هنا يمكن تنفيذ ما تريد بعد نجاح الشراء
          } else {
            alert(data.error);
          }
        })
        .catch(error => console.error('Error:', error));
      } else {
          alert('يرجى ملء جميع الحقول.');
      }
  }

  let hideTimeout;

  function showBuyDoneMenu() {
    const menu = document.querySelector('.buy-done-pop-page');
     

    menu.style.display = 'block';
    setTimeout(() => {
        menu.style.visibility = 'visible';
        menu.style.opacity = '1';
        menu.style.transform = 'translate(-50%, -40%) scale(1)';
    }, 10);

    clearTimeout(hideTimeout);
    hideTimeout = setTimeout(hideBuyDoneMenu, 3000);
  }

  function hideBuyDoneMenu() {
      const menu = document.querySelector('.buy-done-pop-page');
     

      menu.style.opacity = '0';
      menu.style.transform = 'translate(-50%, -40%) scale(0.5)';
      setTimeout(() => {
          menu.style.visibility = 'hidden';
          menu.style.display = 'none';
      }, 300);

      location.reload();
  }

});
//  =========================================================================================================
// الكود الخاص  بتبديل العرض  بين الكوبونات والهدايا في مستودع المستخدم
document.addEventListener("DOMContentLoaded", function () {
  // دوال مساعدة لحفظ واسترجاع حالة الاختيار من التخزين المحلي
  function saveSelectedOption(value) {
      localStorage.setItem("selectedRepo", value);
  }

  function getSelectedOption() {
      return localStorage.getItem("selectedRepo");
  }

  // التحقق من وجود div الذي يحتوي على مربعات الراديو
  const repoTitleDiv = document.querySelector('.repo-title');
  const giftCardsDivs = document.querySelectorAll('.gift-cards');  // جميع عناصر gift-cards
  const coponsCardsDivs = document.querySelectorAll('.copons-cards'); // جميع عناصر copons-cards
  
  if (repoTitleDiv && giftCardsDivs.length > 0 && coponsCardsDivs.length > 0) {
      // مربعات الاختيار
      const giftsPageRadio = document.getElementById("gifts-page");
      const coponsPageRadio = document.getElementById("copons-page");

      // labels المرتبطة بمربعات الاختيار
      const giftsPageLabel = document.querySelector('label[for="gifts-page"]');
      const coponsPageLabel = document.querySelector('label[for="copons-page"]');

      // التحقق من وجود مربعات الاختيار والـ labels
      if (giftsPageRadio && coponsPageRadio && giftsPageLabel && coponsPageLabel) {
          // استرجاع الحالة المحفوظة أو تعيين الخيار الافتراضي
          const savedOption = getSelectedOption();
          
          if (savedOption) {
              document.getElementById(savedOption).checked = true;
          } else {
              giftsPageRadio.checked = true; // جعل الخيار الأول افتراضي
              saveSelectedOption("gifts-page");
          }

          // تحديث العرض بناءً على الحالة المحفوظة أو الاختيار الافتراضي
          updateVisibility();
          updateActiveClass();

          // إضافة مستمع للأحداث لتغيير العرض بناءً على الاختيار
          giftsPageRadio.addEventListener("change", function () {
              if (this.checked) {
                  saveSelectedOption("gifts-page");
                  updateVisibility();
                  updateActiveClass();
              }
          });

          coponsPageRadio.addEventListener("change", function () {
              if (this.checked) {
                  saveSelectedOption("copons-page");
                  updateVisibility();
                  updateActiveClass();
              }
          });

          // دالة لتحديث عرض العناصر
          function updateVisibility() {
              if (giftsPageRadio.checked) {
                  coponsCardsDivs.forEach(function (div) {
                      div.classList.add("dont-show");
                  });
                  giftCardsDivs.forEach(function (div) {
                      div.classList.remove("dont-show");
                  });
              } else if (coponsPageRadio.checked) {
                  giftCardsDivs.forEach(function (div) {
                      div.classList.add("dont-show");
                  });
                  coponsCardsDivs.forEach(function (div) {
                      div.classList.remove("dont-show");
                  });
              }
          }

          // دالة لإضافة كلاس active إلى الـ label المرتبط بالخيار المحدد
          function updateActiveClass() {
              if (giftsPageRadio.checked) {
                  giftsPageLabel.classList.add("active");
                  coponsPageLabel.classList.remove("active");
              } else if (coponsPageRadio.checked) {
                  coponsPageLabel.classList.add("active");
                  giftsPageLabel.classList.remove("active");
              }
          }
      }
  }
});
//  =========================================================================================================
// دالة عرض الهدايا بأنواعها داخل المستودع
document.addEventListener('DOMContentLoaded', function () {
  // الحصول على جميع مربعات الاختيار
  const checkboxes = document.querySelectorAll('.repo-inputs-cont input[type="checkbox"]');

  if (checkboxes.length > 0) {
      // دالة التحقق من حالة مربعات الاختيار
      checkboxes.forEach(function (checkbox) {
        checkbox.addEventListener('change', function () {
            const divClass = this.id; // الحصول على معرف مربع الاختيار
            const targetDiv = document.querySelector(`.products-cards.${divClass}`); // البحث عن القسم المرتبط
            const icon = this.closest('label').querySelector('i'); // العثور على الأيقونة داخل الـ label
            const hr = this.closest('label').querySelector('hr');

            if (this.checked) {
                targetDiv.classList.remove('hidden'); // إزالة الكلاس hidden إذا كان مربع الاختيار مختارًا
                icon.classList.remove('fa-caret-down'); // إزالة الكلاس fa-caret-down
                icon.classList.add('fa-caret-up'); // إضافة الكلاس fa-caret-up
                hr.classList.add('hidden');
              } else {
                targetDiv.classList.add('hidden'); // إضافة الكلاس hidden إذا كان مربع الاختيار غير مختار
                icon.classList.remove('fa-caret-up'); // إزالة الكلاس fa-caret-up
                icon.classList.add('fa-caret-down'); // إضافة الكلاس fa-caret-down
                hr.classList.remove('hidden');
              }
        });
    });
  }

});
//  =========================================================================================================
// انشاء تأثير قلب وإظهار بطاقة الهدية المنبثقة 
document.addEventListener('DOMContentLoaded', function() {
  const surpriseButtons = document.querySelectorAll('.clik-to-surprise');

  surpriseButtons.forEach(button => {
      button.addEventListener('click', function() {
          const relatedGiftId = this.dataset.relatedGift;
          const giftCard = document.querySelector(`.gift-card[data-related-gift="${relatedGiftId}"]`);

          // إذا كانت البطاقة موجودة، قم بإزالة كلاس hidden
          if (giftCard) {
              giftCard.classList.remove('hidden');
              
              // إضافة تأثير دوران البطاقة
              const face = giftCard.querySelector('.card-body');
              const flipButton = giftCard.querySelector('.flip');
              const content = giftCard.querySelector('.back .content');
              const exitButton = giftCard.querySelector('#exit');

              // التعامل مع قلب البطاقة
              if (flipButton && face && content) {
                  flipButton.addEventListener('click', function() {
                      face.classList.add('rotate');
                  });

                  content.addEventListener('click', function() {
                      face.classList.remove('rotate');
                  });
              }

              // إغلاق البطاقة عند النقر على زر الخروج
              if (exitButton) {
                  exitButton.addEventListener('click', function() {
                      giftCard.classList.add('hidden'); // إعادة إضافة كلاس hidden
                  });
              }

              // إغلاق البطاقة عند النقر خارجها
              document.addEventListener('click', function(event) {
                  if (!giftCard.contains(event.target) && !button.contains(event.target)) {
                      giftCard.classList.add('hidden'); // إعادة إضافة كلاس hidden
                  }
              });
          }
      });
  });
});
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
                      hideShareCodeMenu();
                      location.reload();
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



