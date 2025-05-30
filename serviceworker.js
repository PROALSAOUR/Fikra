let staticCacheName = 'djangopwa-v1.1';

self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(staticCacheName).then(function(cache) {
      return cache.addAll([
        '/offline/',  // صفحة غير متصلة
        '/static/css/offline-style.css',
        '/static/css/all.min.css',
        '/static/css/style.css',
        '/static/javascript/main.js',  
        '/static/images/icons/small-logo.webp',  
      ]);
    })
  );
});

self.addEventListener('activate', function(event) {
  var cacheWhitelist = ['djangopwa-v1.1']; // الكاش الذي ترغب في الاحتفاظ به (الإصدار الجديد)

  event.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.map(function(cacheName) {
          // إذا لم يكن الكاش في قائمة الـ whitelist، قم بحذفه
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName); // حذف الكاش القديم
          }
        })
      );
    })
  );
});

self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request).then(function(response) {
      // إذا كان الطلب هو ملف HTML، لا يتم تخزينه في الكاش
      if (event.request.url.endsWith('.html')) {
        return fetch(event.request); // قم بتحميله مباشرة من الشبكة
      }
      return response || fetch(event.request).catch(function() {
        return caches.match('/offline/'); // إعادة الصفحة غير المتصلة إذا فشل التحميل
      });
    })
  );
});

