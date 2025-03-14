document.addEventListener('DOMContentLoaded', () => {
    const filterForm = document.getElementById('filter-form');
    const filterToggle = document.querySelector('.filter-toggle');
    const filterOptions = document.querySelector('.filter-options');
    const closeFilter = document.querySelector('.close-filter');
    const filterTabs = document.querySelectorAll('.filter-tab');
    const filterGroups = document.querySelectorAll('.filter-group');

    if (filterToggle && filterOptions && closeFilter) {
        filterToggle.addEventListener('click', () => {
            filterOptions.classList.toggle('visible');
        });

        closeFilter.addEventListener('click', () => {
            filterOptions.classList.remove('visible');
        });
    }

    if (filterForm) {
        filterForm.addEventListener('submit', (event) => {
            event.preventDefault();

            const inputs = filterForm.querySelectorAll('input, select');
            const queryParams = new URLSearchParams();

            inputs.forEach(input => {
                if (input.value.trim() !== '') {
                    queryParams.append(input.name, input.value);
                }
            });

            window.location.search = queryParams.toString();
        });
    }

    if (filterTabs.length) {
        filterTabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const target = tab.getAttribute('data-target');
                
                filterGroups.forEach(group => {
                    if (group.id === target) {
                        group.classList.add('visible');
                    } else {
                        group.classList.remove('visible');
                    }
                });
            });
        });
    }
    
    let typingTimer;
    const doneTypingInterval = 500;
    const searchInput = document.getElementById('search-query');

    if (searchInput) {
        searchInput.addEventListener('input', (event) => {
            clearTimeout(typingTimer);
            typingTimer = setTimeout(() => {
                const query = event.target.value.trim();
                if (query.length > 0) {
                    filterForm.submit();
                }
            }, doneTypingInterval);
        });

        // لإعادة تعيين قيمة البحث بعد تحميل الصفحة
        const queryParams = new URLSearchParams(window.location.search);
        const searchQuery = queryParams.get('q');
        if (searchQuery) {
            searchInput.value = searchQuery;
        }
    }
});
// =========================================================================================================
//  دالة زر إلغاء الفلترة
function resetFilters() {
   // إعادة تعيين حقول الإدخال
   const q = document.getElementById('search-query');
   const min = document.getElementById('price_min');
   const max = document.getElementById('price_max');
   const category = document.getElementById('category_filter');
   const brand = document.getElementById('brand_filter'); 

   if (q) {
    q.value = '';
   }
   if (min) {
    min.value = '';
   }
   if (max) {
    max.value = '';
   }
   if (category) {
    category.selectedIndex = 0;
   }
   if (brand) {
    brand.selectedIndex = 0;
   }

}
// =========================================================================================================
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
