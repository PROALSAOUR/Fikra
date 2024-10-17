// window.addEventListener('beforeinstallprompt', (e) => {
//     e.preventDefault(); // منع العرض التلقائي
//     deferredPrompt = e;
//     console.log('beforeinstallprompt fired'); // سجل الرسالة

//     installBtn.style.display = 'block'; // إظهار الزر

//     installBtn.addEventListener('click', () => {
//         installBtn.style.display = 'none'; // إخفاء الزر بعد النقر عليه
//         deferredPrompt.prompt(); // إظهار نافذة التثبيت
//         deferredPrompt.userChoice.then((choiceResult) => {
//             if (choiceResult.outcome === 'accepted') {
//                 console.log('User accepted the install prompt');
//             } else {
//                 console.log('User dismissed the install prompt');
//             }
//             deferredPrompt = null; // إعادة تعيين deferredPrompt
//         });
//     });
// });

  
  
