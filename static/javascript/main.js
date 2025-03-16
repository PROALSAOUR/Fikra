window.addEventListener("load", function() {
    document.getElementById("loader").style.display = "none";
});
// ============================================================================
document.addEventListener('DOMContentLoaded', function() {  
    const images = document.querySelectorAll(".lazy-load");
    images.forEach(img => {
    const tempImg = new Image();
    tempImg.src = img.getAttribute("data-src");
    tempImg.onload = function () {
        img.src = tempImg.src; // استبدال الصورة الافتراضية بالأصلية
        img.nextElementSibling.remove(); // إزالة التأثير عند تحميل الصورة
    };
    });
});
// ============================================================================
const toggle = document.getElementById('them');
const body = document.body;
if (toggle && body) {
    // تحقق من وجود الكلاس في localStorage واضف الكلاس إلى body إذا كان موجودًا
    if (localStorage.getItem('them') === 'light') {
        body.classList.add('light-them');
        toggle.checked = true; // لا حاجة لفحص toggle هنا لأننا تحققنا مسبقًا
    }

    // حدث عند تغيير حالة التشيك بوكس
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
// ============================================================================
// قائمة الميقا منيو
document.addEventListener('DOMContentLoaded', function() {
    const body = document.body;
    const sideMenu = document.querySelector('.mega-menu');
    const sideMenuCheckbox = document.getElementById('side-menu');
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
});
// ========================================================================================================
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
// الدالة المسؤلة عن اعادة المستخدم الى الصفحة التي جاء منها 
function goBack() {
    window.history.back();
}
// =========================================================================================================
// إخفاء رسائل الخطأ أو النجاح بعد تحميل الصفحة
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
// دالة اضافة المنتج و ازالته من المفضلة
document.addEventListener('DOMContentLoaded', function() {
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
          localStorage.setItem('isFlipped', isCurrentlyFlipped.toString());
          console.log(isCurrentlyFlipped);
        });
      });
    }
});
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