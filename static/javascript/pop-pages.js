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
// الكود الخاص بتواصل معنا 
document.addEventListener('DOMContentLoaded', function () {
    const contactUsLinks = document.querySelectorAll('.contact-us');
  
    if (contactUsLinks.length > 0) {  // التحقق من وجود العناصر
        contactUsLinks.forEach(function (link) {
            link.addEventListener('click', function (e) {
                e.preventDefault(); // منع الانتقال الافتراضي للرابط
                const phoneNumber = '0926295838';
                const whatsappUrl = `https://wa.me/${phoneNumber}`;
                window.location.href = whatsappUrl; // توجيه المستخدم إلى رابط واتساب
            });
        });
    }
});
// ====================================================================================================
// الكود الخاص بإظهار صفحة افراغ السلة والمفضلة
document.addEventListener('DOMContentLoaded', function () {
    const menus = document.querySelectorAll('.empty-pop-page');
    const links = document.querySelectorAll('.make-it-empty'); // إضافة النقطة المفقودة في الكلاس
    const backButtons = document.querySelectorAll('.empty-pop-page .back');
    const outButtons = document.querySelectorAll('.empty-pop-page .out');

    // التحقق من وجود العناصر
    if (menus.length > 0 && links.length > 0 && backButtons.length > 0 && outButtons.length > 0) {
        function showMenu(menu) {
            menu.style.display = 'block'; // يعرض العنصر
            setTimeout(() => {
                menu.style.visibility = 'visible'; // يجعل العنصر مرئيًا
                menu.style.opacity = '1'; // يضبط الشفافية لتظهر بشكل كامل
                menu.style.transform = 'translate(-50%, -50%) scale(1)'; // يضبط الحجم ليصل للحجم الطبيعي
            }, 10); // التأخير لتطبيق التحول بشكل صحيح
        }

        function hideMenu(menu) {
            menu.style.opacity = '0'; // يضبط الشفافية لتختفي
            menu.style.transform = 'translate(-50%, -50%) scale(0.5)'; // يصغر الحجم مرة أخرى
            setTimeout(() => {
                menu.style.visibility = 'hidden'; // يخفي العنصر
                menu.style.display = 'none'; // يزيل العنصر من التدفق الطبيعي للصفحة
            }, 300); // يجب أن يتطابق مع مدة الـ transition في CSS
        }

        links.forEach((link, index) => {
            if (menus[index]) { // تحقق من وجود العنصر قبل إضافة الحدث
                link.addEventListener('click', function (e) {
                    e.preventDefault();
                    if (menus[index].style.visibility === 'hidden' || menus[index].style.visibility === '') {
                        showMenu(menus[index]);
                    }
                });
            }
        });

        backButtons.forEach((button, index) => {
            if (menus[index]) { // تحقق من وجود العنصر قبل إضافة الحدث
                button.addEventListener('click', () => hideMenu(menus[index]));
            }
        });

        outButtons.forEach((button, index) => {
            if (menus[index]) { // تحقق من وجود العنصر قبل إضافة الحدث
                button.addEventListener('click', () => hideMenu(menus[index]));
            }
        });

        document.addEventListener('click', function (e) {
            menus.forEach((menu, index) => {
                if (menu.style.visibility === 'visible' && !menu.contains(e.target) && !links[index]?.contains(e.target)) {
                    hideMenu(menu);
                }
            });
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

    // التحقق من وجود العناصر قبل إضافة الأحداث
    if (deleteMenu && deleteLink && backButton && outButton) {
        function showDeleteMenu() {
            deleteMenu.style.display = 'block'; // يعرض العنصر
            setTimeout(() => {
                deleteMenu.style.visibility = 'visible'; // يجعل العنصر مرئيًا
                deleteMenu.style.opacity = '1'; // يضبط الشفافية لتظهر بشكل كامل
                deleteMenu.style.transform = 'translate(-50%, -50%) scale(1)'; // يضبط الحجم ليصل للحجم الطبيعي
            }, 10); // التأخير لتطبيق التحول بشكل صحيح
        }

        function hideDeleteMenu() {
            deleteMenu.style.opacity = '0'; // يضبط الشفافية لتختفي
            deleteMenu.style.transform = 'translate(-50%, -50%) scale(0.5)'; // يصغر الحجم مرة أخرى
            setTimeout(() => {
                deleteMenu.style.visibility = 'hidden'; // يخفي العنصر
                deleteMenu.style.display = 'none'; // يزيل العنصر من التدفق الطبيعي للصفحة
            }, 300); // يجب أن يتطابق مع مدة الـ transition في CSS
        }

        deleteLink.addEventListener('click', function (e) {
            e.preventDefault();
            if (deleteMenu.style.visibility === 'hidden' || deleteMenu.style.visibility === '') {
                showDeleteMenu();
            }
        });

        backButton.addEventListener('click', hideDeleteMenu);
        outButton.addEventListener('click', hideDeleteMenu);

        document.addEventListener('click', function (e) {
            if (deleteMenu.style.visibility === 'visible' && !deleteMenu.contains(e.target) && !deleteLink.contains(e.target)) {
                hideDeleteMenu();
            }
        });
    }
});
// ===================================================================================================
// الكود الخاص بإظهار صفحة إلغاء الطلب
document.addEventListener('DOMContentLoaded', function () {
    const cancelMenu = document.querySelector('.canciling-order');
    const cancelLink = document.querySelector('.in-way .cancel .cancel-me');
    const backButton = document.querySelector('.canciling-order .back');
    const cancelButton = document.querySelector('.canciling-order .cancel-order');

    // التحقق من وجود العناصر قبل إضافة الأحداث
    if (cancelMenu && cancelLink && backButton && cancelButton) {
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
            }, 300); // يجب أن يتطابق مع مدة الـ transition في CSS
        }

        cancelLink.addEventListener('click', function (e) {
            e.preventDefault();
            if (cancelMenu.style.visibility === 'hidden' || cancelMenu.style.visibility === '') {
                showCancelMenu();
            }
        });

        backButton.addEventListener('click', hideCancelMenu);
        cancelButton.addEventListener('click', hideCancelMenu);

        document.addEventListener('click', function (e) {
            if (cancelMenu.style.visibility === 'visible' && !cancelMenu.contains(e.target) && !cancelLink.contains(e.target)) {
                hideCancelMenu();
            }
        });
    }
});
// ===================================================================================================
// الكود الخاص بعرض النافذة الخاصة بمشاركة كود الدعوة
document.addEventListener('DOMContentLoaded', function () {
    const shareCodeMenu = document.querySelector('.share-code');
    const shareCodeLink = document.querySelector('.share-code-link');
    const copyIcon = document.querySelector('.share-code code i');
    const shareCodeText = document.querySelector('.share-code code');

    function showShareCodeMenu() {
        shareCodeMenu.style.display = 'block'; // عرض القائمة
        setTimeout(() => {
            shareCodeMenu.style.visibility = 'visible';
            shareCodeMenu.style.opacity = '1';
            shareCodeMenu.style.transform = 'translate(-50%, -40%) scale(1)';
        }, 10);
    }

    function hideShareCodeMenu() {
        shareCodeMenu.style.opacity = '0';
        shareCodeMenu.style.transform = 'translate(-50%, -40%) scale(0.5)';
        setTimeout(() => {
            shareCodeMenu.style.visibility = 'hidden';
            shareCodeMenu.style.display = 'none';
        }, 300);
    }

    // التحقق من وجود العناصر قبل إضافة الأحداث
    if (shareCodeMenu && shareCodeLink) {
        shareCodeLink.addEventListener('click', function (e) {
            e.preventDefault();
            if (shareCodeMenu.style.visibility === 'hidden' || shareCodeMenu.style.visibility === '') {
                showShareCodeMenu();
            }
        });
    }

    if (copyIcon && shareCodeText) {
        copyIcon.addEventListener('click', function () {
            const range = document.createRange();
            range.selectNode(shareCodeText);
            window.getSelection().removeAllRanges(); // إلغاء تحديد النصوص الحالية
            window.getSelection().addRange(range);
            document.execCommand('copy');
            window.getSelection().removeAllRanges(); // إلغاء التحديد بعد النسخ
            alert('تم نسخ الكود بنجاح!');
        });
    }

    document.addEventListener('click', function (e) {
        if (shareCodeMenu && shareCodeMenu.style.visibility === 'visible' && !shareCodeMenu.contains(e.target) && !shareCodeLink.contains(e.target)) {
            hideShareCodeMenu();
        }
    });
});
// ========================================================================================================= 
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
// الكود الخاص بعرض النافذة الخاصة بتحميل التطبيق
document.addEventListener('DOMContentLoaded', function () {
    const downloadMenu = document.querySelector('.download-fikra-page');
    const downloadLink = document.querySelector('.download-fikra-link');

    if (downloadMenu && downloadLink) { // تحقق من وجود العنصرين قبل إضافة الأحداث
        function showDownloadMenu() {
            downloadMenu.style.display = 'block'; // عرض القائمة
            setTimeout(() => {
                downloadMenu.style.visibility = 'visible';
                downloadMenu.style.opacity = '1';
                downloadMenu.style.transform = 'translate(-50%, -40%) scale(1)';
            }, 10);
        }

        function hideDownloadMenu() {
            downloadMenu.style.opacity = '0';
            downloadMenu.style.transform = 'translate(-50%, -40%) scale(0.5)';
            setTimeout(() => {
                downloadMenu.style.visibility = 'hidden';
                downloadMenu.style.display = 'none';
            }, 300);
        }

        downloadLink.addEventListener('click', function (e) {
            e.preventDefault();
            if (downloadMenu.style.visibility === 'hidden' || downloadMenu.style.visibility === '') {
                showDownloadMenu();
            }
        });

        document.addEventListener('click', function (e) {
            if (downloadMenu.style.visibility === 'visible' && !downloadMenu.contains(e.target) && !downloadLink.contains(e.target)) {
                hideDownloadMenu();
            }
        });
    }
});
// ===================================================================================================
// الكود الخاص بعرض النافذة الخاصة بإضافة إلى السلة
document.addEventListener('DOMContentLoaded', function () {
    const menu = document.querySelector('.add-cart-pop-page');
    const link = document.querySelector('.add-cart-pop-link');

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

        link.addEventListener('click', function (e) {
            e.preventDefault();
            if (menu.style.visibility === 'hidden' || menu.style.visibility === '') {
                showMenu();
            }
        });

        document.addEventListener('click', function (e) {
            if (menu.style.visibility === 'visible' && !menu.contains(e.target) && !link.contains(e.target)) {
                hideMenu();
            }
        });
    }
});
// ===================================================================================================
// الكود الخاص بعرض النافذة الخاصة بإتمام عملية الطلب بنجاح
document.addEventListener('DOMContentLoaded', function () {
    const menu = document.querySelector('.ordered-done-pop-page');
    const link = document.querySelector('.ordered-done-link');

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

        link.addEventListener('click', function (e) {
            e.preventDefault();
            if (menu.style.visibility === 'hidden' || menu.style.visibility === '') {
                showMenu();
            }
        });

        document.addEventListener('click', function (e) {
            if (menu.style.visibility === 'visible' && !menu.contains(e.target) && !link.contains(e.target)) {
                hideMenu();
            }
        });
    }
});
// =============================================================================================
// إظهار الفاتورة
document.addEventListener('DOMContentLoaded', function () {
    const showCheckbox = document.querySelector('#show');
    const receipt = document.querySelector('.receipt');
    const confirmButton = document.querySelector('.confirm');
    
    if (showCheckbox && receipt && confirmButton) { // تحقق من وجود العناصر قبل إضافة الأحداث
        // وظيفة لتحديث حالة الفاتورة بناءً على عرض الشاشة
        function updateReceiptVisibility() {
            if (window.innerWidth <= 893) {
                // استعادة حالة التشيك بوكس من localStorage عند تحميل الصفحة
                if (localStorage.getItem('showCheckboxState') === 'checked') {
                    showCheckbox.checked = true;
                    receipt.style.display = 'block';
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
                
                // إضافة حدث للنقر على أي مكان خارج الفاتورة
                document.addEventListener('click', function (event) {
                    if (!receipt.contains(event.target) && event.target !== showCheckbox) {
                        showCheckbox.checked = false;
                        receipt.style.display = 'none';
                        localStorage.setItem('showCheckboxState', 'unchecked');
                    }
                });
                
                // إضافة حدث للنقر على زر يحتوي على الكلاس confirm
                confirmButton.addEventListener('click', function () {
                    showCheckbox.checked = false;
                    receipt.style.display = 'none';
                    localStorage.setItem('showCheckboxState', 'unchecked');
                });
            } else {
                // إذا كانت الشاشة أكبر من 793px، اجعل الفاتورة تظهر دائمًا
                receipt.style.display = 'block';
                localStorage.removeItem('showCheckboxState'); // إزالة حالة التشيك بوكس من localStorage
            }
        }
        
        // استدعاء الوظيفة عند تحميل الصفحة
        updateReceiptVisibility();
        
        // استدعاء الوظيفة عند تغيير حجم الشاشة
        window.addEventListener('resize', updateReceiptVisibility);
    }
});
// =============================================================================================
