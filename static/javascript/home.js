// السلايدرات الخاصة بالاعلانات والعلامات التجارية بالصفحة الرئيسية
document.addEventListener('DOMContentLoaded', function() {  
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