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
