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
  const popup = document.getElementById('confirm-return-popup');
  const cancelBtn = document.getElementById('cancel-return-btn');
  const confirmBtn = document.getElementById('confirm-return-btn');
  // متغيرات لتخزين البيانات مؤقتاً
  let currentRemoveId = null;
  let currentOrderId = null;
  // دالة إظهار النافذة بشكل سلس
  function showPopup() {
    popup.style.display = 'block';
    setTimeout(() => {
      popup.style.visibility = 'visible';
      popup.style.opacity = '1';
      popup.style.transform = 'translate(-50%, -50%) scale(1)';
    }, 10);
  }
  function hidePopup() {
    popup.style.opacity = '0';
    popup.style.transform = 'translate(-50%, -50%) scale(0.5)';
    setTimeout(() => {
      popup.style.visibility = 'hidden';
      popup.style.display = 'none';
    }, 300);
  }
  if (removeIcons.length > 0 && popup && cancelBtn && confirmBtn ) {
      removeIcons.forEach(icon => {
          icon.addEventListener('click', function () {
              const parentElement = this.closest('.remove');
              const removeId = parentElement.getAttribute('data-remove-id');
              const orderId = parentElement.getAttribute('data-order-id');
              if (removeId && orderId) {
                  // حفظ القيم مؤقتاً
                  currentRemoveId = removeId;
                  currentOrderId = orderId;                
                  // إظهار النافذة
                  showPopup();
              }
          });
      });
  }

  if (cancelBtn) {
    // زر التراجع
    cancelBtn.addEventListener('click', function () {
      hidePopup();
      currentRemoveId = null;
      currentOrderId = null;
    });
  }
  // زر تأكيد الحذف
  confirmBtn.addEventListener('click', function () {
      if (currentRemoveId && currentOrderId) {
          fetch('/orders/remove-order-item/', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
                  'X-CSRFToken': getCookie('csrftoken')
              },
              body: JSON.stringify({
                  remove_id: currentRemoveId,
                  order_id: currentOrderId
              })
          })
          .then(response => response.json())
          .then(data => {
              hidePopup();
              if (data.success) {
                  alert(data.message);
                  location.reload();
              } else {
                  alert(data.error);
              }
          })
          .catch(error => {
              console.error('حدث خطأ:', error);
              hidePopup();
          });
      }
  });

  // إخفاء النافذة عند النقر خارجها
  document.addEventListener('click', function (e) {
      if (popup.style.visibility === 'visible' &&
          !popup.contains(e.target) &&
          ![...removeIcons].some(icon => icon.contains(e.target))) {
          hidePopup();
          currentRemoveId = null;
          currentOrderId = null;
      }
  });
  
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
