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
