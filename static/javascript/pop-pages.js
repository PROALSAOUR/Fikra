// الكود الخاص بإظهار صفحة تسجيل الخروج 
document.addEventListener('DOMContentLoaded', function () {
    const signOutMenu = document.querySelector('.sign-out');
    const logoutLink = document.querySelector('.account-menu .fa-arrow-right-from-bracket')?.closest('a');
    const backButton = document.querySelector('.sign-out .back');
    const outButton = document.querySelector('.sign-out .out');

    // التحقق من وجود العناصر قبل إضافة الأحداث
    if (signOutMenu && logoutLink && backButton && outButton) {

        function showSignOutMenu() {
            signOutMenu.style.display = 'block'; // يعرض العنصر
            setTimeout(() => {
                signOutMenu.style.visibility = 'visible'; // يجعل العنصر مرئيًا
                signOutMenu.style.opacity = '1'; // يضبط الشفافية لتظهر بشكل كامل
                signOutMenu.style.transform = 'translate(-50%, -50%) scale(1)'; // يضبط الحجم ليصل للحجم الطبيعي
            }, 10); // التأخير لتطبيق التحول بشكل صحيح
        }

        function hideSignOutMenu() {
            signOutMenu.style.opacity = '0'; // يضبط الشفافية لتختفي
            signOutMenu.style.transform = 'translate(-50%, -50%) scale(0.5)'; // يصغر الحجم مرة أخرى
            setTimeout(() => {
                signOutMenu.style.visibility = 'hidden'; // يخفي العنصر
                signOutMenu.style.display = 'none'; // يزيل العنصر من التدفق الطبيعي للصفحة
            }, 300); // يجب أن يتطابق مع مدة الـ transition في CSS
        }

        logoutLink.addEventListener('click', function (e) {
            e.preventDefault();
            if (signOutMenu.style.visibility === 'hidden' || signOutMenu.style.visibility === '') {
                showSignOutMenu();
            }
        });

        backButton.addEventListener('click', hideSignOutMenu);
        outButton.addEventListener('click', hideSignOutMenu);

        document.addEventListener('click', function (e) {
            if (signOutMenu.style.visibility === 'visible' && !signOutMenu.contains(e.target) && !logoutLink.contains(e.target)) {
                hideSignOutMenu();
            }
        });
    }
});
// ===================================================================================================
// الكود الخاص بإظهار صفحة حذف الحساب
document.addEventListener('DOMContentLoaded', function () {
    const deleteMenu = document.querySelector('.delete-account');
    const deleteLink = document.querySelector('.show-delete-menu');
    const backButton = document.querySelector('.delete-account .back');
    const outButton = document.querySelector('.delete-account .delete');

    // تحقق من وجود العناصر
    if (deleteMenu && deleteLink && backButton && outButton) {

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

        // دالة لحذف الحساب
        function deleteAccount() {
            const deleteAccountUrl = window.deleteAccountUrl;  // استخدم الرابط من تاق script
            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

            fetch(deleteAccountUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                if (response.ok) {
                    window.location.href = "/";  // إعادة التوجيه مباشرة بعد الحذف
                } else {
                    console.error('حدث خطأ أثناء محاولة حذف الحساب.');
                }
            })
            .catch(error => {
                console.error('حدث خطأ:', error);
            });
        }

        // عرض النافذة المنبثقة
        deleteLink.addEventListener('click', function (e) {
            e.preventDefault();
            showDeleteMenu();
        });

        // إخفاء النافذة عند التراجع
        backButton.addEventListener('click', hideDeleteMenu);

        // تنفيذ الحذف عند النقر على زر "حذف حسابي"
        outButton.addEventListener('click', function() {
            hideDeleteMenu();
            setTimeout(deleteAccount, 300);  // تنفيذ الحذف بعد إخفاء القائمة
        });

        // إخفاء النافذة عند النقر خارجها
        document.addEventListener('click', function (e) {
            if (deleteMenu.style.visibility === 'visible' && !deleteMenu.contains(e.target) && !deleteLink.contains(e.target)) {
                hideDeleteMenu();
            }
        });
    }
});
// ===================================================================================================
// الكود الخاص بصفحة التحقق من رقم الهاتف
document.addEventListener('DOMContentLoaded', function () {
    const verifMenu = document.querySelector('.verif-code');
    const verifLinks = document.querySelectorAll('.verif-link');
    const verifButtons = document.querySelectorAll('.verif-code .try-code');

    function showVerifMenu() {
        verifMenu.style.display = 'block';
        setTimeout(() => {
            verifMenu.style.visibility = 'visible';
            verifMenu.style.opacity = '1';
            verifMenu.style.transform = 'translate(-50%, -50%) scale(1)';
        }, 10);
    }

    function hideVerifMenu() {
        verifMenu.style.opacity = '0';
        verifMenu.style.transform = 'translate(-50%, -50%) scale(0.5)';
        setTimeout(() => {
            verifMenu.style.visibility = 'hidden';
            verifMenu.style.display = 'none';
        }, 300);
    }

    if (verifMenu && verifLinks.length > 0 && verifButtons.length > 0) {
        verifLinks.forEach(link => {
            link.addEventListener('click', function (e) {
                e.preventDefault();
                if (verifMenu.style.visibility === 'hidden' || verifMenu.style.visibility === '') {
                    showVerifMenu();
                }
            });
        });

        verifButtons.forEach(button => {
            button.addEventListener('click', hideVerifMenu);
        });

        document.addEventListener('click', function (e) {
            if (verifMenu.style.visibility === 'visible' && !verifMenu.contains(e.target) && !Array.from(verifLinks).some(link => link.contains(e.target))) {
                hideVerifMenu();
            }
        });
    }
});
// ===================================================================================================
// إظهار الفاتورة و النافذة الخاصة بإضافة كوبون الى الفاتورة
document.addEventListener('DOMContentLoaded', function () {

    // إظهار الفاتورة
    const showCheckbox = document.querySelector('#show');
    const receipt = document.querySelector('.receipt');
    const confirmButton = document.querySelector('.confirm');

    // الكود الخاص بعرض النافذة الخاصة بإضافة كوبون الى الفاتورة
    const menu = document.querySelector('.add-copon-pop-page');
    const links = document.querySelectorAll('.add-copon-link'); // استخدم querySelectorAll لتحديد جميع الروابط
    const hideButtons = document.querySelectorAll('.hide-copon-link'); // تحديد جميع الأزرار

    if (showCheckbox && receipt && confirmButton) { // تحقق من وجود العناصر قبل إضافة الأحداث
        // وظيفة لتحديث حالة الفاتورة بناءً على عرض الشاشة
        function updateReceiptVisibility() {
            if (window.innerWidth <= 992) {
                // استعادة حالة التشيك بوكس من localStorage عند تحميل الصفحة
                if (localStorage.getItem('showCheckboxState') === 'checked') {
                    showCheckbox.checked = true;
                    receipt.style.display = 'block'; // التأكد من أن الفاتورة تظهر
                } else {
                    showCheckbox.checked = false;
                    receipt.style.display = 'none';
                }
                
                // إضافة حدث تغيير لحالة التشيك بوكس
                showCheckbox.addEventListener('change', function () {
                    if (this.checked) {
                        receipt.style.display = 'block';
                        localStorage.setItem('showCheckboxState', 'checked');
                    } else {
                        receipt.style.display = 'none';
                        localStorage.setItem('showCheckboxState', 'unchecked');
                    }
                });
                
                // إضافة حدث للنقر على زر يحتوي على الكلاس confirm
                confirmButton.addEventListener('click', function () {
                    if (window.innerWidth < 992) { // التحقق من عرض الشاشة
                        showCheckbox.checked = false;
                        receipt.style.display = 'none';
                        localStorage.setItem('showCheckboxState', 'unchecked');
                    }
                });
            } else {
                // إذا كانت الشاشة أكبر من 992px، اجعل الفاتورة تظهر دائمًا
                receipt.style.display = 'block';
                localStorage.removeItem('showCheckboxState'); // إزالة حالة التشيك بوكس من localStorage
            }
        }
        
        // استدعاء الوظيفة عند تحميل الصفحة
        updateReceiptVisibility();
        
        // استدعاء الوظيفة عند تغيير حجم الشاشة
        window.addEventListener('resize', updateReceiptVisibility);
    }

    if (menu && links.length > 0) { // تحقق من وجود القائمة وأن هناك روابط

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

        // إضافة حدث click لجميع الروابط
        links.forEach(function (link) {
            link.addEventListener('click', function (e) {
                e.preventDefault(); // منع تحديث الصفحة
                if (menu.style.visibility === 'hidden' || menu.style.visibility === '') {
                    showMenu();
                }
            });
        });

        // إضافة حدث لإخفاء القائمة عند النقر على الأزرار التي تحمل الكلاس hide-copon-link
        hideButtons.forEach(function (button) {
            button.addEventListener('click', function (e) {
                e.preventDefault(); // منع تحديث الصفحة
                
                hideMenu(); // إخفاء القائمة
                receipt.style.display = 'block'; // إظهار الفاتورة
                showCheckbox.checked = true; // تعيين حالة التشيك بوكس
                localStorage.setItem('showCheckboxState', 'checked'); // تخزين الحالة في localStorage
            });
        });

        // إضافة حدث للنقر خارج القائمة
        document.addEventListener('click', function (e) {
            // تحقق إذا كانت القائمة مخفية
            if (menu.style.visibility === 'hidden' || menu.style.visibility === '') {
                if (window.innerWidth < 992) { // التحقق من عرض الشاشة
                    if (!receipt.contains(e.target) && !showCheckbox.contains(e.target)) {
                        // أغلق الفاتورة إذا كانت مخفية
                        showCheckbox.checked = false;
                        receipt.style.display = 'none';
                        localStorage.setItem('showCheckboxState', 'unchecked');
                    }
                }
            }
        });

        // إضافة حدث للنقر خارج القائمة لإخفائها
        document.addEventListener('click', function (e) {
            if (menu.style.visibility === 'visible') {
                if (!menu.contains(e.target) && !e.target.closest('.add-copon-link')) {
                    hideMenu();
                }
            }
        });

    }
});
// =============================================================================================
// الكود الخاص بعرض النافذة الخاصة بإتمام عملية شراء كوبون بنجاح
document.addEventListener('DOMContentLoaded', function() {
    let hideTimeout;
  
    function showBuyDoneMenu() {
        const menu = document.querySelector('.buy-done-pop-page');
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
        const menu = document.querySelector('.buy-done-pop-page');
        if (!menu) return; // تأكد من وجود القائمة
  
        menu.style.opacity = '0';
        menu.style.transform = 'translate(-50%, -40%) scale(0.5)';
        setTimeout(() => {
            menu.style.visibility = 'hidden';
            menu.style.display = 'none';
        }, 300);

        location.reload();
    }
  
    // تأكد من تحميل jQuery أولاً
    if (window.jQuery) {
        $(document).ready(function() {
            $('.copon-buy-done-link').click(function(e) {
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
                            showBuyDoneMenu(); // عرض النافذة المنبثقة عند النجاح
                        } else {
                            alert(response.error); // عرض رسالة الخطأ
                        }
                    },
                    error: function(xhr) {
                        var errorMessage = xhr.responseJSON ? xhr.responseJSON.error : 'حدث خطأ أثناء إرسال الطلب.';
                        alert(errorMessage);
                    }
                });
            });
        });
    }
});
// =============================================================================================
// الكود الخاص بإظهار صفحة إلغاء الطلب
document.addEventListener('DOMContentLoaded', function () {
    const cancelMenu = document.querySelector('.canciling-order');
    const cancelLinks = document.querySelectorAll('.in-way .cancel .cancel-me');
    const backButton = document.querySelector('.canciling-order .back');
    const cancelButton = document.querySelector('.canciling-order .cancel-order');
    const cancelInput = document.getElementById('cancel-order-id');

    // التحقق من وجود العناصر قبل إضافة الأحداث
    if (cancelMenu && cancelLinks.length && backButton && cancelButton && cancelInput) {
        function showCancelMenu() {
            cancelMenu.style.display = 'block'; // يعرض العنصر
            setTimeout(() => {
                cancelMenu.style.visibility = 'visible'; // يجعل العنصر مرئيًا
                cancelMenu.style.opacity = '1'; // يضبط الشفافية لتظهر بشكل كامل
                cancelMenu.style.transform = 'translate(-50%, -50%) scale(1)'; // يضبط الحجم ليصل للحجم الطبيعي
            }, 10); // التأخير لتطبيق التحول بشكل صحيح
        }

        function hideCancelMenu() {
            cancelMenu.style.opacity = '0'; // يضبط الشفافية لتختفي
            cancelMenu.style.transform = 'translate(-50%, -50%) scale(0.5)'; // يصغر الحجم مرة أخرى
            setTimeout(() => {
                cancelMenu.style.visibility = 'hidden'; // يخفي العنصر
                cancelMenu.style.display = 'none'; // يزيل العنصر من التدفق الطبيعي للصفحة
            }, 300); 
        }

        cancelLinks.forEach(function (cancelLink) {
            cancelLink.addEventListener('click', function (e) {
                e.preventDefault();

                // نسخ الـ id الخاص بالطلب الذي تم النقر عليه إلى الحقل المخفي
                const cancelId = this.getAttribute('date-cancel-id');
                cancelInput.value = cancelId;

                if (cancelMenu.style.visibility === 'hidden' || cancelMenu.style.visibility === '') {
                    showCancelMenu();
                }
            });
        });

        backButton.addEventListener('click', hideCancelMenu);

        document.addEventListener('click', function (e) {
            if (cancelMenu.style.visibility === 'visible' && !cancelMenu.contains(e.target) && !e.target.closest('.cancel-me')) {
                hideCancelMenu();
            }
        });
    }
});
// =================================================================================================== 

