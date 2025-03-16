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

self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request).then(function(response) {
      // إذا كان الطلب هو index.html، لا تقدم الملف من الكاش
      if (event.request.url.endsWith('index.html')) {
        return fetch(event.request); // قم بتحميله مباشرة من الشبكة
      }
      return response || fetch(event.request).catch(function() {
        return caches.match('/offline/'); // إعادة الصفحة غير المتصلة إذا فشل التحميل
      });
    })
  );
});
